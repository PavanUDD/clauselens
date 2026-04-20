"""Employment contract rulebook — 16 rules covering the most common red flags."""
from __future__ import annotations
from clauselens.rulebook.schema import Rule

EMPLOYMENT_RULES: list[Rule] = [

    Rule(
        rule_id="EMP_R001",
        name="Overly broad non-compete clause",
        contract_types=["employment"],
        severity="HIGH",
        category="restriction",
        detection_patterns=[
            r"non.?compete",
            r"shall\s+not\s+compete",
            r"restrictive\s+covenant",
            r"competing\s+business",
        ],
        semantic_queries=["cannot work for competitor after leaving"],
        plain_english="You may be restricted from working for competitors after you leave.",
        explanation_template=(
            "This contract has a non-compete clause. Typical enforceable non-competes are "
            "6-12 months within a specific region. Nationwide or multi-year non-competes "
            "are often unenforceable — and as of 2024, the FTC banned most new non-competes."
        ),
        typical_range="6-12 months, limited region",
        negotiation_script=(
            "I'd like to narrow the non-compete to 6 months within [city/region] and limit "
            "it to directly competing products. Broader restrictions are often unenforceable."
        ),
        learn_more="FTC's 2024 rule bans most new non-compete agreements.",
    ),

    Rule(
        rule_id="EMP_R002",
        name="At-will employment",
        contract_types=["employment"],
        severity="MEDIUM",
        category="termination",
        detection_patterns=[
            r"at.?will\s+employ\w+",
            r"employment\s+at\s+will",
            r"terminate\s+at\s+any\s+time\s+with\s+or\s+without",
        ],
        semantic_queries=["employer can terminate at any time"],
        plain_english="You can be fired at any time, with or without cause.",
        explanation_template=(
            "This is at-will employment — standard in most US states but worth knowing. "
            "Either party can terminate at any time. Check severance and notice terms."
        ),
        typical_range="Standard in 49 US states",
        negotiation_script=(
            "Given the at-will nature, can we include a severance clause (e.g., 2-4 weeks "
            "per year of service) for involuntary termination without cause?"
        ),
    ),

    Rule(
        rule_id="EMP_R003",
        name="No severance for termination",
        contract_types=["employment"],
        severity="HIGH",
        category="termination",
        detection_patterns=[
            r"no\s+severance",
            r"without\s+severance",
            r"not\s+entitled\s+to\s+(any\s+)?severance",
            r"severance\s+shall\s+not",
        ],
        semantic_queries=["no severance if terminated"],
        plain_english="You get no severance pay if you're let go.",
        explanation_template=(
            "This contract provides no severance. Typical severance is 1-4 weeks per year "
            "of service for involuntary termination without cause. No severance is unfavorable."
        ),
        typical_range="1-4 weeks per year of service",
        negotiation_script=(
            "Can we add severance of 2 weeks per year of service for termination without "
            "cause? That's standard for salaried positions."
        ),
    ),

    Rule(
        rule_id="EMP_R004",
        name="Work-for-hire IP assignment",
        contract_types=["employment"],
        severity="HIGH",
        category="ip",
        detection_patterns=[
            r"work\s+(made\s+)?for\s+hire",
            r"all\s+(inventions|works|ip)\s+(shall\s+be|are)\s+(the\s+property\s+of|assigned)",
            r"assign\w*\s+all\s+right",
            r"intellectual\s+property\s+(shall|is)\s+(belong|assigned|owned)",
        ],
        semantic_queries=["company owns everything you create"],
        plain_english="The company owns anything you create — even on your own time.",
        explanation_template=(
            "This clause assigns IP to the employer. Many states (CA, WA, etc.) exempt "
            "inventions created on your own time with your own resources. Review the "
            "scope carefully if you have side projects or pre-existing IP."
        ),
        typical_range="Work done during employment, using company resources",
        negotiation_script=(
            "Can we add an exception for inventions created on my own time, with my own "
            "resources, unrelated to company business? California Labor Code 2870 codifies this."
        ),
        learn_more="CA Labor Code 2870 protects personal inventions outside company scope.",
    ),

    Rule(
        rule_id="EMP_R005",
        name="Mandatory arbitration",
        contract_types=["employment"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"binding\s+arbitration",
            r"mandatory\s+arbitration",
            r"submit\s+to\s+arbitration",
            r"arbitration\s+shall\s+be\s+the\s+(sole|exclusive)",
        ],
        semantic_queries=["disputes resolved by arbitration"],
        plain_english="You can't sue — disputes go to private arbitration.",
        explanation_template=(
            "Employment disputes must go to arbitration, not court. You lose access to "
            "jury trials and often class-action rights. Arbitrator fees are sometimes shared."
        ),
        typical_range="Optional / employee can choose court",
        negotiation_script=(
            "Can we make arbitration optional rather than mandatory? Or at minimum, "
            "ensure the company covers all arbitration fees."
        ),
    ),

    Rule(
        rule_id="EMP_R006",
        name="Non-solicitation of employees/customers",
        contract_types=["employment"],
        severity="MEDIUM",
        category="restriction",
        detection_patterns=[
            r"non.?solicit\w*",
            r"shall\s+not\s+solicit",
            r"solicit\w+\s+(employees|customers|clients)",
        ],
        semantic_queries=["cannot recruit former coworkers or customers"],
        plain_english="After leaving, you can't recruit coworkers or customers for a set time.",
        explanation_template=(
            "This non-solicitation clause prevents you from recruiting former coworkers "
            "or customers. Typical scope is 6-12 months. Lifetime or vague clauses are "
            "often unenforceable."
        ),
        typical_range="6-12 months",
        negotiation_script=(
            "Can we limit the non-solicitation to 12 months and specify it covers only "
            "direct solicitation, not general job-market activity?"
        ),
    ),

    Rule(
        rule_id="EMP_R007",
        name="Unlimited confidentiality obligation",
        contract_types=["employment"],
        severity="MEDIUM",
        category="confidentiality",
        detection_patterns=[
            r"confidential\w+\s+(in\s+perpetuity|forever|indefinite)",
            r"perpetual\s+confidentialit",
            r"confidential\w+\s+obligation\w*",
            r"non.?disclosure",
        ],
        semantic_queries=["confidentiality lasts forever"],
        plain_english="You must keep company info secret — possibly forever.",
        explanation_template=(
            "This NDA obligation may be unlimited in duration. Typical confidentiality "
            "for non-trade-secret info is 2-5 years. Perpetual NDAs are often unenforceable "
            "except for true trade secrets."
        ),
        typical_range="2-5 years for general confidential info; perpetual only for trade secrets",
        negotiation_script=(
            "Can we limit the confidentiality term to 3 years for general information, "
            "with perpetual protection only for defined trade secrets?"
        ),
    ),

    Rule(
        rule_id="EMP_R008",
        name="No overtime / exempt status",
        contract_types=["employment"],
        severity="MEDIUM",
        category="payment",
        detection_patterns=[
            r"exempt\s+(from\s+)?overtime",
            r"no\s+overtime\s+pay",
            r"exempt\s+employee",
            r"salaried\s+exempt",
        ],
        semantic_queries=["no overtime pay exempt status"],
        plain_english="You won't get overtime pay — make sure this is legal for your role.",
        explanation_template=(
            "You're classified as exempt from overtime. This is legal only for specific "
            "roles under FLSA (executive, admin, professional, computer, outside sales) "
            "earning above a minimum threshold. Misclassification is a common violation."
        ),
        typical_range="Exempt only if salary > FLSA threshold AND job duties qualify",
        negotiation_script=(
            "Can you confirm in writing that my role qualifies as exempt under FLSA "
            "definitions (executive/admin/professional) so we're clear on overtime rules?"
        ),
    ),

    Rule(
        rule_id="EMP_R009",
        name="Clawback of bonuses or equity",
        contract_types=["employment"],
        severity="HIGH",
        category="payment",
        detection_patterns=[
            r"clawback",
            r"claw.?back",
            r"forfeit\w+\s+(bonus|equity|stock|options)",
            r"repay\w+\s+(bonus|signing\s+bonus)",
            r"recoup\w+\s+compensation",
        ],
        semantic_queries=["have to repay bonus if I leave"],
        plain_english="You may have to pay back your bonus or lose equity if you leave.",
        explanation_template=(
            "This contract includes clawback provisions. Common for signing bonuses "
            "(pro-rata if you leave within 12 months) and unvested equity. Review carefully "
            "if you're negotiating a signing bonus or RSUs."
        ),
        typical_range="Pro-rata clawback within 12 months for signing bonuses",
        negotiation_script=(
            "Can we limit the clawback window to 12 months and make it pro-rata rather "
            "than full repayment? That's more standard."
        ),
    ),

    Rule(
        rule_id="EMP_R010",
        name="Relocation / travel obligation",
        contract_types=["employment"],
        severity="LOW",
        category="restriction",
        detection_patterns=[
            r"reloca\w+",
            r"required\s+to\s+travel",
            r"transfer\w+\s+to\s+(another|any)\s+(location|office)",
        ],
        semantic_queries=["required to relocate or travel"],
        plain_english="You may be required to relocate or travel as a condition of the job.",
        explanation_template=(
            "This contract requires relocation or travel. Confirm whether the company "
            "covers moving costs and what happens if you decline a relocation."
        ),
        typical_range="Company pays relocation costs; reasonable travel only",
        negotiation_script=(
            "Can we specify that relocation is voluntary, that the company covers moving "
            "expenses, and that refusing relocation is not grounds for termination?"
        ),
    ),

    Rule(
        rule_id="EMP_R011",
        name="Probationary period",
        contract_types=["employment"],
        severity="LOW",
        category="termination",
        detection_patterns=[
            r"probation\w+\s+period",
            r"introductory\s+period",
            r"during\s+probation",
            r"first\s+\d+\s+(days|months)\s+of\s+employment",
        ],
        semantic_queries=["probationary period first months"],
        plain_english="There's a probation period with easier termination rules.",
        explanation_template=(
            "This contract includes a probationary period. Typical probation is 90 days "
            "(3 months). Over 6 months is unusual. During probation, you may have reduced "
            "benefits or easier termination."
        ),
        typical_range="90 days (3 months)",
        negotiation_script=(
            "Can we cap the probation at 90 days? That's the industry norm for most roles."
        ),
    ),

    Rule(
        rule_id="EMP_R012",
        name="Low or undefined PTO",
        contract_types=["employment"],
        severity="MEDIUM",
        category="benefits",
        detection_patterns=[
            r"paid\s+time\s+off",
            r"\bpto\b",
            r"vacation\s+(days|time|policy)",
            r"annual\s+leave",
        ],
        semantic_queries=["paid time off policy"],
        plain_english="Verify PTO days — below 10 days/year is below US norms.",
        explanation_template=(
            "This contract addresses PTO. Typical salaried roles offer 10-20 days of PTO. "
            "Below 10 days is below US norms. 'Unlimited PTO' sounds good but often "
            "results in less time taken — verify the culture."
        ),
        typical_range="10-20 days PTO annually",
        negotiation_script=(
            "Can we confirm PTO at 15 days annually? That's aligned with market standard "
            "for this role level."
        ),
    ),

    Rule(
        rule_id="EMP_R013",
        name="Assignment of pre-existing IP",
        contract_types=["employment"],
        severity="HIGH",
        category="ip",
        detection_patterns=[
            r"prior\s+inventions",
            r"pre.?existing\s+(intellectual\s+property|ip|inventions)",
            r"all\s+inventions\s+(including|whether)",
        ],
        semantic_queries=["company owns my previous work"],
        plain_english="The company may try to claim work you did BEFORE joining.",
        explanation_template=(
            "This clause may sweep in pre-existing IP. You should list any prior inventions, "
            "side projects, or GitHub repositories in an exhibit/schedule so they're "
            "explicitly excluded from assignment."
        ),
        typical_range="Exhibit listing all pre-existing IP explicitly excluded",
        negotiation_script=(
            "I'd like to attach an exhibit listing my pre-existing inventions and "
            "open-source contributions so they're explicitly carved out of the IP assignment."
        ),
    ),

    Rule(
        rule_id="EMP_R014",
        name="One-sided termination notice",
        contract_types=["employment"],
        severity="MEDIUM",
        category="termination",
        detection_patterns=[
            r"employee\s+(shall|must)\s+provide\s+\d+\s+(days|weeks|months)\s+notice",
            r"terminat\w+\s+by\s+(the\s+)?employee\s+(shall|must|requires)",
        ],
        semantic_queries=["employee must give long notice but employer can fire immediately"],
        plain_english="You must give long notice to quit, but they can fire you anytime.",
        explanation_template=(
            "The notice period is asymmetric. If you must provide significant notice but "
            "the employer can terminate immediately, the contract favors the employer. "
            "Typical is 2 weeks from employee, with reciprocal obligation from employer."
        ),
        typical_range="2 weeks notice from employee; similar or severance from employer",
        negotiation_script=(
            "Can we make the notice period reciprocal? Either equal notice both ways, or "
            "severance from the employer in lieu of notice."
        ),
    ),

    Rule(
        rule_id="EMP_R015",
        name="Change of control / acquisition clause",
        contract_types=["employment"],
        severity="LOW",
        category="termination",
        detection_patterns=[
            r"change\s+of\s+control",
            r"change\s+in\s+control",
            r"acquisition\s+of\s+the\s+company",
            r"merger\s+or\s+acquisition",
        ],
        semantic_queries=["what happens if company is acquired"],
        plain_english="Read carefully what happens to your job if the company is acquired.",
        explanation_template=(
            "This clause addresses company acquisition. Check whether your equity "
            "accelerates, whether you're entitled to severance if terminated post-acquisition, "
            "and whether your role must be 'substantially similar' after the deal."
        ),
        typical_range="Double-trigger acceleration (acquisition + termination) for equity",
        negotiation_script=(
            "Can we add double-trigger equity acceleration — full vesting if my role is "
            "eliminated or materially changed within 12 months of an acquisition?"
        ),
    ),

    Rule(
        rule_id="EMP_R016",
        name="Personal liability for company losses",
        contract_types=["employment"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"employee\s+(shall|will|is)\s+(be\s+)?liable\s+for",
            r"personal\s+liabilit\w+",
            r"indemnif\w+\s+(the\s+)?(company|employer)",
            r"hold\s+(the\s+)?(company|employer)\s+harmless",
        ],
        semantic_queries=["employee personally liable for losses"],
        plain_english="You may be personally liable for losses or asked to cover company costs.",
        explanation_template=(
            "This clause makes you potentially liable for company losses or requires you "
            "to indemnify the company. This is highly unusual for standard employment "
            "and can expose personal assets. Serious red flag."
        ),
        typical_range="Company indemnifies employee acting in good faith",
        negotiation_script=(
            "Personal liability for company losses isn't standard for employees. Can we "
            "remove this clause? I'd expect the company to indemnify me for actions taken "
            "in good faith within the scope of my role."
        ),
    ),
]