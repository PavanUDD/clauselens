"""NDA rulebook — 10 rules covering the most critical red flags
in Non-Disclosure Agreements. Built for IT staffing and consulting firms. Expanding to all small businesses."""
from __future__ import annotations
from clauselens.rulebook.schema import Rule

NDA_RULES: list[Rule] = [

    Rule(
        rule_id="NDA_R001",
        name="No expiration on confidentiality",
        contract_types=["nda"],
        severity="HIGH",
        category="confidentiality",
        detection_patterns=[
            r"no\s+expiration",
            r"forever",
            r"in\s+perpetuity",
            r"no\s+time\s+limit",
            r"indefinite\w*\s+(period|duration|obligation)",
            r"shall\s+survive\s+(indefinitely|forever|without\s+limit)",
            r"perpetual\s+confidential",
            r"confidential\w+.{0,40}no\s+(expir|time\s+limit|end\s+date)",
            r"without\s+limitation\s+as\s+to\s+time",
            r"perpetual.*nature.*material\s+term",
            r"continue\s+in\s+perpetuity",
        ],
        semantic_queries=["confidentiality obligation lasts forever no expiration"],
        plain_english="This NDA never expires — you're bound forever.",
        explanation_template=(
            "This NDA has no expiration date on confidentiality. Standard NDAs "
            "limit obligations to 2-5 years for general information. Perpetual "
            "NDAs are often unenforceable except for true trade secrets."
        ),
        typical_range="2-5 years for general info; perpetual only for trade secrets",
        negotiation_script=(
            "Can we add an expiration of 3 years for general confidential "
            "information, with perpetual protection only for specifically "
            "defined trade secrets?"
        ),
        safe_harbor_patterns=[
            r"\d+\s+year",
            r"\d+\s+month",
            r"expir\w+\s+(after|on|in)",
            r"terminat\w+\s+after\s+\d+",
        ],
        safe_harbor_skips=True,
    ),

    Rule(
        rule_id="NDA_R002",
        name="Overly broad definition of confidential information",
        contract_types=["nda"],
        severity="HIGH",
        category="confidentiality",
        detection_patterns=[
            r"absolutely\s+everything",
            r"any\s+and\s+all\s+information",
            r"all\s+information.{0,40}(whether\s+or\s+not\s+marked|regardless)",
            r"everything.{0,30}(learns?|receives?|observes?)",
            r"means\s+absolutely",
            r"without\s+limitation.{0,40}confidential",
        ],
        semantic_queries=["everything is confidential whether marked or not"],
        plain_english="Everything you learn is considered confidential — even casual conversations.",
        explanation_template=(
            "This NDA defines confidential information extremely broadly. "
            "A fair NDA limits confidentiality to specifically identified "
            "categories or information marked as confidential. "
            "Unlimited scope creates impossible obligations."
        ),
        typical_range="Specific categories OR information marked as confidential at disclosure",
        negotiation_script=(
            "Can we limit confidential information to material that is either "
            "marked as confidential at the time of disclosure or identified "
            "in writing within 30 days? Unlimited scope is unworkable."
        ),
    ),

    Rule(
        rule_id="NDA_R003",
        name="Cannot disclose even under court order",
        contract_types=["nda"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"under\s+any\s+circumstances",
            r"including\s+(legal\s+compulsion|court\s+order)",
            r"without\s+prior\s+written\s+approval.{0,60}court",
            r"court\s+order.{0,40}without\s+(prior\s+)?written",
            r"may\s+not\s+disclose.{0,60}(court|legal|compel)",
            r"minimum\s+of\s+fifteen.*business\s+days.*notice",
            r"bear\s+all\s+costs.*protective\s+relief",
            r"prior\s+to\s+any\s+disclosure.*written\s+notice",
        ],
        semantic_queries=["cannot disclose even if court orders you to"],
        plain_english="This NDA claims you can't disclose even if a court orders you to — that's unenforceable and dangerous.",
        explanation_template=(
            "This clause attempts to prevent disclosure even under legal "
            "compulsion. Courts can always compel testimony — this clause "
            "is unenforceable and could put you in an impossible legal position."
        ),
        typical_range="Carve-out for legally compelled disclosure with prompt notice to disclosing party",
        negotiation_script=(
            "We need a standard carve-out: disclosure is permitted if required "
            "by law or court order, provided I give prompt written notice to "
            "allow you to seek a protective order first."
        ),
    ),

    Rule(
        rule_id="NDA_R004",
        name="IP ownership grab in NDA",
        contract_types=["nda"],
        severity="HIGH",
        category="ip",
        detection_patterns=[
            r"ideas?.{0,40}(become|property\s+of|belong\s+to|assign)",
            r"improvements?.{0,40}automatically.{0,40}(property|belong|assign)",
            r"inventions?.{0,60}(disclosing\s+party|other\s+party)",
            r"develop\w+.{0,60}(while\s+having\s+access|during.{0,20}access)",
            r"automatically\s+become\s+the\s+property",
            r"derivative.*works.*assigned.*disclosing\s+party",
            r"inspired\s+by.*confidential\s+information.*assigned",
            r"irrevocably\s+assigned.*sole.*exclusive.*property",
        ],
        semantic_queries=["ideas developed while under NDA become property of other party"],
        plain_english="Any idea you develop while under this NDA automatically becomes their property.",
        explanation_template=(
            "This NDA contains an IP grab. Any ideas or improvements you "
            "develop while having access to their confidential information "
            "become their property. This goes far beyond a standard NDA "
            "and is effectively an IP assignment."
        ),
        typical_range="NDAs should never contain IP assignment — that belongs in a separate agreement",
        negotiation_script=(
            "IP assignment clauses don't belong in an NDA. Can we remove "
            "Section 4 entirely? If IP assignment is needed, it should be "
            "a separate agreement with proper consideration."
        ),
    ),

    Rule(
        rule_id="NDA_R005",
        name="One-sided legal fees — receiving party pays regardless",
        contract_types=["nda"],
        severity="HIGH",
        category="legal",
        detection_patterns=[
            r"legal\s+fees.{0,60}regardless\s+of\s+(outcome|result|who\s+wins)",
            r"attorney.{0,10}fees.{0,60}regardless",
            r"all\s+(legal|attorney).{0,10}fees\s+paid\s+by\s+receiving\s+party",
            r"receiving\s+party.{0,40}(legal|attorney).{0,10}fees",
            r"costs?\s+of\s+(litigation|enforcement).{0,40}receiving\s+party",
            r"non-prevailing\s+party",
            r"regardless\s+of.*outcome.*attorney",
        ],
        semantic_queries=["receiving party pays all legal fees regardless of outcome"],
        plain_english="You pay their legal fees even if they lose — that's one-sided and unfair.",
        explanation_template=(
            "This NDA requires you to pay the other party's legal fees "
            "regardless of outcome. Standard NDAs use 'prevailing party' "
            "fee shifting — whoever wins gets fees paid."
        ),
        typical_range="Prevailing party pays, or each party bears their own fees",
        negotiation_script=(
            "Can we change the fee clause to 'prevailing party' — whoever "
            "wins the dispute gets their legal fees covered?"
        ),
        safe_harbor_patterns=[
            r"prevailing\s+party",
            r"each\s+party\s+(shall\s+)?bear",
        ],
        safe_harbor_skips=True,
    ),

    Rule(
        rule_id="NDA_R006",
        name="Excessive liquidated damages",
        contract_types=["nda"],
        severity="MEDIUM",
        category="legal",
        detection_patterns=[
            r"liquidated\s+damages",
            r"\$[\d,]+\s+(per\s+incident|per\s+breach|per\s+violation)",
            r"damages\s+of\s+\$[\d,]+",
            r"penalty\s+of\s+\$[\d,]+",
            r"fixed\s+(penalty|damages).{0,30}\$[\d,]+",
        ],
        semantic_queries=["fixed dollar penalty per breach of NDA"],
        plain_english="A fixed dollar penalty per breach — check if the amount is proportionate to actual harm.",
        explanation_template=(
            "This NDA specifies liquidated damages of a fixed amount per breach. "
            "Courts only enforce these if they're a reasonable estimate of actual "
            "damages. Excessive amounts may be unenforceable as penalty clauses."
        ),
        typical_range="Actual damages only, or reasonable liquidated damages tied to real estimated harm",
        negotiation_script=(
            "Can we replace fixed liquidated damages with actual damages? "
            "Fixed penalties per incident aren't enforceable unless they "
            "reflect real estimated harm."
        ),
    ),

    Rule(
        rule_id="NDA_R007",
        name="One-sided NDA — only receiving party has obligations",
        contract_types=["nda"],
        severity="MEDIUM",
        category="confidentiality",
        detection_patterns=[
            r"one.?way\s+nda",
            r"unilateral\s+nda",
            r"only\s+the\s+receiving\s+party",
            r"receiving\s+party\s+alone",
            r"obligations?\s+(of|on)\s+(only\s+)?receiving\s+party",
        ],
        semantic_queries=["only one party has confidentiality obligations"],
        plain_english="Only you have confidentiality obligations — the other party has none.",
        explanation_template=(
            "This appears to be a one-sided NDA. Only the receiving party "
            "has obligations. In business relationships where both parties "
            "share sensitive information, a mutual NDA is more fair."
        ),
        typical_range="Mutual NDA for most business relationships",
        negotiation_script=(
            "Since we'll both be sharing sensitive information, can we make "
            "this a mutual NDA with equal obligations on both sides?"
        ),
    ),

    Rule(
        rule_id="NDA_R008",
        name="Pre-consent to injunction without hearing",
        contract_types=["nda"],
        severity="MEDIUM",
        category="legal",
        detection_patterns=[
            r"consent\s+to\s+(an\s+)?injunction",
            r"injunctive\s+relief\s+without\s+(bond|notice|hearing)",
            r"waive.{0,30}(bond|notice).{0,30}injunction",
            r"entitled\s+to\s+injunctive\s+relief\s+without",
            r"irreparable\s+harm.{0,40}injunction\s+without",
        ],
        semantic_queries=["pre-agree to court injunction without hearing or bond"],
        plain_english="You pre-agree to a court injunction without a hearing — giving up your right to be heard first.",
        explanation_template=(
            "This clause makes you pre-consent to injunctive relief without "
            "a bond or hearing. The other party can get a court order against "
            "you immediately without proving their case first."
        ),
        typical_range="Injunctive relief only after proper court process",
        negotiation_script=(
            "Can we remove the pre-consent to injunction without bond or "
            "hearing? Standard practice allows injunctive relief through "
            "normal court process where I can present my position."
        ),
    ),

    Rule(
        rule_id="NDA_R009",
        name="Return or destroy all materials — verify timeline",
        contract_types=["nda"],
        severity="LOW",
        category="obligations",
        detection_patterns=[
            r"return\s+or\s+destroy",
            r"destroy\s+all\s+(copies|materials|documents)",
            r"certif\w+\s+destruction",
            r"return\s+all\s+confidential",
            r"delete\s+all\s+(copies|materials|data)",
        ],
        semantic_queries=["must return or destroy all confidential materials on request"],
        plain_english="You must return or destroy all their confidential materials — verify the timeline and what's excluded.",
        explanation_template=(
            "This NDA requires return or destruction of all confidential "
            "materials. Verify the deadline and whether copies retained "
            "for legal compliance purposes are permitted."
        ),
        typical_range="Return or destroy within 30 days of request; legal compliance copies permitted",
        negotiation_script=(
            "Can we specify a 30-day timeline for return or destruction, "
            "and clarify that copies retained solely for legal compliance "
            "or regulatory purposes are permitted?"
        ),
    ),

    Rule(
        rule_id="NDA_R010",
        name="Governing law in unfavorable jurisdiction",
        contract_types=["nda"],
        severity="LOW",
        category="legal",
        detection_patterns=[
            r"governed\s+by\s+the\s+laws\s+of",
            r"governing\s+law",
            r"jurisdiction\s+(shall\s+be|is)",
            r"venue\s+(shall\s+be|is)",
            r"regardless\s+of\s+where.{0,40}(located|dispute|arises)",
            r"courts?\s+of\s+the\s+state\s+of",
        ],
        semantic_queries=["governing law in different state from where you are located"],
        plain_english="Check which state's laws apply — it may not be yours, meaning disputes are expensive.",
        explanation_template=(
            "This NDA specifies governing law and venue. If different from "
            "where you're located, any dispute requires out-of-state counsel "
            "and travel. Verify the jurisdiction is reasonable."
        ),
        typical_range="Your home state or a neutral commercial state; or arbitration",
        negotiation_script=(
            "Can we change governing law and venue to my home state, or "
            "agree to neutral arbitration rather than a specific state court?"
        ),
    ),
]
