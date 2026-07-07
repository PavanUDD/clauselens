import uuid
import time
import logging
import asyncio
import tempfile
import os
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from clauselens.ingestion.pdf_loader import load_pdf
from clauselens.ingestion.chunker import split_into_chunks
from clauselens.classification.contract_classifier import classify
from clauselens.analysis.risk_engine import evaluate
from clauselens.analysis.health_score import compute
from clauselens.analysis.term_extractor import extract_all_terms

MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '20'))
UPLOAD_TIMEOUT_SECONDS = int(os.getenv('UPLOAD_TIMEOUT_SECONDS', '120'))
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)
log = logging.getLogger('clauselens.api')


class JobStorage:
    def __init__(self):
        self._store = {}

    def create(self, job_id: str):
        self._store[job_id] = {
            'status': 'processing',
            'created_at': datetime.utcnow(),
            'result': None,
            'error': None,
            'timings': {}
        }

    def complete(self, job_id: str, result: dict, timings: dict):
        self._store[job_id]['status'] = 'complete'
        self._store[job_id]['result'] = result
        self._store[job_id]['timings'] = timings
        self._store[job_id]['completed_at'] = datetime.utcnow()

    def fail(self, job_id: str, error: str):
        self._store[job_id]['status'] = 'error'
        self._store[job_id]['error'] = error

    def get(self, job_id: str) -> Optional[dict]:
        return self._store.get(job_id)

    def cleanup_old_jobs(self, max_age_hours: int = 1):
        cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)
        expired = [
            k for k, v in self._store.items()
            if v['created_at'] < cutoff
        ]
        for k in expired:
            del self._store[k]
        if expired:
            log.info(f'Cleaned up {len(expired)} expired jobs')


JOB_STORE = JobStorage()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info(f'ClauseLens API v{APP_VERSION} starting up')

    async def cleanup_loop():
        while True:
            await asyncio.sleep(3600)
            JOB_STORE.cleanup_old_jobs()

    asyncio.create_task(cleanup_loop())
    log.info('ClauseLens API ready')

    yield

    log.info('ClauseLens API shutting down')


app = FastAPI(
    title='ClauseLens API',
    version=APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


def validate_pdf_bytes(content: bytes, filename: str) -> None:
    if filename and os.path.splitext(filename)[1].lower() in {'.doc', '.docx', '.txt', '.xlsx'}:
        raise HTTPException(400, 'Only PDF files are supported. Please convert your document to PDF and re-upload.')
    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(400, f'File too large. Maximum {MAX_FILE_SIZE_MB}MB.')
    if len(content) < 4 or content[:4] != b'%PDF':
        raise HTTPException(400, 'Invalid file. PDF required.')
    if len(content) < 100:
        raise HTTPException(400, 'File appears empty or corrupted.')
    if b'/Encrypt' in content[:2048]:
        raise HTTPException(400, 'Password-protected PDFs are not supported. Please remove the password and re-upload.')


def process_contract(job_id: str, file_bytes: bytes, filename: str):
    request_log = logging.getLogger(f'clauselens.job.{job_id[:8]}')
    timings = {}
    tmp_path = None

    try:
        request_log.info(f'Starting analysis: {filename} ({len(file_bytes)/1024:.0f}KB)')
        overall_start = time.time()

        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        t = time.time()
        pages = load_pdf(tmp_path)
        timings['pdf_extraction'] = round(time.time() - t, 2)
        request_log.info(f'Extracted {len(pages)} pages in {timings["pdf_extraction"]}s')

        if not pages:
            raise ValueError('No text could be extracted. The PDF may be scanned or image-based.')

        t = time.time()
        chunks = split_into_chunks(pages)
        timings['chunking'] = round(time.time() - t, 2)
        request_log.info(f'Created {len(chunks)} chunks in {timings["chunking"]}s')

        t = time.time()
        contract_type, confidence, scores = classify(chunks)
        timings['classification'] = round(time.time() - t, 2)
        request_log.info(f'Classified as {contract_type} ({confidence:.0%}) in {timings["classification"]}s')

        t = time.time()
        terms = extract_all_terms(chunks)
        timings['term_extraction'] = round(time.time() - t, 2)

        t = time.time()
        flags = evaluate(chunks, contract_type, terms)
        timings['rule_engine'] = round(time.time() - t, 2)
        request_log.info(f'Rule engine: {len(flags)} flags in {timings["rule_engine"]}s')

        t = time.time()
        health = compute(flags)
        timings['scoring'] = round(time.time() - t, 2)

        timings['total'] = round(time.time() - overall_start, 2)
        request_log.info(f'Analysis complete: {health["score"]}/100 in {timings["total"]}s')

        if timings['total'] > UPLOAD_TIMEOUT_SECONDS:
            raise TimeoutError(f'Analysis exceeded {UPLOAD_TIMEOUT_SECONDS}s timeout')

        def serialize_flag(flag):
            return {
                'rule_id': flag.rule_id,
                'name': flag.name,
                'severity': flag.severity,
                'category': flag.category,
                'plain_english': flag.plain_english,
                'explanation': flag.explanation,
                'negotiation_script': flag.negotiation_script,
                'typical_range': flag.typical_range,
                'evidence': flag.evidence,
                'match_strength': flag.match_strength,
                'learn_more': getattr(flag, 'learn_more', None),
            }

        result = {
            'contract_type': contract_type,
            'confidence': confidence,
            'page_count': len(pages),
            'chunk_count': len(chunks),
            'health': health,
            'flags': [serialize_flag(f) for f in flags],
            'terms': terms,
            'timings': timings,
            'filename': filename,
            'analyzed_at': datetime.utcnow().isoformat(),
        }

        JOB_STORE.complete(job_id, result, timings)

    except Exception as e:
        error_msg = str(e)
        request_log.error(f'Analysis failed: {error_msg}')
        JOB_STORE.fail(job_id, error_msg)
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)
            request_log.debug('Temp file deleted')


@app.post('/api/v1/analyze')
async def analyze(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    request_id = str(uuid.uuid4())
    log.info(f'Upload received: {file.filename} | request={request_id[:8]}')

    content = await file.read()
    validate_pdf_bytes(content, file.filename)

    job_id = str(uuid.uuid4())
    JOB_STORE.create(job_id)
    background_tasks.add_task(process_contract, job_id, content, file.filename)

    log.info(f'Job queued: {job_id[:8]} | request={request_id[:8]}')

    return {
        'job_id': job_id,
        'status': 'processing',
        'request_id': request_id
    }


@app.get('/api/v1/results/{job_id}')
async def get_results(job_id: str):
    job = JOB_STORE.get(job_id)

    if not job:
        raise HTTPException(404, f'Job {job_id} not found')

    if job['status'] == 'processing':
        return {'status': 'processing', 'job_id': job_id}

    if job['status'] == 'error':
        raise HTTPException(500, {
            'status': 'error',
            'message': job['error'],
            'job_id': job_id
        })

    return {
        'status': 'complete',
        'job_id': job_id,
        **job['result']
    }


@app.get('/api/v1/health')
async def health_check():
    return {
        'status': 'ok',
        'version': APP_VERSION,
        'active_jobs': len([
            j for j in JOB_STORE._store.values()
            if j['status'] == 'processing'
        ])
    }
