"""Staffing Agreement rulebook — 14 rules covering the most critical
red flags in IT staffing contracts used by ITserve-style companies."""
from __future__ import annotations
from clauselens.rulebook.schema import Rule

STAFFING_RULES: list[Rule] = [

    Rule(
        rule_id="STAFF_R001",
        name="Right-to-hire fee — excessive or undefined",
        contract_types=["staffing"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"right.?to.?hire",
            r"conversion\s+fee",
            r"direct\s+hire\s+fee",
            r"temp.?to.?perm",
            r"convert\w+\s+(to\s+)?permanent",
            r"hire\w*\s+(the\s+)?candidate\s+(directly|permanently)",
            r"placement\s+fee.{0,60}(hire|permanent|direct)",
        ],
        semantic_queries=["fee if client hires staffed worker directly"],
        plain_english="If the client hires your placed candidate directly, you may owe a conversion fee — check the amount and conditions.",
        explanation_template=(
            "This staffing agreement includes right-to-hire or conversion fee terms. "
            "Verify the fee structure, how long it applies, and whether it decreases "
            "over time. Typical right-to-hire fees are 15-25% of first-year salary, "
            "reducing to zero after 6-12 months of placement."
        ),
        typical_range="15-25% of first-year salary, reducing to 0% after 6-12 months",
        negotiation_script=(
            "Can we add a sliding scale to the conversion fee — reducing by "
            "a defined percentage each month of placement, reaching zero "
            "after 6 months? That's the industry standard."
        ),
    ),

    Rule(
        rule_id="STAFF_R002",
        name="Worker misclassification risk — IC treated as employee",
        contract_types=["staffing"],
        severity="HIGH",
        category="compliance",
        detection_patterns=[
            r"independent\s+contractor.{0,60}(direct|control|supervise|manage)",
            r"(client|company|customer)\s+(shall|will|may)\s+(direct|control|supervise)",
            r"work\s+(schedule|hours|location)\s+(set|determined|controlled)\s+by\s+(client|company)",
            r"report\s+(directly|daily)\s+to\s+(client|company|customer)",
            r"subject\s+to\s+(client|company).{0,30}(direction|control|supervision|management)",
        ],
        semantic_queries=["contractor controlled and directed by client like employee"],
        plain_english="The level of client control described may legally reclassify your contractor as an employee — triggering tax and benefit liability.",
        explanation_template=(
            "This agreement describes a level of client control (direction, schedule, "
            "location) that may legally constitute an employment relationship under "
            "IRS and state law. Misclassification exposes both you and the client "
            "to back taxes, penalties, and benefits liability."
        ),
        typical_range="Contractor controls their own methods; client controls outcomes only",
        negotiation_script=(
            "Can we revise this language to clarify that Client directs the "
            "outcomes and deliverables but not the means, methods, or schedule? "
            "This protects both parties from IRS misclassification risk."
        ),
        learn_more="IRS 20-factor test determines worker classification. Behavioral control is the key risk factor.",
    ),

    Rule(
        rule_id="STAFF_R003",
        name="Bench time — no pay during gaps",
        contract_types=["staffing"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"bench\s+(time|period|rate)",
            r"no\s+work\s+available.{0,40}(no\s+pay|not\s+compensat|suspend)",
            r"payment\s+(only\s+)?for\s+hours?\s+(actually\s+)?worked",
            r"minimum\s+(hours?|guarantee).{0,40}(none|not\s+guaranteed|no)",
            r"gap\s+(in\s+)?placement.{0,40}(no\s+(compensation|pay)|suspend)",
        ],
        semantic_queries=["no pay during bench time between placements"],
        plain_english="You may receive no pay during gaps between client assignments — even if you're exclusively committed to this agency.",
        explanation_template=(
            "This staffing agreement provides no pay during bench periods. "
            "If you're exclusively contracted to this agency, you have no "
            "income during gaps. Typical fair arrangements include minimum "
            "guaranteed hours or bench pay at a reduced rate."
        ),
        typical_range="Minimum 20 hours/week guaranteed, or bench pay at 50% billing rate",
        negotiation_script=(
            "Given my exclusivity commitment, can we add a minimum hours "
            "guarantee of 20 hours per week, or bench pay at 50% of billing "
            "rate during gaps between placements?"
        ),
    ),

    Rule(
        rule_id="STAFF_R004",
        name="Exclusivity — cannot work for other clients",
        contract_types=["staffing"],
        severity="HIGH",
        category="restriction",
        detection_patterns=[
            r"exclusively\s+(work|provide|available|dedicat)\s+(for|to)",
            r"shall\s+not\s+(work|provide\s+services|engage).{0,40}(other|third|another)",
            r"exclusiv\w+\s+(arrangement|commitment|agreement)",
            r"not\s+(permitted|allowed)\s+to\s+(work|accept|take).{0,30}(other|additional|outside)",
            r"sole\s+and\s+exclusive\s+(provider|staffing|agency)",
        ],
        semantic_queries=["contractor cannot work for any other client"],
        plain_english="You're locked into this agency exclusively — you cannot take other work even during bench periods.",
        explanation_template=(
            "This staffing agreement requires exclusivity. Combined with no bench "
            "pay guarantee, this means you have no income protection during gaps "
            "and cannot diversify your client base. Exclusivity should come with "
            "minimum pay guarantees."
        ),
        typical_range="Non-exclusive, or exclusive with minimum pay guarantee",
        negotiation_script=(
            "If exclusivity is required, I need a minimum pay guarantee during "
            "bench periods. Otherwise, can we make this non-exclusive so I can "
            "take other work during gaps?"
        ),
    ),

    Rule(
        rule_id="STAFF_R005",
        name="Non-solicitation — cannot follow clients",
        contract_types=["staffing"],
        severity="MEDIUM",
        category="restriction",
        detection_patterns=[
            r"shall\s+not\s+solicit.{0,60}(client|customer|end\s+user)",
            r"non.?solicit\w+.{0,40}(client|customer|account)",
            r"not\s+(approach|contact|work\s+with).{0,40}(client|customer)\s+(directly|independently)",
            r"bypass\w*\s+(agency|staffing\s+firm|recruiter)",
            r"direct\s+(relationship|engagement|contract)\s+with\s+(client|end.?client)",
        ],
        semantic_queries=["cannot contact client directly or bypass staffing agency"],
        plain_english="You cannot work directly with the client company after this placement — even if they want to hire you.",
        explanation_template=(
            "This non-solicitation clause prevents you from working directly "
            "with the client. Verify the duration and scope. "
            "12 months is typical — longer than 24 months is aggressive."
        ),
        typical_range="12 months post-placement; does not prevent client from initiating contact",
        negotiation_script=(
            "Can we limit the non-solicitation to 12 months and clarify it "
            "only restricts me from actively soliciting — not from responding "
            "if the client approaches me directly?"
        ),
    ),

    Rule(
        rule_id="STAFF_R006",
        name="Billing rate markup not disclosed",
        contract_types=["staffing"],
        severity="MEDIUM",
        category="payment",
        detection_patterns=[
            r"billing\s+rate.{0,60}(confidential|not\s+disclos|proprietary)",
            r"mark.?up.{0,40}(confidential|not\s+disclos|trade\s+secret)",
            r"pay\s+rate.{0,60}(separate|different|independent).{0,40}billing",
            r"agency\s+(fee|margin|markup).{0,30}(confidential|not\s+disclos)",
        ],
        semantic_queries=["billing rate to client kept confidential from worker"],
        plain_english="The agency's markup on your rate is kept confidential — you don't know what the client pays for you.",
        explanation_template=(
            "This agreement keeps the client billing rate confidential. "
            "Staffing agency markups typically range from 25-80% above your "
            "pay rate. While common, you should know this when negotiating "
            "your pay rate."
        ),
        typical_range="Markup disclosure or right to renegotiate if markup exceeds 50%",
        negotiation_script=(
            "Can we include a provision that I'm informed of the client billing "
            "rate, or that my pay rate is at minimum 60% of the client billing rate?"
        ),
    ),

    Rule(
        rule_id="STAFF_R007",
        name="Timesheet dispute — agency decision is final",
        contract_types=["staffing"],
        severity="MEDIUM",
        category="payment",
        detection_patterns=[
            r"timesheet.{0,60}(agency|company|firm).{0,30}(final|conclusive|binding|sole\s+discretion)",
            r"disputed\s+(hours?|timesheet).{0,40}(agency|company).{0,30}(determin|decid|final)",
            r"hours?\s+(worked|billed).{0,40}(agency|company).{0,40}(sole|final|conclusive)",
            r"payment\s+(based\s+on|subject\s+to).{0,30}(agency|company).{0,30}(approv|verif|confirm)",
        ],
        semantic_queries=["agency has final say on disputed timesheets"],
        plain_english="If there's a timesheet dispute, the agency's decision is final — you have no independent recourse.",
        explanation_template=(
            "This agreement gives the agency final authority over timesheet disputes. "
            "Without an independent dispute mechanism, you have limited recourse "
            "if hours are incorrectly reduced or denied."
        ),
        typical_range="Dispute escalation process with written documentation and response timeline",
        negotiation_script=(
            "Can we add a formal dispute process — I submit written documentation "
            "of disputed hours, agency responds within 5 business days with "
            "written explanation, and we escalate to a neutral third party "
            "if unresolved?"
        ),
    ),

    Rule(
        rule_id="STAFF_R008",
        name="Background check costs charged to contractor",
        contract_types=["staffing"],
        severity="LOW",
        category="payment",
        detection_patterns=[
            r"background\s+check.{0,60}(contractor|candidate|worker).{0,30}(cost|expense|pay|responsible)",
            r"(drug\s+test|screening|clearance).{0,60}(contractor|candidate).{0,30}(cost|expense|pay)",
            r"cost\s+of\s+(background|screening|drug).{0,30}(deduct|withhold|contractor)",
        ],
        semantic_queries=["contractor pays for their own background check"],
        plain_english="You may be charged for required background checks or drug tests.",
        explanation_template=(
            "This agreement requires you to pay for background checks or "
            "drug testing. These costs should typically be borne by the "
            "agency or client — they're a cost of doing business, not "
            "your personal expense."
        ),
        typical_range="Agency or client pays all screening costs",
        negotiation_script=(
            "Can the agency cover background check and drug test costs? "
            "These are required by your client process, not my choice."
        ),
    ),

    Rule(
        rule_id="STAFF_R009",
        name="Payment delay — paid only when agency is paid",
        contract_types=["staffing"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"paid\s+(only\s+)?when\s+(agency|company|firm)\s+(receives?|is\s+paid|collects?)",
            r"payment\s+(contingent|conditional)\s+(on|upon)\s+(receipt|collection|agency\s+receiv)",
            r"subject\s+to\s+(agency|company)\s+receiv\w+\s+payment",
            r"pay.?when.?paid",
            r"receipt\s+of\s+funds\s+from\s+(client|end.?client|customer)",
        ],
        semantic_queries=["contractor only paid after agency receives client payment"],
        plain_english="You only get paid after the agency collects from the client — client non-payment becomes your risk.",
        explanation_template=(
            "This is a 'pay-when-paid' clause. If the client doesn't pay the agency, "
            "the agency doesn't pay you. This transfers client credit risk entirely "
            "to you. Many states have laws prohibiting pay-when-paid clauses "
            "for certain worker types."
        ),
        typical_range="Payment on fixed schedule regardless of client payment status",
        negotiation_script=(
            "Can we remove the pay-when-paid clause? I have no relationship with "
            "the end client and can't manage their credit risk. "
            "I need payment on a fixed schedule regardless of when you collect."
        ),
    ),

    Rule(
        rule_id="STAFF_R010",
        name="Immediate termination — no notice period",
        contract_types=["staffing"],
        severity="MEDIUM",
        category="termination",
        detection_patterns=[
            r"terminat\w+\s+(immediately|without\s+notice|with\s+no\s+notice)",
            r"(agency|company|firm)\s+may\s+terminat\w+\s+(at\s+any\s+time|immediately)",
            r"terminat\w+\s+effective\s+immediately",
            r"no\s+notice\s+(required|period|necessary).{0,40}terminat",
            r"without\s+(any\s+)?prior\s+notice.{0,30}terminat",
        ],
        semantic_queries=["agency can terminate contractor immediately with no notice"],
        plain_english="The agency can end your placement immediately with zero notice — no income protection.",
        explanation_template=(
            "This agreement allows immediate termination with no notice period. "
            "For a contractor depending on this income, zero notice is a "
            "serious financial risk. Typical agreements provide 1-2 weeks notice "
            "or equivalent pay in lieu."
        ),
        typical_range="2 weeks written notice, or 2 weeks pay in lieu of notice",
        negotiation_script=(
            "Can we add a minimum 2-week notice period for termination, "
            "or 2 weeks pay in lieu? Immediate termination with no financial "
            "protection is unreasonable given my commitment to this placement."
        ),
        safe_harbor_patterns=[
            r"(2|two)\s+weeks?\s+(notice|written\s+notice)",
            r"(14|fifteen|14)\s+days?\s+(notice|written\s+notice)",
            r"pay\s+in\s+lieu\s+of\s+notice",
        ],
        safe_harbor_skips=True,
    ),

    Rule(
        rule_id="STAFF_R011",
        name="Insurance requirements — excessive or at contractor's cost",
        contract_types=["staffing"],
        severity="MEDIUM",
        category="compliance",
        detection_patterns=[
            r"contractor\s+(shall|must|is\s+required\s+to)\s+(maintain|carry|obtain)\s+insurance",
            r"(general\s+liability|professional\s+liability|E&O|errors\s+and\s+omissions).{0,40}(contractor|worker)",
            r"minimum\s+(coverage|insurance)\s+of\s+\$[\d,]+",
            r"additional\s+insured.{0,40}(agency|company|client)",
            r"certificate\s+of\s+insurance.{0,40}(required|provide|furnish)",
        ],
        semantic_queries=["contractor required to carry expensive liability insurance"],
        plain_english="You may be required to carry expensive professional liability insurance at your own cost.",
        explanation_template=(
            "This agreement requires you to maintain insurance at your own expense. "
            "Professional liability (E&O) insurance for IT contractors can cost "
            "$1,000-5,000/year. Verify coverage requirements and whether the "
            "agency's umbrella policy covers you."
        ),
        typical_range="Agency provides umbrella coverage; contractor carries basic general liability only",
        negotiation_script=(
            "Can we clarify whether the agency's umbrella policy covers me for "
            "work performed under this agreement? If not, can we negotiate "
            "reimbursement for required insurance premiums above $500/year?"
        ),
    ),

    Rule(
        rule_id="STAFF_R012",
        name="Expense reimbursement — limited or excluded",
        contract_types=["staffing"],
        severity="LOW",
        category="payment",
        detection_patterns=[
            r"expense\w*.{0,40}(not\s+reimburse|no\s+reimbursement|contractor\s+responsible)",
            r"(travel|equipment|software|tool).{0,40}(contractor'?s?\s+expense|not\s+covered|not\s+reimburse)",
            r"no\s+(additional|separate)\s+compensation\s+for\s+(expense|travel|equipment)",
            r"all\s+expenses?\s+(are\s+)?(included|incorporated|covered)\s+in\s+(the\s+)?rate",
        ],
        semantic_queries=["contractor not reimbursed for travel or equipment expenses"],
        plain_english="Business expenses like travel, equipment, or software may not be reimbursed — they come out of your rate.",
        explanation_template=(
            "This agreement may not reimburse business expenses. If your "
            "billing rate doesn't account for significant travel, equipment, "
            "or software costs, your effective hourly rate is lower than "
            "it appears."
        ),
        typical_range="Pre-approved expenses reimbursed at cost within 30 days",
        negotiation_script=(
            "Can we add a provision for reimbursement of pre-approved "
            "project-related expenses? Travel, specialized software, and "
            "equipment required for this engagement should be reimbursed separately."
        ),
    ),

    Rule(
        rule_id="STAFF_R013",
        name="Visa sponsorship — undefined obligations",
        contract_types=["staffing"],
        severity="HIGH",
        category="compliance",
        detection_patterns=[
            r"visa\s+sponsor\w*",
            r"h.?1b",
            r"work\s+(authorization|permit|visa)",
            r"immigration\s+(status|sponsor|support)",
            r"labor\s+condition\s+application",
            r"LCA",
            r"prevailing\s+wage",
        ],
        semantic_queries=["visa sponsorship H1B work authorization terms"],
        plain_english="This contract involves visa sponsorship — verify all obligations, costs, and what happens if the placement ends.",
        explanation_template=(
            "This staffing agreement involves visa sponsorship. Critical questions: "
            "Who pays visa filing fees? What happens to your visa status if the "
            "placement ends? Are you tied to this agency while on sponsored status? "
            "Immigration obligations in staffing contracts require careful review."
        ),
        typical_range="Agency pays all visa costs; worker retains ability to transfer sponsorship; written transition plan",
        negotiation_script=(
            "Can we clearly specify: (1) who pays all visa fees, (2) your "
            "obligations if my placement ends before visa expiry, and (3) "
            "whether I can transfer sponsorship to another employer? "
            "These terms are critical for my immigration status."
        ),
        learn_more="USCIS regulations require H-1B employers to pay return transportation if worker is terminated early.",
    ),

    Rule(
        rule_id="STAFF_R014",
        name="Training cost repayment obligation",
        contract_types=["staffing"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"training.{0,60}(repay|reimburse|cost|expense).{0,40}(terminat|leave|resign)",
            r"(repay|reimburse).{0,40}training.{0,60}(terminat|leave|exit|resign)",
            r"cost\s+of\s+training.{0,40}(deduct|withhold|repay)",
            r"training\s+(fee|cost|expense).{0,40}(clawback|recover|repay)",
            r"leave.{0,30}within.{0,30}(months?|year).{0,30}training",
        ],
        semantic_queries=["contractor must repay training costs if they leave early"],
        plain_english="You may owe the agency for training costs if you leave before a specified period.",
        explanation_template=(
            "This staffing agreement requires repayment of training costs "
            "if you leave before a specified period. Verify the amount, "
            "the repayment period, and whether training was mandatory. "
            "Excessive training repayment clauses can trap workers."
        ),
        typical_range="Pro-rata repayment only for voluntary resignation within 6 months; zero repayment for termination without cause",
        negotiation_script=(
            "Can we limit training repayment to voluntary resignation only "
            "(not termination), cap it at actual documented costs, and "
            "pro-rate it over a maximum 6-month period? "
            "If you terminate me, I owe nothing."
        ),
    ),
]
