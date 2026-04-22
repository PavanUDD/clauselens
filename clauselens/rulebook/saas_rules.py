"""SaaS / subscription service agreement rulebook — 10 rules."""
from __future__ import annotations
from clauselens.rulebook.schema import Rule

SAAS_RULES: list[Rule] = [

    Rule(
        rule_id="SAAS_R001",
        name="Auto-renewal with short notice window",
        contract_types=["saas"],
        severity="HIGH",
        category="renewal",
        detection_patterns=[
            r"auto.?renew\w*",
            r"automatically\s+renew",
            r"shall\s+renew",
            r"evergreen",
        ],
        plain_english="Your subscription renews automatically — easy to miss the cancellation window.",
        explanation_template=(
            "This SaaS contract auto-renews. Check the notice window (often 30-90 days "
            "before renewal). Miss it and you're locked in for another term. Pages {pages}."
        ),
        typical_range="30 days notice to cancel; month-to-month after initial term",
        negotiation_script=(
            "Can we change this to month-to-month after the initial term, or shorten "
            "the cancellation notice window to 30 days?"
        ),
    ),

    Rule(
        rule_id="SAAS_R002",
        name="Unilateral price increase rights",
        contract_types=["saas"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"increase\s+(the\s+)?(fees|price|subscription)",
            r"price\s+(change|adjustment|increase)",
            r"modify\s+(the\s+)?fees",
            r"adjust\w+\s+subscription",
        ],
        plain_english="The vendor can raise prices — check if and how they're capped.",
        explanation_template=(
            "This SaaS agreement permits price changes. Without a cap, vendors can "
            "raise fees dramatically at renewal. Pages {pages}."
        ),
        typical_range="CPI-linked or capped at 5-7% per year, with 60 days notice",
        negotiation_script=(
            "Can we cap annual price increases at the greater of CPI or 5%, with "
            "60 days written notice? That protects our budget predictability."
        ),
    ),

    Rule(
        rule_id="SAAS_R003",
        name="Weak SLA / uptime guarantee",
        contract_types=["saas"],
        severity="MEDIUM",
        category="service",
        detection_patterns=[
            r"uptime",
            r"service\s+level\s+agreement",
            r"\bsla\b",
            r"availability",
            r"99\.\d+\s*%",
        ],
        plain_english="Check the uptime commitment and what you get if it's broken.",
        explanation_template=(
            "SLA terms are defined here. Typical SaaS uptime is 99.9% (~8h downtime/yr). "
            "Below 99.5% is weak. Remedies should be credits you can actually use. Pages {pages}."
        ),
        typical_range="99.9% uptime with service credits as primary remedy",
        negotiation_script=(
            "Can we secure a 99.9% uptime SLA with tiered service credits for any "
            "breach, and the right to terminate for repeated SLA failures?"
        ),
    ),

    Rule(
        rule_id="SAAS_R004",
        name="Data ownership and portability",
        contract_types=["saas"],
        severity="HIGH",
        category="data",
        detection_patterns=[
            r"your\s+data",
            r"customer\s+data",
            r"data\s+(ownership|portability|export)",
            r"right\s+to\s+(use|access)\s+(your|customer)\s+data",
        ],
        plain_english="Who owns the data you put in, and can you get it out?",
        explanation_template=(
            "Data ownership terms are present. Verify: (1) you retain ownership, "
            "(2) you can export data in a standard format anytime, (3) vendor "
            "deletes data on termination. Pages {pages}."
        ),
        typical_range="Customer owns data; vendor provides export + deletes on termination",
        negotiation_script=(
            "Can we confirm in writing that we retain full ownership of our data, "
            "have export rights in a standard format (CSV/JSON) anytime, and "
            "you'll delete all data within 30 days of termination?"
        ),
    ),

    Rule(
        rule_id="SAAS_R005",
        name="Liability cap below fees paid",
        contract_types=["saas"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"limit\w+\s+of\s+liabilit",
            r"aggregate\s+liabilit",
            r"liabilit\w+\s+(shall\s+not\s+exceed|capped)",
            r"in\s+no\s+event\s+shall",
        ],
        plain_english="If the vendor fails you, there's a cap on how much you can recover.",
        explanation_template=(
            "Liability is capped. Typical cap is 12 months of fees paid. Caps "
            "below that, or tied to just the last payment, are vendor-favorable. Pages {pages}."
        ),
        typical_range="Liability capped at 12 months of fees paid",
        negotiation_script=(
            "Can we raise the liability cap to 12 months of fees paid? The current "
            "cap doesn't reflect the actual risk of data loss or service failure."
        ),
    ),

    Rule(
        rule_id="SAAS_R006",
        name="Mandatory arbitration / no class action",
        contract_types=["saas"],
        severity="MEDIUM",
        category="legal",
        detection_patterns=[
            r"binding\s+arbitration",
            r"mandatory\s+arbitration",
            r"class\s+action\s+waiver",
            r"waive\s+.*\s+class",
        ],
        plain_english="Disputes go to arbitration, not court, and you can't join a class action.",
        explanation_template=(
            "Arbitration and/or class-action waivers limit your legal options. "
            "For B2B SaaS, sometimes acceptable; for consumer-facing products, "
            "a major disadvantage. Pages {pages}."
        ),
        typical_range="Optional arbitration; court available for IP and injunctive relief",
        negotiation_script=(
            "Can we make arbitration optional — either party can choose court — and "
            "preserve rights to seek injunctive relief in court for IP matters?"
        ),
    ),

    Rule(
        rule_id="SAAS_R007",
        name="Vendor can modify terms unilaterally",
        contract_types=["saas"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"modify\s+(the\s+)?(terms|agreement)",
            r"update\w*\s+(the\s+)?(terms|agreement)",
            r"change\s+these\s+terms",
            r"terms\s+may\s+change",
        ],
        plain_english="The vendor can change the contract terms later without your approval.",
        explanation_template=(
            "This agreement allows unilateral modification of terms. Without a "
            "material-changes-require-consent clause, rules can change mid-contract. Pages {pages}."
        ),
        typical_range="Material changes require 30 days notice + right to terminate",
        negotiation_script=(
            "Can we add that material changes to terms require 30 days written "
            "notice and give us the right to terminate without penalty if we "
            "don't accept them?"
        ),
    ),

    Rule(
        rule_id="SAAS_R008",
        name="Usage-based fees / overage charges",
        contract_types=["saas"],
        severity="MEDIUM",
        category="payment",
        detection_patterns=[
            r"overage\s+(fees|charges)",
            r"usage.?based",
            r"(additional|excess)\s+usage",
            r"exceeds?\s+(the\s+)?(limit|threshold)",
        ],
        plain_english="Costs can grow past your subscription tier if you hit usage limits.",
        explanation_template=(
            "Overage or usage-based fees apply. Review the unit rate carefully and "
            "set up usage alerts. A surprise overage bill is the #1 SaaS complaint. Pages {pages}."
        ),
        typical_range="Alerts at 75%/90%/100% of plan; overages billed monthly at disclosed rate",
        negotiation_script=(
            "Can we add automatic usage alerts at 75%, 90%, and 100% thresholds, "
            "and cap overage charges at 25% of the base subscription in any month?"
        ),
    ),

    Rule(
        rule_id="SAAS_R009",
        name="Security and compliance commitments",
        contract_types=["saas"],
        severity="LOW",
        category="data",
        detection_patterns=[
            r"security",
            r"encrypt\w+",
            r"\bsoc\s*2\b",
            r"\biso\s*27001\b",
            r"\bgdpr\b",
            r"\bhipaa\b",
        ],
        plain_english="Verify the vendor's security certifications match your needs.",
        explanation_template=(
            "Security terms referenced. For enterprise/regulated industries, "
            "require named standards: SOC 2 Type II, ISO 27001, GDPR, HIPAA "
            "as applicable to your data. Pages {pages}."
        ),
        typical_range="SOC 2 Type II + encryption at rest and in transit",
        negotiation_script=(
            "Can we confirm SOC 2 Type II compliance in writing, with annual "
            "attestations provided, plus encryption at rest and in transit?"
        ),
    ),

    Rule(
        rule_id="SAAS_R010",
        name="Termination and data retention",
        contract_types=["saas"],
        severity="MEDIUM",
        category="termination",
        detection_patterns=[
            r"terminat\w+\s+for\s+(convenience|cause)",
            r"upon\s+termination",
            r"termination\s+of\s+this\s+agreement",
            r"data\s+(deletion|retention)\s+(upon|after)",
        ],
        plain_english="Check what happens to your data and access on termination.",
        explanation_template=(
            "Termination terms are defined. Verify: (1) data export window "
            "(typically 30-90 days post-termination), (2) data deletion timeline, "
            "(3) notice periods for termination. Pages {pages}."
        ),
        typical_range="90 days data export window; certified deletion within 30 days after",
        negotiation_script=(
            "Can we secure a 90-day data export window post-termination, followed "
            "by certified deletion within 30 days? Standard for enterprise SaaS."
        ),
    ),
]