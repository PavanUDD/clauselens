"""Vendor / Master Service Agreement rulebook — 15 rules covering the most
critical red flags for IT staffing and consulting firms signing MSAs. Expanding to all small businesses."""
from __future__ import annotations
from clauselens.rulebook.schema import Rule

VENDOR_RULES: list[Rule] = [

    Rule(
        rule_id="VENDOR_R001",
        name="Termination for convenience — no payment owed",
        contract_types=["vendor"],
        severity="HIGH",
        category="termination",
        detection_patterns=[
            r"terminat\w+\s+for\s+convenience",
            r"terminat\w+\s+at\s+(any\s+time|its\s+sole\s+discretion)",
            r"terminat\w+\s+without\s+cause",
            r"cancel\w+\s+(this\s+agreement\s+)?at\s+any\s+time",
            r"terminat\w+\s+upon\s+\d+\s+(hours?|days?)\s+notice",
        ],
        semantic_queries=["client can terminate contract anytime without paying"],
        plain_english="The client can cancel anytime — and may owe you nothing for work in progress.",
        explanation_template=(
            "This MSA allows termination for convenience. If the client cancels, "
            "you may not be compensated for completed but uninvoiced work, work in "
            "progress, or preparation costs. Typical fair MSAs require 30 days notice "
            "AND payment for all work completed through termination date."
        ),
        typical_range="30 days written notice + payment for all work completed to date",
        negotiation_script=(
            "Can we add language that on termination for convenience, Client pays "
            "for all work completed and reasonable costs incurred through the "
            "termination date, plus a 30-day wind-down period?"
        ),
        learn_more="Termination for convenience clauses are standard but the payment terms on exit are negotiable.",
        safe_harbor_patterns=[
            r"pay\w+\s+for\s+all\s+work\s+completed",
            r"compensat\w+\s+for\s+work\s+in\s+progress",
            r"fees\s+(earned|incurred)\s+(through|prior\s+to)\s+terminat",
        ],
        safe_harbor_skips=False,
        safe_harbor_note=(
            "✅ This termination clause includes payment for completed work. "
            "Verify the notice period and wind-down terms are reasonable."
        ),
    ),

    Rule(
        rule_id="VENDOR_R002",
        name="Extended payment terms — Net 60 or longer",
        contract_types=["vendor"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"net\s*6[0-9]",
            r"net\s*[7-9]\d",
            r"net\s*1[0-9]\d",
            r"within\s+6[0-9]\s+days",
            r"within\s+[7-9]\d\s+days",
            r"60\s+(calendar\s+)?days\s+(of|from|after)\s+(invoice|receipt)",
            r"90\s+(calendar\s+)?days\s+(of|from|after)\s+(invoice|receipt)",
        ],
        semantic_queries=["payment terms 60 days 90 days after invoice"],
        plain_english="You may wait 60-90+ days to get paid — a serious cash flow risk.",
        explanation_template=(
            "This contract requires Net 60 or longer payment terms. Combined with a "
            "90-day dispute window, you could wait 150+ days to receive payment. "
            "Standard for small vendors is Net 30. Net 60+ is aggressive and creates "
            "real cash flow risk."
        ),
        typical_range="Net 30 from invoice date",
        negotiation_script=(
            "Can we change payment terms to Net 30? I'm a small business and "
            "Net 60+ creates serious cash flow challenges. I'm happy to offer "
            "a 2% discount for payment within 15 days as an incentive."
        ),
        safe_harbor_patterns=[
            r"net\s*[12]\d(?!\d)",
            r"within\s+[12]\d\s+days",
            r"net\s*30",
        ],
        safe_harbor_skips=True,
    ),

    Rule(
        rule_id="VENDOR_R003",
        name="Long dispute window blocks payment",
        contract_types=["vendor"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"dispute\w*\s+(invoice|payment).{0,60}(60|90|120)\s+days",
            r"(60|90|120)\s+days.{0,40}(dispute|object|contest)",
            r"withhold\w*\s+payment\s+(during|pending|while)",
            r"dispute\w*\s+(period|window)\s+of\s+(60|90|120)",
            r"contest\w*\s+(any\s+)?invoice\s+within\s+(60|90|120)",
        ],
        semantic_queries=["client can dispute invoice for 90 days and withhold payment"],
        plain_english="The client can dispute your invoice for up to 90 days and withhold all payment during that time.",
        explanation_template=(
            "This MSA allows the client to dispute invoices for an extended period "
            "while withholding full payment. A 60-90 day dispute window on top of "
            "Net 60 terms means you could wait 5+ months to get paid. "
            "Standard dispute windows are 15-30 days."
        ),
        typical_range="15-30 days to dispute, payment of undisputed amounts within terms",
        negotiation_script=(
            "Can we shorten the dispute window to 15 days and require payment of "
            "undisputed invoice amounts within standard terms, even while a partial "
            "dispute is pending? Withholding full payment during disputes is unfair."
        ),
    ),

    Rule(
        rule_id="VENDOR_R004",
        name="Unlimited IP assignment including pre-existing work",
        contract_types=["vendor"],
        severity="HIGH",
        category="ip",
        detection_patterns=[
            r"all\s+work\s+product.{0,60}(exclusively|sole)\s+(property|ownership)",
            r"assign\w+.{0,40}all\s+(right|title|interest)",
            r"pre.?existing\s+(ip|tools?|frameworks?|code|software).{0,60}(assign|transfer|belong)",
            r"including.{0,30}pre.?existing",
            r"background\s+(ip|intellectual\s+property).{0,40}(assign|transfer|grant)",
            r"perpetually\s+irrevocably\s+assign",
        ],
        semantic_queries=["vendor assigns all IP including pre-existing tools to client"],
        plain_english="The client claims ownership of your pre-existing tools, code, and frameworks — not just the work you do for them.",
        explanation_template=(
            "This MSA sweeps in pre-existing intellectual property. If you use your "
            "own frameworks, code libraries, or tools in the project, this clause "
            "could transfer ownership of those to the client. You could lose the "
            "right to use your own tools on future projects."
        ),
        typical_range="Client owns deliverables only. Vendor retains pre-existing IP with license grant.",
        negotiation_script=(
            "Can we carve out pre-existing IP? I retain ownership of all tools, "
            "frameworks, and code I developed prior to this engagement. "
            "You receive a perpetual license to use them as incorporated in "
            "the deliverables, but I retain the underlying IP."
        ),
        safe_harbor_patterns=[
            r"background\s+ip\s+remains.{0,30}(vendor|contractor|supplier)",
            r"pre.?existing\s+ip.{0,40}(retain|remain|exclude)",
            r"license\s+to\s+(use|incorporate).{0,40}pre.?existing",
        ],
        safe_harbor_skips=True,
    ),

    Rule(
        rule_id="VENDOR_R005",
        name="Liability cap below contract value",
        contract_types=["vendor"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"limitation\s+of\s+liability",
            r"limit\w+\s+of\s+liabilit",
            r"liabilit\w+\s+(shall\s+not\s+exceed|capped?\s+at|limited\s+to)",
            r"maximum\s+liabilit\w+\s+(shall\s+be|is|of)",
            r"aggregate\s+liabilit\w+\s+(shall\s+not|capped?|limited)",
            r"liabilit\w+\s+cap",
        ],
        semantic_queries=["liability limited to amount paid in last 3 months"],
        plain_english="Your liability is capped — but verify the cap is fair relative to contract value.",
        explanation_template=(
            "This MSA includes a liability cap. Check whether it applies equally "
            "to both parties. A cap of '3 months fees' on a $500K project means "
            "you could be liable for far more than you earned. "
            "Most fair MSAs cap liability at total fees paid under the contract."
        ),
        typical_range="Mutual cap at total fees paid, or 12 months fees for each party",
        negotiation_script=(
            "Can we make the liability cap mutual and set it at total fees paid "
            "under this agreement? A one-sided cap or a cap lower than contract "
            "value creates disproportionate risk."
        ),
        safe_harbor_patterns=[
            r"mutual\w*\s+(limitation|cap|liabilit)",
            r"each\s+party.{0,40}liabilit\w+.{0,40}(cap|limit|exceed)",
        ],
        safe_harbor_skips=False,
        safe_harbor_note=(
            "✅ Liability cap appears mutual. Verify the cap amount is reasonable "
            "relative to the contract value."
        ),
    ),

    Rule(
        rule_id="VENDOR_R006",
        name="Broad indemnification — vendor bears all risk",
        contract_types=["vendor"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"vendor\s+shall\s+indemnif",
            r"supplier\s+shall\s+indemnif",
            r"contractor\s+shall\s+indemnif",
            r"indemnif\w+\s+(and\s+hold\s+harmless|defend).{0,60}(any\s+and\s+all|all\s+claims)",
            r"indemnif\w+\s+(client|company|customer)\s+from\s+any",
            r"third.?party\s+claims?.{0,60}indemnif",
        ],
        semantic_queries=["vendor must indemnify client from all third party claims"],
        plain_english="You may be responsible for indemnifying the client against virtually any third-party claim.",
        explanation_template=(
            "This indemnification clause could make you responsible for the client's "
            "legal costs on any third-party claim related to your work — even if "
            "the claim isn't your fault. Broad indemnification clauses are a "
            "significant financial risk for small vendors."
        ),
        typical_range="Mutual indemnification limited to each party's own negligence or breach",
        negotiation_script=(
            "Can we limit indemnification to claims arising directly from our own "
            "gross negligence or willful misconduct, and make it mutual? "
            "I can't indemnify you against claims that aren't caused by my actions."
        ),
        safe_harbor_patterns=[
            r"mutual\w*\s+indemnif",
            r"each\s+party\s+shall\s+indemnif",
            r"solely\s+(caused\s+by|arising\s+from).{0,30}(negligence|breach|misconduct)",
            r"gross\s+negligence\s+or\s+willful\s+misconduct",
        ],
        safe_harbor_skips=False,
        safe_harbor_note=(
            "✅ Indemnification appears limited to negligence or misconduct. "
            "Verify it is mutual and not one-sided."
        ),
    ),

    Rule(
        rule_id="VENDOR_R007",
        name="Non-compete restricts future client work",
        contract_types=["vendor"],
        severity="HIGH",
        category="restriction",
        detection_patterns=[
            r"shall\s+not\s+(provide|perform|offer)\s+(similar\s+)?services.{0,60}(competi|industry|sector)",
            r"non.?compete.{0,60}(vendor|supplier|contractor)",
            r"(12|18|24|36)\s+months?.{0,40}(compet|similar\s+services|same\s+industry)",
            r"restrict\w+\s+from\s+(working|providing|offering).{0,40}(compet|similar)",
            r"exclusively\s+(work|provide|dedicated)\s+to\s+(client|company|customer)",
        ],
        semantic_queries=["vendor cannot work for competitors for months after contract"],
        plain_english="You may be restricted from working with similar clients — even after this contract ends.",
        explanation_template=(
            "This MSA restricts your ability to work with similar clients or in the "
            "same industry. For a vendor or consultant, this can severely limit your "
            "business. Post-contract non-competes for vendors are often unenforceable "
            "but costly to fight."
        ),
        typical_range="No post-contract restriction for vendors; non-solicitation of specific contacts only",
        negotiation_script=(
            "As a vendor, a non-compete would prevent me from running my business. "
            "Can we replace this with a narrow non-solicitation — I won't directly "
            "target your specific employees or clients — rather than a broad "
            "industry restriction?"
        ),
    ),

    Rule(
        rule_id="VENDOR_R008",
        name="Automatic renewal with long notice window",
        contract_types=["vendor"],
        severity="MEDIUM",
        category="renewal",
        detection_patterns=[
            r"auto.?renew\w*",
            r"automatically\s+renew",
            r"renew\w*\s+for\s+(additional|successive|another)",
            r"evergreen\s+(clause|term|renewal)",
            r"unless\s+(either\s+party|written\s+notice).{0,40}(cancel|terminat|non.?renew)",
        ],
        semantic_queries=["contract renews automatically unless notice given"],
        plain_english="This MSA auto-renews — you could be locked in for another full term if you miss the notice window.",
        explanation_template=(
            "This MSA renews automatically. If the notice window to cancel is "
            "90-180 days, you must plan cancellation far in advance. Missing "
            "the window locks you into another full term."
        ),
        typical_range="30 days notice to cancel before renewal, or mutual written opt-in",
        negotiation_script=(
            "Can we change the auto-renewal to require affirmative written consent "
            "from both parties, or reduce the cancellation notice window to 30 days?"
        ),
        safe_harbor_patterns=[
            r"30\s+days?.{0,20}(notice|prior).{0,20}(cancel|non.?renew|terminat)",
            r"written\s+(consent|agreement)\s+(of\s+both|from\s+both)\s+parties",
        ],
        safe_harbor_skips=True,
    ),

    Rule(
        rule_id="VENDOR_R009",
        name="Unilateral contract modification",
        contract_types=["vendor"],
        severity="HIGH",
        category="terms",
        detection_patterns=[
            r"(client|company|customer)\s+(may|reserves?\s+the\s+right\s+to)\s+modify",
            r"(client|company|customer)\s+(may|can)\s+(amend|change|update)\s+(this\s+)?(agreement|terms|contract)",
            r"modif\w+\s+(terms|agreement|contract)\s+(at\s+any\s+time|unilaterally)",
            r"terms\s+may\s+be\s+updated\s+(at\s+any\s+time|without\s+notice)",
            r"right\s+to\s+change\s+(these\s+)?(terms|agreement)\s+at\s+any\s+time",
        ],
        semantic_queries=["client can change contract terms without vendor agreement"],
        plain_english="The client can change contract terms without your agreement — this undermines the entire contract.",
        explanation_template=(
            "This clause allows the client to modify contract terms unilaterally. "
            "This is a serious red flag — it means the terms you agreed to can "
            "change without your consent. All contract changes should require "
            "mutual written agreement."
        ),
        typical_range="All amendments require written consent of both parties",
        negotiation_script=(
            "Can we add language requiring mutual written consent for any "
            "modification to this agreement? Unilateral modification rights "
            "undermine the entire contract."
        ),
    ),

    Rule(
        rule_id="VENDOR_R010",
        name="Acceptance period delays payment trigger",
        contract_types=["vendor"],
        severity="MEDIUM",
        category="payment",
        detection_patterns=[
            r"acceptance\s+(period|review|testing|criteria)",
            r"accept\w+\s+(deliverable|work\s+product|milestone).{0,60}(trigger|start|begin)",
            r"payment\s+(due|triggered|start).{0,40}(acceptance|approved|sign.?off)",
            r"(30|60|90)\s+days?.{0,30}(accept|review|test|inspect)",
            r"deemed\s+accept\w+\s+(if|after|upon)",
        ],
        semantic_queries=["payment only triggered after client acceptance of deliverables"],
        plain_english="Payment doesn't start until the client formally accepts your work — they control the clock.",
        explanation_template=(
            "This MSA requires formal client acceptance before payment is triggered. "
            "If the acceptance period is long or undefined, the client controls "
            "when your payment clock starts. Combined with Net 60 terms, "
            "this can significantly delay payment."
        ),
        typical_range="10-15 day acceptance window; deemed accepted if no written objection",
        negotiation_script=(
            "Can we add a 'deemed acceptance' clause — deliverables are considered "
            "accepted if Client provides no written objection within 10 business days? "
            "This protects both parties and keeps the project moving."
        ),
        safe_harbor_patterns=[
            r"deemed\s+accept\w+.{0,40}(10|15|five|ten)\s+(business\s+)?days",
            r"no\s+written\s+objection.{0,30}(accept|deemed|consider)",
        ],
        safe_harbor_skips=True,
    ),

    Rule(
        rule_id="VENDOR_R011",
        name="Governing law in distant jurisdiction",
        contract_types=["vendor"],
        severity="MEDIUM",
        category="legal",
        detection_patterns=[
            r"govern\w+\s+(by\s+)?the\s+laws\s+of",
            r"jurisdiction\s+(shall\s+be|is\s+exclusively?)",
            r"venue\s+(shall\s+be|is)\s+(exclusively?|only)",
            r"disputes?.{0,40}(courts?\s+of|jurisdiction\s+of)",
            r"regardless\s+of\s+where.{0,40}(located|based|resid)",
        ],
        semantic_queries=["disputes must be resolved in different state or country"],
        plain_english="If there's a dispute, you may have to litigate in another state or country — at your own cost.",
        explanation_template=(
            "This MSA specifies a governing jurisdiction. If it's different from "
            "where you operate, any dispute requires you to hire out-of-state "
            "counsel and potentially travel. This is a real cost that favors "
            "the larger party."
        ),
        typical_range="Your home state, or mutual agreement to arbitration",
        negotiation_script=(
            "Can we change governing law to my home state, or agree to binding "
            "arbitration in a neutral location? Requiring me to litigate in "
            "your jurisdiction creates a financial disadvantage."
        ),
    ),

    Rule(
        rule_id="VENDOR_R012",
        name="Audit rights — excessive access to vendor records",
        contract_types=["vendor"],
        severity="MEDIUM",
        category="privacy",
        detection_patterns=[
            r"audit\s+(right|access).{0,60}(vendor|supplier|contractor)",
            r"(client|company|customer).{0,30}right\s+to\s+(audit|inspect|examine)",
            r"access\s+to\s+(vendor'?s?|supplier'?s?|contractor'?s?)\s+(books|records|financials)",
            r"inspect\w*\s+(books|records|financial\s+records|accounts)",
        ],
        semantic_queries=["client has right to audit vendor financial records"],
        plain_english="The client has the right to audit your books and financial records.",
        explanation_template=(
            "This MSA grants the client audit rights over your records. "
            "Verify the scope — broad audit rights can expose sensitive "
            "information about your other clients and pricing. "
            "Audit rights should be limited to records directly relevant "
            "to this engagement."
        ),
        typical_range="Audit rights limited to project-specific records only, with 30 days notice",
        negotiation_script=(
            "Can we limit audit rights to records directly related to this "
            "engagement only, with 30 days advance written notice, and at "
            "Client's expense? Broad financial audits aren't appropriate "
            "for a vendor relationship."
        ),
    ),

    Rule(
        rule_id="VENDOR_R013",
        name="Liquidated damages or penalty clauses",
        contract_types=["vendor"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"liquidated\s+damages",
            r"penalty\s+(clause|of\s+\$|for\s+(delay|late|missed))",
            r"\$[\d,]+\s+per\s+(day|week|hour).{0,30}(delay|late|miss)",
            r"(daily|weekly)\s+(penalty|charge|fee).{0,40}(delay|failure|breach)",
            r"service\s+credits?.{0,40}(SLA|uptime|delivery|deadline)",
        ],
        semantic_queries=["daily penalty for late delivery or missed deadlines"],
        plain_english="You face financial penalties for delays or missed deadlines — check the amounts and triggers.",
        explanation_template=(
            "This MSA includes liquidated damages or penalty clauses. "
            "Daily penalties for delays can quickly exceed the contract value. "
            "Verify the trigger conditions, penalty amounts, and whether "
            "there are force majeure protections."
        ),
        typical_range="Service credits only (not cash penalties); capped at monthly fees; force majeure protected",
        negotiation_script=(
            "Can we replace cash penalties with service credits capped at the "
            "monthly fee, and add force majeure protections for delays outside "
            "my control? Uncapped daily penalties create disproportionate risk."
        ),
    ),

    Rule(
        rule_id="VENDOR_R014",
        name="Non-solicitation of vendor's employees",
        contract_types=["vendor"],
        severity="MEDIUM",
        category="restriction",
        detection_patterns=[
            r"(client|company|customer).{0,40}shall\s+not\s+solicit",
            r"non.?solicit\w+.{0,40}(employ|staff|personnel|team)",
            r"solicit\w+\s+(or\s+hire|or\s+recruit).{0,40}(vendor|supplier|contractor)",
            r"hire\s+(away|directly).{0,40}(vendor|supplier|contractor).{0,30}(employ|staff|personnel)",
        ],
        semantic_queries=["client cannot hire vendor employees directly"],
        plain_english="Check whether the non-solicitation applies to both parties equally.",
        explanation_template=(
            "This MSA includes non-solicitation terms for employees/staff. "
            "Verify whether this is mutual — the client shouldn't be able "
            "to directly hire your team members away, but you also need "
            "to ensure you're not overly restricted."
        ),
        typical_range="Mutual 12-month non-solicitation of each party's direct employees",
        negotiation_script=(
            "Can we make the non-solicitation mutual and limit it to 12 months? "
            "Neither party should be able to directly recruit the other's "
            "key personnel during and shortly after the engagement."
        ),
        safe_harbor_patterns=[
            r"mutual\w*\s+non.?solicit",
            r"each\s+party.{0,40}shall\s+not\s+solicit",
        ],
        safe_harbor_skips=True,
    ),

    Rule(
        rule_id="VENDOR_R015",
        name="Warranty obligations — excessive or undefined",
        contract_types=["vendor"],
        severity="MEDIUM",
        category="legal",
        detection_patterns=[
            r"warrant\w+\s+(that|the\s+deliverable|work\s+product).{0,60}(free\s+from\s+defect|conform|specification)",
            r"warrant\w+\s+period\s+of\s+(1|2|3|one|two|three)\s+year",
            r"remediat\w+\s+(defect|error|bug).{0,40}(at\s+no\s+additional|free\s+of\s+charge|own\s+expense)",
            r"warrant\w+.{0,60}(12|24|36)\s+months",
            r"fix\w*\s+(defect|error|bug)\s+(at\s+vendor'?s?|at\s+(your|no)\s+expense)",
        ],
        semantic_queries=["vendor warrants work for years and must fix defects for free"],
        plain_english="You may be obligated to fix defects for free for an extended period after delivery.",
        explanation_template=(
            "This MSA includes warranty obligations requiring you to remediate "
            "defects at your own expense. A 1-2 year warranty on software or "
            "services can be a significant ongoing cost. "
            "Verify the scope, duration, and what counts as a 'defect.'"
        ),
        typical_range="90-day warranty for services; defects limited to non-conformance with written specifications",
        negotiation_script=(
            "Can we limit the warranty to 90 days and define 'defect' as "
            "material non-conformance with the written specifications in the SOW? "
            "Open-ended multi-year warranties create unlimited ongoing liability."
        ),
        safe_harbor_patterns=[
            r"90\s+day\s+warrant",
            r"warrant\w+\s+(period\s+of\s+)?ninety",
            r"conform\w+\s+to\s+(written\s+)?specification",
        ],
        safe_harbor_skips=False,
        safe_harbor_note=(
            "✅ Warranty appears limited. Verify the duration and defect "
            "definition are specific and reasonable."
        ),
    ),
]
