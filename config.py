"""ClauseLens — central configuration."""
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent
STORAGE_DIR = PROJECT_ROOT / "storage"
SAMPLES_DIR = PROJECT_ROOT / "samples"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create dirs
for d in [STORAGE_DIR, SAMPLES_DIR, LOGS_DIR]:
    d.mkdir(exist_ok=True)

# Model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

# Chunking
CHUNK_SIZE = 180           # words per chunk
CHUNK_OVERLAP = 40         # word overlap between chunks

# Retrieval
DEFAULT_TOP_K = 5
MIN_SIMILARITY_SCORE = 0.35

# Risk engine
SEVERITY_WEIGHTS = {"HIGH": 15, "MEDIUM": 7, "LOW": 2}
MAX_HEALTH_SCORE = 100

# Contract types
SUPPORTED_CONTRACT_TYPES = ["rental", "employment", "freelance", "saas", "loan", "unknown"]
LAUNCH_CONTRACT_TYPES = ["rental", "employment"]  # fully built

# UI
APP_NAME = "ClauseLens"
APP_TAGLINE = "Your contract, reviewed. Privately. Instantly."
THEME_BG = "#0a0a0f"
THEME_ACCENT = "#3b82f6"

# Privacy
ENABLE_TELEMETRY = False
LOG_USER_CONTENT = False   # NEVER change this to True