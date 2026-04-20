"""Rental agreement rulebook — 18 rules covering the most common red flags."""
from __future__ import annotations
from clauselens.rulebook.schema import Rule

RENTAL_RULES: list[Rule] = [

    Rule(
        rule_id="RENTAL_R001",
        name="Excessive early termination penalty",
        contract_types=["rental"],
        severity="HIGH",
        category="termination",
        detection_patterns=[
            r"early\s+terminat\w+",
            r"break\s+(the\s+)?lease",
            r"terminat\w+\s+before\s+the\s+end",
            r"liquidated\s+damages",
            r"early\s+move.?out",
        ],
        semantic_queries=["penalty for leaving the lease early", "break lease fee"],
        plain_english="You may owe a large penalty if you leave before the lease ends.",
        explanation_template=(
            "This lease includes an early termination penalty. Typical leases "
            "charge 1 month's rent OR forfeit the deposit — not both. Review "
            "Section(s) on pages {pages} before signing."
        ),
        typical_range="1 month rent OR forfeit deposit",
        negotiation_script=(
            "Hi, I noticed the early termination clause requires a significant penalty. "
            "Industry standard is typically 1 month's rent or forfeiture of deposit, not both. "
            "Could we revise this to 1 month's rent as a more balanced term?"
        ),
        learn_more="Many state tenant laws cap early-termination fees.",
    ),

    Rule(
        rule_id="RENTAL_R002",
        name="Non-refundable security deposit",
        contract_types=["rental"],
        severity="HIGH",
        category="deposit",
        detection_patterns=[
            r"non.?refundable\s+(security\s+)?deposit",
            r"deposit\s+shall\s+not\s+be\s+refunded",
            r"deposit\s+is\s+forfeited",
        ],
        semantic_queries=["security deposit not refundable"],
        plain_english="Your security deposit cannot be returned under any circumstance.",
        explanation_template=(
            "This contract marks the security deposit as non-refundable. In most US "
            "states, deposits must be refundable minus actual damages. This clause "
            "may be unenforceable in your state."
        ),
        typical_range="Refundable minus documented damages",
        negotiation_script=(
            "I noticed the security deposit is listed as non-refundable. In most states, "
            "deposits must be refundable minus documented damages. Could we revise this "
            "to match standard practice?"
        ),
        learn_more="HUD guidance requires itemized deductions for deposit retention.",
    ),

    Rule(
        rule_id="RENTAL_R003",
        name="Automatic lease renewal",
        contract_types=["rental"],
        severity="MEDIUM",
        category="renewal",
        detection_patterns=[
            r"auto.?renew\w*",
            r"automatically\s+renew",
            r"shall\s+renew\s+for",
            r"evergreen",
            r"renewed\s+automatically",
        ],
        semantic_queries=["lease automatically renews"],
        plain_english="Your lease renews automatically unless you give notice in time.",
        explanation_template=(
            "This lease auto-renews. If you forget to send notice by the required "
            "deadline, you may be locked into another full term."
        ),
        typical_range="Month-to-month after initial term, OR requires opt-in renewal",
        negotiation_script=(
            "Can we change the auto-renewal to a month-to-month conversion after the "
            "initial term, or require explicit written opt-in for renewal?"
        ),
    ),

    Rule(
        rule_id="RENTAL_R004",
        name="Landlord entry without notice",
        contract_types=["rental"],
        severity="HIGH",
        category="privacy",
        detection_patterns=[
            r"access\s+by\s+landlord",
            r"landlord'?s?\s+right\s+to\s+enter",
            r"right\s+of\s+entry",
            r"reasonable\s+access\s+to\s+the\s+premises",
            r"enter\s+the\s+premises\s+(at|for|to)",
            r"inspect\s+the\s+premises",
            r"landlord\s+may\s+enter",
        ],
        semantic_queries=["landlord access to premises without notice"],
        plain_english="The landlord can enter your home — check notice requirements.",
        explanation_template=(
            "This lease has a landlord-entry clause (pages {pages}). Most states "
            "require at least 24 hours written notice except in emergencies. Verify "
            "what notice this clause requires."
        ),
        typical_range="24-48 hours written notice, except emergencies",
        negotiation_script=(
            "I'd like to add a 24-hour written notice requirement for non-emergency "
            "landlord entry, which matches state law in most jurisdictions."
        ),
    ),

    Rule(
        rule_id="RENTAL_R005",
        name="No subletting allowed",
        contract_types=["rental"],
        severity="LOW",
        category="restriction",
        detection_patterns=[
            r"sublet\w*",
            r"sub.?let\w*",
            r"sub.?leas\w*",
            r"assignment\s+and\s+sub",
            r"assign\s+this\s+(lease|agreement)",
            r"assignment\s+of\s+(this\s+)?(lease|agreement)",
        ],
        semantic_queries=["cannot sublet the apartment"],
        plain_english="Subletting or assignment is restricted — read the terms.",
        explanation_template=(
            "This lease addresses subletting and assignment (pages {pages}). Verify "
            "whether it's fully prohibited or allowed with landlord consent. If plans "
            "change, you may not be able to transfer the lease."
        ),
        typical_range="Allowed with landlord approval",
        negotiation_script=(
            "Could we change this to 'sublet allowed with landlord's written consent, "
            "not to be unreasonably withheld'? That's the standard balanced clause."
        ),
    ),

    Rule(
        rule_id="RENTAL_R006",
        name="Tenant pays all repairs",
        contract_types=["rental"],
        severity="HIGH",
        category="maintenance",
        detection_patterns=[
            r"tenant\s+(shall|is|will)\s+(be\s+)?responsible\s+for\s+all\s+repairs",
            r"tenant\s+pays\s+for\s+all\s+maintenance",
            r"all\s+repairs\s+at\s+tenant'?s?\s+expense",
        ],
        semantic_queries=["tenant responsible for all repairs"],
        plain_english="You pay for every repair — even major ones like plumbing or roof.",
        explanation_template=(
            "This clause makes the tenant responsible for all repairs. Typically "
            "landlords cover structural, plumbing, electrical, and major systems."
        ),
        typical_range="Tenant: minor upkeep only. Landlord: structural + major systems.",
        negotiation_script=(
            "Standard leases split repair responsibility: tenant handles minor upkeep, "
            "landlord handles major systems (plumbing, electrical, HVAC, structural). "
            "Can we adopt that split?"
        ),
    ),

    Rule(
        rule_id="RENTAL_R007",
        name="Aggressive late fees",
        contract_types=["rental"],
        severity="MEDIUM",
        category="payment",
        detection_patterns=[
            r"late\s+fee",
            r"late\s+charge",
            r"interest\s+on\s+(unpaid|late)",
            r"\d+\s*%\s+per\s+(day|month)",
        ],
        semantic_queries=["late payment fee amount"],
        plain_english="The late fee for missed rent may be unusually high.",
        explanation_template=(
            "This contract contains late fees. Typical late fees are 5% of monthly rent. "
            "Fees above 10% or daily compounding interest may be unenforceable in your state."
        ),
        typical_range="~5% of monthly rent",
        negotiation_script=(
            "Can we cap the late fee at 5% of monthly rent with a 5-day grace period? "
            "That's standard practice."
        ),
    ),

    Rule(
        rule_id="RENTAL_R008",
        name="Large rent increase allowed",
        contract_types=["rental"],
        severity="MEDIUM",
        category="payment",
        detection_patterns=[
            r"landlord\s+may\s+increase\s+(the\s+)?rent",
            r"rent\s+may\s+be\s+(increased|adjusted|raised)",
            r"adjust\w+\s+(the\s+)?rent\s+(upward|annually)",
            r"annual\s+rent\s+increase",
            r"rent\s+shall\s+increase",
        ],
        semantic_queries=["rent can increase annually"],
        plain_english="The landlord can raise rent — check the cap and notice period.",
        explanation_template=(
            "This lease permits the landlord to increase rent (possibly after initial "
            "term or on renewal). Typical increases are 3-8% annually. Verify the cap "
            "and notice period — above 10%/year or under 60 days notice is aggressive."
        ),
        typical_range="3-8% annually with 60 days written notice",
        negotiation_script=(
            "Can we cap annual rent increases at 8% with 60 days written notice? That "
            "matches typical residential lease terms."
        ),
    ),

    Rule(
        rule_id="RENTAL_R009",
        name="No pets clause",
        contract_types=["rental"],
        severity="LOW",
        category="restriction",
        detection_patterns=[
            r"no\s+pets",
            r"pets\s+are\s+(not\s+)?prohibited",
            r"no\s+animals",
            r"there\s+will\s+be\s+no\s+animals",
        ],
        semantic_queries=["pets not allowed"],
        plain_english="Pets are not allowed at this property.",
        explanation_template=(
            "A no-pets clause is common but worth noting if you have or plan to have pets. "
            "Service animals are typically protected by federal law regardless of this clause."
        ),
        typical_range="Common — many landlords charge a pet deposit instead",
        negotiation_script=(
            "Would you consider allowing pets with an additional refundable pet deposit "
            "(typically $200-500)?"
        ),
    ),

    Rule(
        rule_id="RENTAL_R010",
        name="Tenant waives right to jury trial",
        contract_types=["rental"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"waive\w*\s+(the\s+)?right\s+to\s+(a\s+)?jury\s+trial",
            r"waiver\s+of\s+jury\s+trial",
            r"no\s+jury\s+trial",
        ],
        semantic_queries=["waive jury trial rights"],
        plain_english="You give up your right to a jury trial if there's a dispute.",
        explanation_template=(
            "This lease waives your right to a jury trial. Disputes would be resolved "
            "by a judge or arbitrator only. This generally favors the landlord."
        ),
        typical_range="Jury trial rights preserved",
        negotiation_script=(
            "I'm not comfortable waiving my right to a jury trial. Can we remove this "
            "clause? Standard leases preserve this right."
        ),
    ),

    Rule(
        rule_id="RENTAL_R011",
        name="Mandatory arbitration",
        contract_types=["rental"],
        severity="MEDIUM",
        category="legal",
        detection_patterns=[
            r"binding\s+arbitration",
            r"mandatory\s+arbitration",
            r"submit\s+to\s+arbitration",
            r"arbitration\s+shall\s+be\s+the\s+(sole|exclusive)",
        ],
        semantic_queries=["disputes resolved by arbitration"],
        plain_english="Disputes must go to private arbitration — not court.",
        explanation_template=(
            "This lease requires arbitration for disputes. Arbitration is private, often "
            "costs less, but you give up access to courts and class action rights."
        ),
        typical_range="Optional / court available",
        negotiation_script=(
            "Can we make arbitration optional rather than mandatory, so either party can "
            "choose court or arbitration?"
        ),
    ),

    Rule(
        rule_id="RENTAL_R012",
        name="Attorney's fees clause",
        contract_types=["rental"],
        severity="MEDIUM",
        category="legal",
        detection_patterns=[
            r"attorney'?s?\s+fees",
            r"legal\s+fees",
            r"court\s+costs",
            r"reasonable\s+attorneys?\s+fees",
            r"prevailing\s+party",
            r"costs\s+of\s+collection",
        ],
        semantic_queries=["tenant pays attorney fees if sued"],
        plain_english="Check who pays legal fees if there's a dispute.",
        explanation_template=(
            "This lease addresses attorney's fees (pages {pages}). A fair clause is "
            "'prevailing party' — whoever wins gets fees. A one-sided tenant-pays-landlord "
            "clause is tenant-unfavorable. Read carefully."
        ),
        typical_range="'Prevailing party' clause (mutual)",
        negotiation_script=(
            "Can we make this a 'prevailing party' clause — whoever wins gets legal fees? "
            "One-sided clauses aren't standard."
        ),
    ),

    Rule(
        rule_id="RENTAL_R013",
        name="Large security deposit required",
        contract_types=["rental"],
        severity="MEDIUM",
        category="deposit",
        detection_patterns=[
            r"security\s+deposit",
            r"damage\s+deposit",
        ],
        semantic_queries=["security deposit amount"],
        plain_english="Check the security deposit amount — it should typically be 1-2 months rent.",
        explanation_template=(
            "This lease requires a security deposit. Typical deposits are 1-2 months rent. "
            "Deposits above 2 months are aggressive and may be capped by state law."
        ),
        typical_range="1-2 months rent",
        negotiation_script=(
            "Could we reduce the security deposit to 1 month's rent? Most states cap "
            "deposits at 2 months, and 1 month is standard."
        ),
    ),

    Rule(
        rule_id="RENTAL_R014",
        name="Utilities included / excluded — check carefully",
        contract_types=["rental"],
        severity="LOW",
        category="payment",
        detection_patterns=[
            r"utilit(y|ies)",
            r"electric\w*\s+(and|,)\s+(water|gas)",
            r"tenant\s+(shall|is)\s+responsible\s+for\s+(all\s+)?utilit",
        ],
        semantic_queries=["who pays utilities"],
        plain_english="Verify which utilities you must pay separately — it adds up.",
        explanation_template=(
            "This lease addresses utilities. Confirm exactly which utilities (water, gas, "
            "electric, internet, trash) are included in rent and which you pay."
        ),
        typical_range="Varies — water/trash often included, electric/gas often not",
        negotiation_script=(
            "Can you clarify in writing exactly which utilities are included in the rent "
            "and which I'm responsible for? I'd like to budget accurately."
        ),
    ),

    Rule(
        rule_id="RENTAL_R015",
        name="No guest policy / restrictions on visitors",
        contract_types=["rental"],
        severity="LOW",
        category="restriction",
        detection_patterns=[
            r"no\s+overnight\s+guest",
            r"guest\s+(shall|may)\s+not\s+stay",
            r"limit\w+\s+(on\s+)?guest",
            r"visitor\s+(shall|may)\s+not",
        ],
        semantic_queries=["restrictions on overnight guests"],
        plain_english="There are restrictions on who can stay with you.",
        explanation_template=(
            "This lease restricts guests or visitors. Verify the allowed duration "
            "(e.g., 7 or 14 nights) so you're not in violation for normal visits."
        ),
        typical_range="No restriction, or 7-14 consecutive nights",
        negotiation_script=(
            "Can we revise this to allow guests for up to 14 consecutive nights without "
            "requiring permission? That matches standard practice."
        ),
    ),

    Rule(
        rule_id="RENTAL_R016",
        name="Joint and several liability",
        contract_types=["rental"],
        severity="MEDIUM",
        category="legal",
        detection_patterns=[
            r"joint\s+and\s+several\s+liabilit",
            r"jointly\s+and\s+severally\s+liable",
        ],
        semantic_queries=["all tenants responsible for full rent"],
        plain_english="If your roommate doesn't pay, you're on the hook for the full rent.",
        explanation_template=(
            "Joint-and-several liability means any one tenant can be held responsible for "
            "the ENTIRE rent and damages, not just their share. Common but risky with roommates."
        ),
        typical_range="Common in multi-tenant leases — know the risk",
        negotiation_script=(
            "Can we change this to 'several liability' — each tenant only responsible "
            "for their share — or require a co-signer rather than making roommates liable?"
        ),
    ),

    Rule(
        rule_id="RENTAL_R017",
        name="Move-out cleaning fee",
        contract_types=["rental"],
        severity="LOW",
        category="deposit",
        detection_patterns=[
            r"cleaning\s+fee",
            r"move.?out\s+(cleaning|fee)",
            r"professional\s+cleaning\s+(required|shall)",
        ],
        semantic_queries=["mandatory cleaning fee at move out"],
        plain_english="There may be a mandatory cleaning fee when you leave.",
        explanation_template=(
            "This lease charges a move-out cleaning fee. Many states require this to be "
            "an actual cost, not a flat fee, and it should come from the deposit only if justified."
        ),
        typical_range="Actual documented cleaning cost only",
        negotiation_script=(
            "Can we specify that cleaning charges be based on actual documented costs "
            "rather than a flat mandatory fee?"
        ),
    ),

    Rule(
        rule_id="RENTAL_R018",
        name="Holdover tenancy penalty",
        contract_types=["rental"],
        severity="MEDIUM",
        category="termination",
        detection_patterns=[
            r"hold.?over",
            r"holding\s+over",
            r"remain\s+in\s+possession\s+(after|beyond)",
            r"tenancy\s+at\s+sufferance",
        ],
        semantic_queries=["staying past lease end penalty"],
        plain_english="If you stay past the lease end, you may owe significantly higher rent.",
        explanation_template=(
            "This lease has a holdover clause. If you remain after the termination date, "
            "you may be charged elevated rent (often 1.5x-2x) or face eviction. Plan your "
            "move-out date carefully."
        ),
        typical_range="Month-to-month at original rent, or modest holdover premium",
        negotiation_script=(
            "Can we cap holdover rent at the original monthly amount, or set it to "
            "month-to-month tenancy terms rather than a penalty rate?"
        ),
    ),
]