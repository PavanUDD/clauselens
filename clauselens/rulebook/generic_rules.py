"""Generic rulebook — catches universal red flags in ANY contract type.
Used as fallback when classifier returns 'unknown'.
"""
from __future__ import annotations
from clauselens.rulebook.schema import Rule

GENERIC_RULES: list[Rule] = [

    Rule(
        rule_id="GEN_R001",
        name="Auto-renewal clause",
        contract_types=["unknown"],
        severity="MEDIUM",
        category="renewal",
        detection_patterns=[
            r"auto.?renew\w*",
            r"automatically\s+renew",
            r"shall\s+renew",
            r"evergreen",
        ],
        plain_english="This contract may renew automatically — mark the cancellation deadline.",
        explanation_template=(
            "An auto-renewal clause is present on pages {pages}. Note the "
            "cancellation notice window carefully to avoid being locked in."
        ),
        typical_range="30-90 days advance written notice to opt out",
        negotiation_script=(
            "Can we change auto-renewal to require explicit written opt-in, or "
            "shorten the cancellation notice window?"
        ),
    ),

    Rule(
        rule_id="GEN_R002",
        name="One-sided termination rights",
        contract_types=["unknown"],
        severity="HIGH",
        category="termination",
        detection_patterns=[
            r"terminat\w+\s+at\s+any\s+time",
            r"terminat\w+\s+without\s+cause",
            r"terminat\w+\s+for\s+convenience",
            r"sole\s+discretion\s+to\s+terminat",
        ],
        plain_english="One party can end the contract whenever they want — check if it's mutual.",
        explanation_template=(
            "Termination rights appear asymmetric. Verify that termination rights, "
            "notice periods, and post-termination obligations are reciprocal. Pages {pages}."
        ),
        typical_range="Mutual termination rights with equivalent notice periods",
        negotiation_script=(
            "Can we make termination rights mutual, with the same notice period "
            "for both parties?"
        ),
    ),

    Rule(
        rule_id="GEN_R003",
        name="Indemnification clause",
        contract_types=["unknown"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"indemnif\w+",
            r"hold\s+harmless",
            r"defend\s+and\s+indemnif\w+",
        ],
        plain_english="You may have to defend the other party against lawsuits at your own cost.",
        explanation_template=(
            "An indemnification clause is present on pages {pages}. These can "
            "create unlimited third-party liability. Verify it's mutual and capped."
        ),
        typical_range="Mutual indemnification, capped at contract value or insurance limits",
        negotiation_script=(
            "Can we make indemnification mutual and cap it at either the contract "
            "value or available insurance limits?"
        ),
    ),

    Rule(
        rule_id="GEN_R004",
        name="Unlimited liability exposure",
        contract_types=["unknown"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"unlimited\s+liabilit",
            r"fully\s+liable",
            r"without\s+limit\w+",
            r"all\s+damages\s+arising",
        ],
        plain_english="Your financial exposure under this contract has no cap.",
        explanation_template=(
            "Unlimited-liability language is present on pages {pages}. This is "
            "rare in modern contracts and highly unfavorable."
        ),
        typical_range="Liability capped at contract value or 12 months of fees",
        negotiation_script=(
            "Can we cap liability at the greater of 12 months of fees paid or "
            "the total contract value? Unlimited liability is unusual."
        ),
    ),

    Rule(
        rule_id="GEN_R005",
        name="Waiver of consequential damages",
        contract_types=["unknown"],
        severity="MEDIUM",
        category="legal",
        detection_patterns=[
            r"no\s+consequential\s+damages",
            r"exclud\w+\s+consequential",
            r"in\s+no\s+event\s+shall",
            r"(lost\s+profits|loss\s+of\s+profits)",
        ],
        plain_english="If something goes wrong, you may not be able to recover indirect losses.",
        explanation_template=(
            "Consequential-damages waiver is present on pages {pages}. You lose "
            "the right to recover things like lost profits or business interruption."
        ),
        typical_range="Mutual waiver; exceptions for IP infringement and confidentiality breach",
        negotiation_script=(
            "Can we make the consequential-damages waiver mutual, and carve out "
            "exceptions for IP infringement and confidentiality breaches?"
        ),
    ),

    Rule(
        rule_id="GEN_R006",
        name="Broad confidentiality obligations",
        contract_types=["unknown"],
        severity="LOW",
        category="confidentiality",
        detection_patterns=[
            r"confidentialit\w+",
            r"non.?disclosure",
            r"proprietary\s+information",
            r"trade\s+secret",
        ],
        plain_english="Confidentiality obligations are present — verify scope and duration.",
        explanation_template=(
            "NDA obligations found on pages {pages}. Verify duration (perpetual "
            "NDAs are often unenforceable for non-trade-secret info)."
        ),
        typical_range="2-5 years for general info; perpetual only for trade secrets",
        negotiation_script=(
            "Can we limit confidentiality obligations to 3 years for general "
            "information, with perpetual coverage only for defined trade secrets?"
        ),
    ),

    Rule(
        rule_id="GEN_R007",
        name="Mandatory arbitration",
        contract_types=["unknown"],
        severity="MEDIUM",
        category="legal",
        detection_patterns=[
            r"binding\s+arbitration",
            r"mandatory\s+arbitration",
            r"submit\s+to\s+arbitration",
        ],
        plain_english="Disputes must go to private arbitration — you can't sue in court.",
        explanation_template=(
            "Mandatory arbitration is specified on pages {pages}. Arbitration "
            "limits court access and often class-action rights."
        ),
        typical_range="Optional arbitration; court available for IP and injunctive relief",
        negotiation_script=(
            "Can we make arbitration optional and preserve court access for "
            "IP matters and injunctive relief?"
        ),
    ),

    Rule(
        rule_id="GEN_R008",
        name="Jury trial waiver",
        contract_types=["unknown"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"waive\w*\s+(the\s+)?right\s+to\s+(a\s+)?jury\s+trial",
            r"waiver\s+of\s+jury\s+trial",
            r"no\s+jury\s+trial",
        ],
        plain_english="You give up your right to have a jury decide any dispute.",
        explanation_template=(
            "A jury-trial waiver is on pages {pages}. Disputes would be decided "
            "by a judge only, which typically favors the more sophisticated party."
        ),
        typical_range="Jury trial rights preserved",
        negotiation_script=(
            "I'm not comfortable waiving jury-trial rights. Can we remove this clause?"
        ),
    ),

    Rule(
        rule_id="GEN_R009",
        name="Governing law and venue",
        contract_types=["unknown"],
        severity="LOW",
        category="legal",
        detection_patterns=[
            r"governing\s+law",
            r"jurisdiction\s+(of|in)",
            r"laws\s+of\s+the\s+state\s+of",
            r"venue\s+(shall|will)\s+be",
        ],
        plain_english="Check which state's laws apply and where you'd have to fight a lawsuit.",
        explanation_template=(
            "Governing law and venue are specified on pages {pages}. If the "
            "chosen state is across the country from you, lawsuits become expensive."
        ),
        typical_range="Governing law of your home state or a neutral commercial state",
        negotiation_script=(
            "Can we change governing law and venue to my home state, or at "
            "minimum a neutral state like Delaware?"
        ),
    ),

    Rule(
        rule_id="GEN_R010",
        name="Assignment of the contract",
        contract_types=["unknown"],
        severity="MEDIUM",
        category="legal",
        detection_patterns=[
            r"assign\w*\s+(this\s+)?(agreement|contract)",
            r"assignment\s+of\s+(this\s+)?(agreement|rights)",
            r"transfer\s+(this\s+)?(agreement|contract)",
        ],
        plain_english="The other party may be able to transfer this contract to someone else.",
        explanation_template=(
            "Assignment provisions are on pages {pages}. Without consent requirements, "
            "the counterparty can transfer the contract to an entity you don't know."
        ),
        typical_range="Assignment requires written consent, not unreasonably withheld",
        negotiation_script=(
            "Can we add that assignment requires the other party's written consent, "
            "not to be unreasonably withheld?"
        ),
    ),

    Rule(
        rule_id="GEN_R011",
        name="Non-compete restriction",
        contract_types=["unknown"],
        severity="HIGH",
        category="restriction",
        detection_patterns=[
            r"non.?compete",
            r"shall\s+not\s+compete",
            r"restrictive\s+covenant",
            r"competing\s+business",
        ],
        plain_english="This contract may restrict your future business or employment.",
        explanation_template=(
            "A non-compete clause is on pages {pages}. Overly broad non-competes "
            "are often unenforceable, but can still chill business activity."
        ),
        typical_range="6-12 months, limited geographic area, specific competing activities",
        negotiation_script=(
            "Can we narrow the non-compete to 6-12 months within a specific "
            "geographic area and limited to directly competing products/services?"
        ),
    ),

    Rule(
        rule_id="GEN_R012",
        name="Force majeure clause",
        contract_types=["unknown"],
        severity="LOW",
        category="legal",
        detection_patterns=[
            r"force\s+majeure",
            r"acts?\s+of\s+god",
            r"beyond\s+(the\s+)?(reasonable\s+)?control",
        ],
        plain_english="Neither side is liable for events outside their control (disasters, war, etc.).",
        explanation_template=(
            "A force-majeure clause is present on pages {pages}. Verify it explicitly "
            "covers pandemics and is mutual — post-2020 standard."
        ),
        typical_range="Mutual force-majeure including pandemics and government actions",
        negotiation_script=(
            "Can we make the force-majeure clause explicitly mutual and include "
            "pandemics, government actions, and cyber events in the list?"
        ),
    ),
]