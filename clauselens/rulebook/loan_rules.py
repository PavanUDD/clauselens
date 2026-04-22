"""Loan / financial agreement rulebook — 10 rules."""
from __future__ import annotations
from clauselens.rulebook.schema import Rule

LOAN_RULES: list[Rule] = [

    Rule(
        rule_id="LOAN_R001",
        name="High annual percentage rate (APR)",
        contract_types=["loan"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"annual\s+percentage\s+rate",
            r"\bapr\b",
            r"interest\s+rate\s+of",
            r"\d+\.\d+\s*%\s+per\s+(year|annum)",
        ],
        plain_english="Check the APR carefully — it's the real cost of the loan.",
        explanation_template=(
            "APR is disclosed in this agreement. Typical personal loans: 6-36% APR "
            "depending on credit. Anything above 36% flirts with predatory lending "
            "territory in many states. Pages {pages}."
        ),
        typical_range="Personal loans: 6-36% APR; mortgages: 5-8%",
        negotiation_script=(
            "The APR here seems high for my credit profile. Can we discuss a lower "
            "rate or review if I qualify for better terms?"
        ),
    ),

    Rule(
        rule_id="LOAN_R002",
        name="Prepayment penalty",
        contract_types=["loan"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"prepayment\s+penalt",
            r"early\s+payoff\s+(fee|charge)",
            r"penalt\w+\s+for\s+early\s+payment",
        ],
        plain_english="You may be penalized for paying off the loan early.",
        explanation_template=(
            "This loan has a prepayment penalty. That means if you pay it off early "
            "(refinance, windfall, etc.), you owe an extra fee. Pages {pages}."
        ),
        typical_range="No prepayment penalty (standard for most consumer loans since 2014)",
        negotiation_script=(
            "Can we remove the prepayment penalty? Most modern consumer loans don't "
            "have them, and I want flexibility to pay ahead."
        ),
    ),

    Rule(
        rule_id="LOAN_R003",
        name="Variable / adjustable interest rate",
        contract_types=["loan"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"variable\s+(interest\s+)?rate",
            r"adjustable\s+rate",
            r"rate\s+may\s+(change|vary|adjust)",
            r"indexed\s+to",
        ],
        plain_english="The interest rate can go up over time — your payments can grow.",
        explanation_template=(
            "This is a variable-rate loan. Your monthly payment can increase if "
            "rates rise. Verify the cap on rate changes and payment shock. Pages {pages}."
        ),
        typical_range="Rate cap of 2% per adjustment, 5% lifetime cap",
        negotiation_script=(
            "Can we convert this to a fixed rate, or at minimum add caps of 2% per "
            "adjustment period and 5% over the life of the loan?"
        ),
    ),

    Rule(
        rule_id="LOAN_R004",
        name="Personal guarantee",
        contract_types=["loan"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"personal(ly)?\s+guarantee",
            r"personal\s+liabilit",
            r"joint(ly)?\s+and\s+several(ly)?\s+liable",
            r"co.?signer",
        ],
        plain_english="You're personally on the hook — your personal assets are at risk.",
        explanation_template=(
            "A personal guarantee makes you individually liable for the loan, even "
            "if it's in a business name. Your personal assets (home, savings) can "
            "be pursued on default. Pages {pages}."
        ),
        typical_range="Limited guarantee, or business-only liability with corporate veil",
        negotiation_script=(
            "Can we limit the personal guarantee — either remove it, cap it at a "
            "specific amount, or tie it to a fixed period rather than the full loan term?"
        ),
    ),

    Rule(
        rule_id="LOAN_R005",
        name="Default and acceleration clause",
        contract_types=["loan"],
        severity="HIGH",
        category="default",
        detection_patterns=[
            r"default",
            r"acceleration\s+(of|clause)",
            r"(the\s+)?entire\s+balance\s+(shall|may)\s+become\s+due",
            r"accelerate\s+(the\s+)?(loan|balance)",
        ],
        plain_english="Missing a payment can trigger the entire loan being due immediately.",
        explanation_template=(
            "A default + acceleration clause means missing a payment can make the "
            "whole balance due at once. Verify the cure period (time to fix missed "
            "payments) before acceleration kicks in. Pages {pages}."
        ),
        typical_range="30-day cure period before acceleration",
        negotiation_script=(
            "Can we include a 30-day written notice and cure period before any "
            "acceleration? That gives me a fair chance to resolve issues."
        ),
    ),

    Rule(
        rule_id="LOAN_R006",
        name="Collateral / security interest",
        contract_types=["loan"],
        severity="MEDIUM",
        category="collateral",
        detection_patterns=[
            r"collateral",
            r"security\s+interest",
            r"lien\s+(on|against)",
            r"secured\s+by",
        ],
        plain_english="The loan is secured by something you own — it can be seized on default.",
        explanation_template=(
            "This loan is secured by collateral. On default, the lender can take "
            "the collateral to satisfy the debt. Verify exactly what's pledged. Pages {pages}."
        ),
        typical_range="Specific named collateral; no blanket UCC-1 liens on unrelated assets",
        negotiation_script=(
            "Can we specify exactly what collateral is pledged, and exclude any "
            "blanket lien on future or unrelated assets?"
        ),
    ),

    Rule(
        rule_id="LOAN_R007",
        name="Late payment fees",
        contract_types=["loan"],
        severity="MEDIUM",
        category="payment",
        detection_patterns=[
            r"late\s+(payment\s+)?(fee|charge)",
            r"late\s+fee\s+of",
            r"overdue\s+(payment|balance)\s+fee",
        ],
        plain_english="Check the late-payment fee amount — some are aggressive.",
        explanation_template=(
            "Late fees are defined here. Typical is 5% of the overdue payment or "
            "$25-40 flat, whichever is greater. Higher fees may be unenforceable. Pages {pages}."
        ),
        typical_range="5% of overdue payment or $25 flat",
        negotiation_script=(
            "Can we cap late fees at 5% of the overdue amount, with a 10-day grace "
            "period before they apply?"
        ),
    ),

    Rule(
        rule_id="LOAN_R008",
        name="Binding arbitration for disputes",
        contract_types=["loan"],
        severity="MEDIUM",
        category="legal",
        detection_patterns=[
            r"binding\s+arbitration",
            r"mandatory\s+arbitration",
            r"class\s+action\s+waiver",
        ],
        plain_english="Disputes go to arbitration, not court — you lose some rights.",
        explanation_template=(
            "Arbitration clauses are present. Arbitration limits your ability to "
            "sue in court or join class actions. Pages {pages}."
        ),
        typical_range="Optional arbitration for consumers; small-claims court preserved",
        negotiation_script=(
            "Can we make arbitration optional, and preserve my right to use "
            "small-claims court for smaller disputes?"
        ),
    ),

    Rule(
        rule_id="LOAN_R009",
        name="Cross-default or cross-collateralization",
        contract_types=["loan"],
        severity="HIGH",
        category="default",
        detection_patterns=[
            r"cross.?default",
            r"cross.?collateraliz\w+",
            r"default\s+under\s+(any\s+)?other",
        ],
        plain_english="Default on a DIFFERENT loan can trigger default on this one too.",
        explanation_template=(
            "Cross-default clauses link this loan to others. A problem with one "
            "loan can accelerate multiple loans. Pages {pages}."
        ),
        typical_range="No cross-default; each loan stands alone",
        negotiation_script=(
            "Can we remove any cross-default or cross-collateralization provisions? "
            "I'd like each loan to stand on its own terms."
        ),
    ),

    Rule(
        rule_id="LOAN_R010",
        name="Loan fees / origination costs",
        contract_types=["loan"],
        severity="LOW",
        category="payment",
        detection_patterns=[
            r"origination\s+fee",
            r"processing\s+fee",
            r"loan\s+(origination|processing)",
            r"closing\s+costs",
        ],
        plain_english="Upfront fees add to the true cost — check what's rolled in.",
        explanation_template=(
            "Origination or processing fees apply. Typical origination: 1-5% of "
            "loan amount. Higher fees inflate the effective cost of borrowing. Pages {pages}."
        ),
        typical_range="1-3% origination fee for personal loans",
        negotiation_script=(
            "Can we reduce or waive the origination fee? Many lenders offer 0-1% "
            "origination for strong applicants."
        ),
    ),
]