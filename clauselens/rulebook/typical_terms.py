"""Industry-benchmark 'typical' values per contract type.

Used for side-by-side comparison tables and threshold checks.
Sources: consumer protection guides, standard industry practice.
NOT legal advice. Rough norms only.
"""
from __future__ import annotations

TYPICAL_TERMS: dict[str, dict[str, dict]] = {
    "rental": {
        "security_deposit": {
            "typical": "1 to 2 months rent",
            "max_months": 2,
            "note": "Many states cap deposits at 2 months rent."
        },
        "early_termination_penalty": {
            "typical": "1 month rent OR forfeit deposit (not both)",
            "max_months": 1,
            "note": "Charging both is unusually aggressive."
        },
        "notice_period_days": {
            "typical": "30 days written notice",
            "min_days": 30,
            "note": "Less than 30 days is tenant-unfavorable."
        },
        "rent_increase_annual_pct": {
            "typical": "3-8% annually",
            "max_pct": 8.0,
            "note": "Above 10% per year is aggressive; some states cap this."
        },
        "late_fee_pct": {
            "typical": "5% of monthly rent",
            "max_pct": 10.0,
            "note": "Late fees above 10% are often unenforceable."
        },
        "lease_term_months": {
            "typical": "12 months",
            "note": "Multi-year leases without early-out are risky."
        },
    },
    "employment": {
        "non_compete_months": {
            "typical": "6-12 months within same region",
            "max_months": 12,
            "note": "Over 12 months or nationwide is often unenforceable."
        },
        "severance_months": {
            "typical": "1-4 weeks per year of service",
            "note": "No severance for involuntary termination is unfavorable."
        },
        "notice_period_days": {
            "typical": "2 weeks (employee) / 30-60 days (employer)",
            "min_days": 14,
            "note": "Asymmetric notice periods favor the employer."
        },
        "probation_months": {
            "typical": "3 months",
            "max_months": 6,
            "note": "Probation beyond 6 months is unusual."
        },
        "pto_days": {
            "typical": "10-20 days paid time off annually",
            "min_days": 10,
            "note": "Below 10 days PTO is below US norm for salaried roles."
        },
        "at_will_clause": {
            "typical": "Standard in most US states",
            "note": "Means either party can terminate anytime; normal but check severance."
        },
    },
}


def get_typical(contract_type: str, term_key: str) -> dict:
    """Safe lookup of a typical-term entry."""
    return TYPICAL_TERMS.get(contract_type, {}).get(term_key, {})


def get_all_typical(contract_type: str) -> dict[str, dict]:
    """All typical terms for a contract type."""
    return TYPICAL_TERMS.get(contract_type, {})