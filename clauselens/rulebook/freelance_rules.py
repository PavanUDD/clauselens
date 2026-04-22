"""Freelance / contractor agreement rulebook — 10 rules."""
from __future__ import annotations
from clauselens.rulebook.schema import Rule

FREELANCE_RULES: list[Rule] = [

    Rule(
        rule_id="FREE_R001",
        name="IP automatically transferred to client",
        contract_types=["freelance"],
        severity="HIGH",
        category="ip",
        detection_patterns=[
            r"work\s+(made\s+)?for\s+hire",
            r"all\s+(work\s+product|deliverables|ip)\s+(shall\s+be|are)\s+(owned|assigned|property)",
            r"assign\w*\s+all\s+right",
            r"client\s+(shall|will)\s+own\s+(all|the)",
        ],
        plain_english="The client owns everything you create, including rights to use it however they want.",
        explanation_template=(
            "This contract transfers all IP to the client on payment. Consider a "
            "license-back clause letting you use portfolio snippets, or retention "
            "of rights to general methodologies you develop. Pages {pages}."
        ),
        typical_range="IP assigned on full payment; contractor retains portfolio/methodology rights",
        negotiation_script=(
            "Can we add a clause allowing me to reference this work in my portfolio "
            "and retain rights to general tools/methodologies I develop?"
        ),
    ),

    Rule(
        rule_id="FREE_R002",
        name="Late or delayed payment terms",
        contract_types=["freelance"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"net\s+(30|45|60|90)",
            r"payable\s+within\s+\d+\s+days",
            r"payment\s+due\s+(within|upon)",
            r"invoice\s+(shall|will)\s+be\s+paid",
        ],
        plain_english="Check how long you wait for payment — and what happens if it's late.",
        explanation_template=(
            "Payment terms are defined here. Net 30 is standard for freelancers; "
            "Net 60 or Net 90 is tough on cashflow. Verify late-payment penalties "
            "favor you, not the client. Pages {pages}."
        ),
        typical_range="Net 15-30 days with 1.5%/month late fee",
        negotiation_script=(
            "Can we shorten the payment terms to Net 15, and add 1.5% monthly interest "
            "on overdue invoices? That's standard for independent contractors."
        ),
    ),

    Rule(
        rule_id="FREE_R003",
        name="Unlimited revisions clause",
        contract_types=["freelance"],
        severity="HIGH",
        category="scope",
        detection_patterns=[
            r"unlimited\s+revisions",
            r"revisions?\s+(until|as\s+needed)",
            r"client\s+satisfaction",
            r"revise\s+until\s+(approved|satisfactory)",
        ],
        plain_english="The client can ask for endless revisions at no extra charge — scope creep risk.",
        explanation_template=(
            "This contract may allow unlimited revisions. Without a cap, a single "
            "project can absorb weeks of unpaid work. Pages {pages}."
        ),
        typical_range="2-3 rounds of revisions included; additional revisions billed hourly",
        negotiation_script=(
            "Can we cap revisions at 2 rounds included, with additional revisions "
            "billed at my standard hourly rate? That protects both of us from scope creep."
        ),
    ),

    Rule(
        rule_id="FREE_R004",
        name="Broad non-compete for contractor",
        contract_types=["freelance"],
        severity="HIGH",
        category="restriction",
        detection_patterns=[
            r"non.?compete",
            r"shall\s+not\s+(provide|perform)\s+(similar|competing)",
            r"exclusiv\w+\s+services",
            r"not\s+work\s+for\s+(competitors|competing)",
        ],
        plain_english="You may be blocked from working with similar clients.",
        explanation_template=(
            "This non-compete restricts who you can work with. For contractors, "
            "non-competes are often unenforceable — but they can still chill "
            "your business. Pages {pages}."
        ),
        typical_range="No non-compete, or narrow to specific named competitors for 6 months",
        negotiation_script=(
            "As an independent contractor, a broad non-compete limits my ability to "
            "serve my business. Can we remove it, or narrow to specific named "
            "competitors for 6 months post-engagement?"
        ),
    ),

    Rule(
        rule_id="FREE_R005",
        name="Kill fee / early termination terms",
        contract_types=["freelance"],
        severity="MEDIUM",
        category="termination",
        detection_patterns=[
            r"kill\s+fee",
            r"cancellation\s+fee",
            r"terminat\w+\s+for\s+convenience",
            r"terminat\w+\s+at\s+any\s+time",
        ],
        plain_english="If the client cancels mid-project, check what you're owed.",
        explanation_template=(
            "This contract addresses early termination. Without a kill fee, "
            "a cancelled project leaves you unpaid for time invested. Pages {pages}."
        ),
        typical_range="50% of remaining fees + payment for work completed",
        negotiation_script=(
            "Can we add a kill fee of 50% of remaining project fees if terminated "
            "for convenience? That covers my committed time and opportunity cost."
        ),
    ),

    Rule(
        rule_id="FREE_R006",
        name="Contractor liability / indemnification",
        contract_types=["freelance"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"indemnif\w+\s+(the\s+)?client",
            r"contractor\s+(shall|will)\s+indemnif",
            r"hold\s+(the\s+)?client\s+harmless",
            r"unlimited\s+liabilit",
        ],
        plain_english="You may be personally liable for client losses or third-party claims.",
        explanation_template=(
            "This clause can expose you to unlimited personal liability. "
            "Always cap contractor liability at the contract value. Pages {pages}."
        ),
        typical_range="Liability capped at fees paid in the prior 12 months",
        negotiation_script=(
            "Can we cap my liability at the total fees paid under this agreement, "
            "and exclude indirect/consequential damages? That's standard for independent contractors."
        ),
    ),

    Rule(
        rule_id="FREE_R007",
        name="Client owns pre-existing work",
        contract_types=["freelance"],
        severity="HIGH",
        category="ip",
        detection_patterns=[
            r"pre.?existing\s+(work|ip|materials)",
            r"prior\s+works?",
            r"existing\s+(tools|templates|code)",
            r"background\s+ip",
        ],
        plain_english="The client may try to claim tools or code you built before this engagement.",
        explanation_template=(
            "Verify this contract carves out your pre-existing tools, templates, "
            "libraries, and methodology from IP assignment. Pages {pages}."
        ),
        typical_range="Background IP explicitly retained by contractor; licensed to client for project use",
        negotiation_script=(
            "I'd like to add an explicit schedule listing my pre-existing tools, "
            "templates, and libraries — with a license to the client for project "
            "use but retained ownership by me."
        ),
    ),

    Rule(
        rule_id="FREE_R008",
        name="Exclusivity requirement",
        contract_types=["freelance"],
        severity="MEDIUM",
        category="restriction",
        detection_patterns=[
            r"exclusiv\w+",
            r"full.?time\s+(attention|commitment)",
            r"sole\s+(client|engagement)",
            r"not\s+work\s+for\s+other",
        ],
        plain_english="The client may require you to work only with them.",
        explanation_template=(
            "Exclusivity turns a contractor relationship into a de-facto employment "
            "arrangement, risking misclassification (IRS / state). Pages {pages}."
        ),
        typical_range="Non-exclusive; contractor free to serve other clients",
        negotiation_script=(
            "Can we make this a non-exclusive engagement? Exclusivity can create "
            "worker misclassification issues and limits my business."
        ),
    ),

    Rule(
        rule_id="FREE_R009",
        name="Unclear scope / deliverables",
        contract_types=["freelance"],
        severity="MEDIUM",
        category="scope",
        detection_patterns=[
            r"scope\s+of\s+(work|services)",
            r"deliverables",
            r"statement\s+of\s+work",
            r"\bsow\b",
        ],
        plain_english="Check that deliverables and acceptance criteria are specific and measurable.",
        explanation_template=(
            "The Scope of Work section is referenced. Vague scope = scope creep. "
            "Demand specifics: exact deliverables, acceptance criteria, and "
            "what's explicitly out of scope. Pages {pages}."
        ),
        typical_range="Specific deliverables, measurable acceptance criteria, named exclusions",
        negotiation_script=(
            "Can we attach a detailed SOW with specific deliverables, acceptance "
            "criteria, and explicit out-of-scope items? Protects both of us."
        ),
    ),

    Rule(
        rule_id="FREE_R010",
        name="Confidentiality obligations",
        contract_types=["freelance"],
        severity="LOW",
        category="confidentiality",
        detection_patterns=[
            r"confidentialit\w+",
            r"non.?disclosure",
            r"trade\s+secret",
            r"proprietary\s+information",
        ],
        plain_english="Confidentiality terms are present — verify they're reasonable in scope and duration.",
        explanation_template=(
            "NDA obligations are present. Typical is 2-3 years for general info, "
            "perpetual only for defined trade secrets. Pages {pages}."
        ),
        typical_range="2-3 years for general confidential info",
        negotiation_script=(
            "Can we limit confidentiality obligations to 3 years for general "
            "information, with perpetual coverage only for defined trade secrets?"
        ),
    ),
]