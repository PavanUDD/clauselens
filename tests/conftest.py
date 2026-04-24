"""Pytest fixtures shared across test files."""
import pytest


@pytest.fixture
def rental_chunks():
    """Sample rental contract chunks for testing."""
    return [
        {
            "chunk_id": 0,
            "page_num": 1,
            "text": "This Residential Lease Agreement is entered into between the Landlord and Tenant. The monthly rent shall be $1,800. A security deposit of $3,600 is required.",
        },
        {
            "chunk_id": 1,
            "page_num": 2,
            "text": "If Tenant breaks the lease early, Tenant shall pay three months rent as liquidated damages. The Landlord may enter the premises without notice.",
        },
        {
            "chunk_id": 2,
            "page_num": 3,
            "text": "No pets shall be allowed on the premises. Tenant shall not sublet this agreement. All utilities are the tenant's responsibility.",
        },
        {
            "chunk_id": 3,
            "page_num": 4,
            "text": "This lease shall automatically renew for successive one-year terms. The prevailing party shall recover reasonable attorneys fees.",
        },
    ]


@pytest.fixture
def employment_chunks():
    """Sample employment contract chunks."""
    return [
        {
            "chunk_id": 0,
            "page_num": 1,
            "text": "This Employment Agreement is between Employer and Employee. Employee shall be paid a salary of $120,000. Employment is at-will.",
        },
        {
            "chunk_id": 1,
            "page_num": 2,
            "text": "Employee agrees to a non-compete clause for 24 months following termination. Employee shall not solicit clients or employees. All inventions are work made for hire.",
        },
        {
            "chunk_id": 2,
            "page_num": 3,
            "text": "Disputes shall be resolved by binding arbitration. No severance will be paid upon termination.",
        },
    ]


@pytest.fixture
def sample_text_with_money():
    return "The total fee is $50,000. Additional costs may include $1,200 in setup fees and a $500 deposit."


@pytest.fixture
def sample_text_with_percentages():
    return "Late fees are 5% of monthly rent. Rent increases are capped at 10% annually. Interest accrues at 1.5 percent per month."


@pytest.fixture
def sample_text_with_durations():
    return "This contract is valid for 12 months. Notice must be given 30 days in advance. Probationary period is 3 months."