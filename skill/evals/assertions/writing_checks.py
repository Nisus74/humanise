"""Objective assertion functions for humanise eval harness.

Each function takes a draft string (and optional audience_tag) and returns a dict
with a score and diagnostic details. Used by run_all.py to grade outputs, and by
the live workflow (SKILL.md Step 3) as the automated mechanical sweep, pass one.

June 2026 revisions:
- 'endeavour' removed from the AusE marker list (it's severity-1 slop; being
  Australian doesn't rescue it).
- severity-2/3 pass threshold tightened to <= 2, matching the fingerprint table.
- curly-quote check is medium-aware: in docx, curly is the human default and
  only mixing curly with straight fails.
- New checks: I/This sentence openers (hard fail in formal channels only),
  sentence-length profile (runs of 3 similar-length sentences), paragraph-shape
  variance (advisory), and the spaced-hyphen dash substitute.
"""

import re
from collections import Counter
from functools import lru_cache


# Spans wrapped in <!--sweep-ignore--> ... <!--/sweep-ignore--> are exempt from
# every check. Use for quoted material, "before" examples, and banned words named
# for teaching, so legitimately-present slop doesn't produce false positives.
SWEEP_IGNORE_RE = re.compile(
    r"<!--\s*sweep-ignore\s*-->.*?<!--\s*/\s*sweep-ignore\s*-->",
    re.DOTALL | re.IGNORECASE,
)


def strip_sweep_ignore(draft):
    """Remove sweep-exempt spans before any check runs."""
    return SWEEP_IGNORE_RE.sub(" ", draft)


SEVERITY_1_SLOP = [
    "delve",
    "tapestry",
    "multifaceted",
    "nuanced",
    "realm",
    "embark",
    "endeavour",
    "endeavor",
    "intricate",
    "intricacies",
    "pivotal",
    "meticulous",
    "meticulously",
    "testament",
    "interplay",
]

# "landscape" is severity 1 only when metaphorical: an abstract-domain modifier
# precedes it ("competitive/regulatory/AI landscape"). Literal uses ("landscape
# photography", "a landscape of rolling hills") are left alone. Compiled once.
LANDSCAPE_METAPHOR_RE = re.compile(
    r"\b(?:competitive|business|market|funding|regulatory|threat|media|"
    r"political|economic|technological|technology|tech|digital|cultural|"
    r"legal|financial|investment|startup|vendor|product|industry|innovation|"
    r"security|data|current|evolving|changing|shifting|broader|wider|global|"
    r"modern|emerging|ai)\s+landscape\b",
    re.IGNORECASE,
)

SEVERITY_2_3_SLOP = [
    "leverage",
    "utilise",
    "utilize",
    "facilitate",
    "robust",
    "seamless",
    "seamlessly",
    "foster",
    "transformative",
    "comprehensive",
    "holistic",
    "garner",
    "bolster",
    "harness",
    "spearhead",
    "catalyse",
    "catalyze",
    "streamline",
    "empower",
    "enhance",
    "fundamentally",
    "incredibly",
    "genuinely",
    "essentially",
    "ultimately",
    "undeniably",
    "remarkably",
    # newer 2026 tells (see ai-slop-dictionary Severity 2.5)
    "underpin",
    "underpinned",
    "crucially",
    "resonate",
    "resonates",
    # impeccable.design STYLE.md additions (stolen-engineer diction + marketing 2025)
    "load-bearing",
    "highest-leverage",
    "biggest unlock",
    "data-driven",
    "elevate",
    "elevates",
    "underscore",
    "underscores",
]

# Academic / register-paper verbs. The fancier cousins of copula avoidance
# (serves as / functions as). They swap the user's crisp first person for a
# dissertation register. Single words go here; multiword phrases in
# ACADEMIC_PHRASES below. Mapped to plain verbs in ai-slop-dictionary.md.
ACADEMIC_VERBS = [
    "operationalise",
    "operationalised",
    "operationalises",
    "operationalising",
    "operationalize",
    "operationalized",
    "operationalizes",
    "constitute",
    "constitutes",
    "constituted",
    "constituting",
    "encompass",
    "encompasses",
    "encompassed",
    "encompassing",
    "elucidate",
    "elucidates",
    "elucidated",
    "evince",
    "evinces",
    "instantiate",
    "instantiates",
    "necessitate",
    "necessitates",
    "necessitated",
    "necessitating",
    "delineate",
    "delineates",
    "delineated",
]

ACADEMIC_PHRASES = [
    "stem from",
    "stems from",
    "stemmed from",
    "stemming from",
    "predicated on",
    "predicated upon",
    "contingent upon",
    "contingent on",
    "illustrative of",
    "indicative of",
    "reflective of",
    "germane to",
    "by virtue of",
    "in light of the fact",
    "serves to",
    "serve to",
]

# Verbs and phrases scanned together by academic_register; joined once at import.
ACADEMIC_REGISTER = ACADEMIC_VERBS + ACADEMIC_PHRASES

# Self-narrated honesty / meta-candour. The writing announces its own candour
# instead of just being candid. A trust-me reflex models reach for and people
# rarely use. Rewrite rule: delete the caption, keep the claim.
META_CANDOUR = [
    "honestly",
    "to be honest",
    "if i am honest",
    "if i'm honest",
    "i'll be honest",
    "in all honesty",
    "the honest version",
    "the honest answer",
    "the honest read",
    "an honest label",
    "an honest assessment",
    "candidly",
    "in plain terms",
    "plainly put",
    "let's be clear",
    "let me be clear",
    "the truth is",
    "truth be told",
    "the straightforward statement",
    "the straightforward version",
    "the real answer is",
    "the plain truth",
    "frankly",
]
# Noun-phrase form: "Pipeline honesty:", "One honesty:" etc. matched by regex.
META_CANDOUR_LABEL_RE = re.compile(r"\b[A-Z][a-z]+\s+honesty\s*:", re.MULTILINE)


SLOP_OPENERS = [
    "here's the thing",
    "here's what most people miss",
    "here's what nobody's talking about",
    "here's the uncomfortable truth",
    "let me be clear",
    "i'll be honest",
    "let's talk about",
    "we need to talk about",
    "what most people don't realise",
    "what most people don't realize",
    "i hope this email finds you well",
    "i hope this finds you well",
    "in today's rapidly evolving",
    "in today's fast-paced",
    "in today's digital",
    "in today's evolving",
    "i wanted to reach out",
    "i am writing to apply",
    # impeccable.design STYLE.md
    "gone are the days",
    "let's dive in",
    "let's dive into",
    "whether you're",
    "whether you are",
]

AUSE_ENDINGS = [
    # -ise verb family (AusE) vs -ize (US). Broadened to cover the common verbs;
    # a narrow list under-counts genuinely Australian prose (see notes in SKILL.md
    # "Tripwires, not targets"). Verb endings only, to avoid matching nouns like
    # "expertise", "premise", "exercise", "compromise".
    r"\borganis(ed|es|e|ing|ation|ations)\b",
    r"\brecognis(ed|es|e|ing|ation)\b",
    r"\brealis(ed|es|e|ing|ation)\b",
    r"\bprioritis(ed|es|e|ing|ation)\b",
    r"\bsummaris(ed|es|e|ing|ation)\b",
    r"\bspecialis(ed|es|e|ing|ation)\b",
    r"\bminimis(ed|es|e|ing|ation)\b",
    r"\bmaximis(ed|es|e|ing|ation)\b",
    r"\bfinalis(ed|es|e|ing|ation)\b",
    r"\bcustomis(ed|es|e|ing|ation)\b",
    r"\bstandardis(ed|es|e|ing|ation)\b",
    r"\bemphasis(ed|es|e|ing)\b",
    r"\bcategoris(ed|es|e|ing|ation)\b",
    r"\bnormalis(ed|es|e|ing|ation)\b",
    r"\bmobilis(ed|es|e|ing|ation)\b",
    r"\butilis(ed|es|e|ing|ation)\b",
    r"\boptimis(ed|es|e|ing|ation)\b",
    r"\bmodernis(ed|es|e|ing|ation)\b",
    r"\bproductis(ed|es|e|ing)\b",
    r"\bcharacteris(ed|es|e|ing|ation)\b",
    r"\bgeneralis(ed|es|e|ing|ation)\b",
    r"\bcentralis(ed|es|e|ing|ation)\b",
    r"\bcapitalis(ed|es|e|ing|ation)\b",
    r"\bstabilis(ed|es|e|ing|ation)\b",
    r"\bscrutinis(ed|es|e|ing)\b",
    r"\bapologis(ed|es|e|ing)\b",
    r"\bcriticis(ed|es|e|ing)\b",
    r"\bvisualis(ed|es|e|ing|ation)\b",
    r"\bfamiliaris(ed|es|e|ing)\b",
    r"\bincentivis(ed|es|e|ing)\b",
    r"\bdigitis(ed|es|e|ing|ation)\b",
    r"\bsynthesis(ed|es|e|ing)\b",
    r"\banalys(ed|es|e|ing)\b",  # AusE 'analyse' vs US 'analyze'
    # -our family. NOTE: 'endeavour' deliberately excluded; it's severity-1 slop
    # and must never count toward AusE visibility.
    r"\bcolour(s|ed|ing|ful)?\b",
    r"\bbehaviour(s|al)?\b",
    r"\bneighbour(s|hood|ing)?\b",
    r"\bhonour(s|ed|ing|able)?\b",
    r"\bfavour(s|ed|ing|able|ably|ite|ites)?\b",
    r"\blabour(s|ed|ing)?\b",
    r"\b(rigour|vigour|valour|flavour|savour|vapour|odour|tumour|demeanour|candour|ardour|clamour|splendour|harbour|parlour|rumour|saviour|fervour|glamour)(s|ed|ing|able)?\b",
    # -re family
    r"\bcentre(s|d)?\b",
    r"\btheatre(s)?\b",
    r"\bfibre(s)?\b",
    r"\blitre(s)?\b",
    r"\bmetre(s)?\b",
    r"\b(calibre|lustre|sombre|spectre|manoeuvre|sabre)(s|d)?\b",
    # -ll- inflections (AusE doubles the l)
    r"\btravelling\b",
    r"\bmodelling\b",
    r"\bcancelled\b",
    # 'fulfilling' is spelled identically in AusE and US, so it is not a regional
    # marker and is intentionally absent from both lists.
    r"\blabelling\b",
    r"\b(modelled|labelled|travelled|signalled|fuelled|funnelled|counselled|levelled|totalled|marvelled|cancelling)\b",
    # digraphs (ae/oe) common in AusE, especially medical
    r"\b(haemo\w*|haemato\w*|anaemi\w*|leukaemi\w*|paediatric\w*|orthopaedic\w*|oedema|oesophag\w*|foetal|foetus|oestrogen|coeliac)\b",
    # -ogue / misc
    r"\bcatalogue(s|d)?\b",
    r"\bdialogue(s)?\b",
    r"\banalogue(s)?\b",
    r"\bprogramme(s)?\b",
    r"\bpractis(ed|es|e|ing)\b",  # AusE verb
    r"\blicence(s|d)?\b",  # AusE noun
    r"\bdefence\b",
    r"\boffence\b",
    r"\backnowledgement(s)?\b",
    r"\bjudgement(s)?\b",
]

US_ENDINGS = [
    r"\borganiz(ed|es|e|ing|ation|ations)\b",
    r"\brecogniz(ed|es|e|ing|ation)\b",
    r"\brealiz(ed|es|e|ing|ation)\b",
    r"\bprioritiz(ed|es|e|ing|ation)\b",
    r"\bsummariz(ed|es|e|ing|ation)\b",
    r"\bspecializ(ed|es|e|ing|ation)\b",
    r"\bminimiz(ed|es|e|ing|ation)\b",
    r"\bmaximiz(ed|es|e|ing|ation)\b",
    r"\bfinaliz(ed|es|e|ing|ation)\b",
    r"\bcustomiz(ed|es|e|ing|ation)\b",
    r"\bstandardiz(ed|es|e|ing|ation)\b",
    r"\bemphasiz(ed|es|e|ing)\b",
    r"\butiliz(ed|es|e|ing|ation)\b",
    r"\boptimiz(ed|es|e|ing|ation)\b",
    r"\banalyz(ed|es|e|ing)\b",
    r"\bcolor(s|ed|ing|ful)?\b",
    r"\bbehavior(s|al)?\b",
    r"\bneighbor(s|hood|ing)?\b",
    r"\bhonor(s|ed|ing|able)?\b",
    r"\bfavor(s|ed|ing|able|ably|ite|ites)?\b",
    r"\blabor(s|ed|ing)?\b",
    r"\b(rigor|vigor|valor|flavor|savor|vapor|odor|tumor|demeanor|candor|ardor|clamor|splendor|harbor|parlor|rumor|savior|endeavor|fervor|glamor)(s|ed|ing|able)?\b",
    r"\bcenter(s|ed)?\b",
    r"\btheater(s)?\b",
    r"\bfiber(s)?\b",
    r"\bliter(s)?\b",
    r"\bmeter(s)?\b",
    r"\btraveling\b",
    r"\bmodeling\b",
    r"\bcanceled\b",
    r"\b(modeled|labeled|traveled|signaled|fueled|funneled|counseled|leveled|totaled|marveled)\b",
    r"\blabeling\b",
    r"\b(hemo\w*|hemato\w*|anemi\w*|leukemi\w*|pediatric\w*|orthopedic\w*|edema|esophag\w*|fetal|fetus|estrogen|celiac)\b",
    r"\bcatalog(s|ed|ing)?\b",
    r"\bdialog(s)?\b",
    r"\banalog(s)?\b",
    r"\bdefense\b",
    r"\boffense\b",
    r"\bjudgment(s)?\b",  # US
]

CONTRACTIONS = [
    r"\b(don't|doesn't|didn't|won't|wouldn't|couldn't|shouldn't|can't|cannot)\b",
    r"\b(it's|that's|there's|here's|what's|who's)\b",
    r"\b(i'm|i'll|i've|i'd)\b",
    r"\b(you're|you'll|you've|you'd)\b",
    r"\b(we're|we'll|we've|we'd)\b",
    r"\b(they're|they'll|they've|they'd)\b",
    r"\b(he's|she's|he'd|she'd|he'll|she'll)\b",
    r"\b(isn't|aren't|wasn't|weren't|hasn't|haven't|hadn't)\b",
    r"\b(let's)\b",
]

# Precompiled once at import. The dialect-ending and contraction scans run on
# every draft, so compiling these (76 + 40 + 9 patterns) per call was pure waste.
AUSE_ENDING_RES = [re.compile(p, re.IGNORECASE) for p in AUSE_ENDINGS]
US_ENDING_RES = [re.compile(p, re.IGNORECASE) for p in US_ENDINGS]
CONTRACTION_RES = [re.compile(p, re.IGNORECASE) for p in CONTRACTIONS]


# ---------------------------------------------------------------------------
# Shared helpers. These scan/strip idioms recur across many checks; keeping one
# copy each stops the checks drifting apart.
# ---------------------------------------------------------------------------

WORD_RE = re.compile(r"\b[\w'-]+\b")

# The antithesis ("binary contrast") tic, shared by structural_tell_count and
# binary_contrast_density so the two views always measure the same thing.
BINARY_INLINE_RE = re.compile(r"\b\w+,\s+not\s+\w+", re.IGNORECASE)
CLASSIC_BINARY_RE = re.compile(
    r"(?:it's|its)\s+not\s+(?:about|because|that)\s+.{3,40}?,?\s*(?:it's|its)\s+(?:about|because|that)",
    re.IGNORECASE,
)
NOT_JUST_RE = re.compile(
    r"\bnot\s+(?:just|only)\s+.{2,40}?,?\s+but(?:\s+also)?\b", re.IGNORECASE
)
# Negated-copula antithesis: "the factor isn't X, it's Y". Same negate-then-reveal
# move as the classic form, but built on isn't/aren't/wasn't rather than "it's not",
# so the classic regex misses it. Length-bounded to avoid runaway matches.
NEGATED_COPULA_RE = re.compile(
    r"\b(?:isn't|isnt|is not|aren't|arent|are not|wasn't|wasnt|was not|weren't|werent|were not)\b"
    r"[^.?!]{2,40}?,\s*(?:it's|its|that's|thats|they're|theyre)\b",
    re.IGNORECASE,
)


# Negation pivot: "less about X, more about Y" (impeccable.design STYLE.md). Same
# antithesis move as the binary contrast, a different surface the other regexes miss.
NEG_PIVOT_RE = re.compile(r"\bless about\b.{2,40}?\bmore about\b", re.IGNORECASE)

# Triple/template tells scanned by structural_tell_count, compiled once.
TRIPLE_AND_RE = re.compile(
    r"\b(\w+(?:\s+\w+){0,2}),\s+(\w+(?:\s+\w+){0,2}),\s+and\s+(\w+(?:\s+\w+){0,2})\b"
)
TRIPLE_NO_AND_RE = re.compile(
    r"(\w+(?:\s+\w+){0,2}),\s+(\w+(?:\s+\w+){0,2}),\s+(\w+(?:\s+\w+){0,2})(?=[.!?])"
)
SENTENCE_TEMPLATE_RE = re.compile(
    r"The\s+(?:best\s+)?\w+s?\s+don'?t\s+\w+[^.]*\.\s+They\s+\w+"
)
# Transition-slop connectors. Module-level so other passes can reuse the list.
TRANSITION_SLOP = [
    "but here's where",
    "and here's the kicker",
    "now for the surprising",
    "let me put it this way",
    "here's what's interesting",
]
TRANSITION_SLOP_RES = [re.compile(p, re.IGNORECASE) for p in TRANSITION_SLOP]


def _binary_contrast_hits(draft):
    """Return (inline, classic, not_just, negated_copula, neg_pivot) match lists."""
    return (
        BINARY_INLINE_RE.findall(draft),
        CLASSIC_BINARY_RE.findall(draft),
        NOT_JUST_RE.findall(draft),
        NEGATED_COPULA_RE.findall(draft),
        NEG_PIVOT_RE.findall(draft),
    )


def _strip_frontmatter(text):
    """Drop a leading --- ... --- YAML frontmatter block."""
    return re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)


def _strip_frontmatter_headers(text):
    """Drop frontmatter and ATX headers (including the no-space #Heading form)."""
    return re.sub(r"^#+\s*.*$", "", _strip_frontmatter(text), flags=re.MULTILINE)


@lru_cache(maxsize=None)
def _term_re(term):
    """Compiled word-boundary matcher for a slop/register term, cached across calls."""
    return re.compile(rf"\b{re.escape(term)}\b")


def _count_terms(lower, terms):
    """Word-boundary occurrence counts for each term in an already-lowercased draft.

    Returns a Counter of present terms to their counts (absent terms omitted),
    matching the per-term assignment the slop/register checks rely on.
    """
    found = Counter()
    for term in terms:
        n = len(_term_re(term).findall(lower))
        if n:
            found[term] = n
    return found


def _spelling_leaks(draft, patterns):
    """Flat list of every match across a list of compiled dialect-ending patterns."""
    hits = []
    for pattern in patterns:
        hits.extend(pattern.findall(draft))
    return hits


def _runs_of_similar(values, predicate, window=3):
    """Count sliding windows of `window` consecutive values that satisfy predicate."""
    return sum(
        1 for i in range(len(values) - window + 1) if predicate(values[i : i + window])
    )


@lru_cache(maxsize=32)
def _sentences(draft):
    """Split prose into sentences, dropping frontmatter, headers, and bullets' markers.

    Returns a tuple so the cached result is immutable. The header strip also
    handles the no-space ATX form (#Heading), and markers are stripped from both
    ends so a trailing bold marker (fix.**) does not leak into the token count.
    """
    text = _strip_frontmatter_headers(draft)
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    cleaned = []
    for p in parts:
        p = p.strip().strip("-*>•").strip().strip("\"'“”‘’")
        if len(p.split()) >= 2:
            cleaned.append(p)
    return tuple(cleaned)


def em_dash_count(draft):
    count = draft.count("—")  # em dash
    return {
        "count": count,
        "pass": count == 0,
        "details": f"{count} em dash(es) found" if count else "no em dashes",
    }


def en_dash_count(draft, allow_in_ranges=True):
    """Count en dashes. If allow_in_ranges, skip those between digits (2015–18)."""
    all_ens = draft.count("–")
    if not allow_in_ranges:
        return {
            "total": all_ens,
            "non_range_count": all_ens,
            "count": all_ens,
            "pass": all_ens == 0,
            "details": f"{all_ens} en dash(es) (ranges not exempt)",
        }
    # Non-range use = a spaced en dash doing em-dash/pause work ("result – a fix").
    # Unspaced en dashes join range endpoints (2015–18, Mon–Fri) and are allowed.
    bad = len(re.findall(r"(?<=\s)–|–(?=\s)", draft))
    return {
        "total": all_ens,
        "non_range_count": bad,
        "count": bad,
        "pass": bad == 0,
        "details": f"{bad} non-range en dash(es); {all_ens - bad} in ranges (allowed)",
    }


def spaced_hyphen_dash(draft):
    """The em dash substitute: a spaced hyphen doing dash work mid-sentence.

    'the result - a cleaner pipeline - shipped' carries the same theatrical-pause
    rhythm as an em dash and reads as a dodge. List bullets at line start are
    excluded by the lookbehind.
    """
    matches = re.findall(r"(?<=[a-zA-Z,)]) - (?=[a-zA-Z(])", draft)
    return {
        "count": len(matches),
        "pass": len(matches) == 0,
        "details": f"{len(matches)} spaced hyphen(s) used as dash"
        if matches
        else "none",
    }


def curly_quote_count(draft, medium="plain"):
    """Medium-aware quote check.

    plain (Slack, email, markdown): curly quotes fail; straight is the human default.
    docx (word-processed deliverables): curly is the human default (autocorrect
    produces it); only MIXING curly and straight apostrophes/quotes fails.
    """
    curly = sum(draft.count(c) for c in ["“", "”", "‘", "’"])
    straight = draft.count('"') + draft.count("'")
    if medium == "docx":
        mixed = curly > 0 and straight > 0
        return {
            "count": curly,
            "straight_count": straight,
            "pass": not mixed,
            "details": (
                "mixed curly and straight quotes in a docx medium"
                if mixed
                else "docx medium: curly quotes are the human default here"
            ),
        }
    return {
        "count": curly,
        "pass": curly == 0,
        "details": f"{curly} curly quote character(s)" if curly else "no curly quotes",
    }


def severity_1_slop_count(draft):
    """Count Severity 1 slop words (case-insensitive, word-boundary)."""
    lower = draft.lower()
    found = _count_terms(lower, SEVERITY_1_SLOP)
    # 'landscape' is severity-1 slop only in its metaphorical sense (see
    # LANDSCAPE_METAPHOR_RE). Literal uses are left alone so this hard check
    # does not false-fire.
    metaphorical = len(LANDSCAPE_METAPHOR_RE.findall(lower))
    if metaphorical:
        found["landscape(metaphor)"] = metaphorical
    total = sum(found.values())
    return {
        "count": total,
        "pass": total == 0,
        "found": dict(found),
        "details": f"Sev 1 slop found: {dict(found)}" if found else "clean",
    }


def severity_2_3_slop_count(draft):
    found = _count_terms(draft.lower(), SEVERITY_2_3_SLOP)
    total = sum(found.values())
    return {
        "count": total,
        "pass": total <= 2,  # fingerprint budget: 0-2 per piece
        "found": dict(found),
        "details": f"Sev 2-3 slop count: {total}",
    }


def slop_opener_check(draft):
    """Check if the draft opens with a slop opener."""
    first_chunk = draft.strip()[:200].lower()
    hit = None
    for opener in SLOP_OPENERS:
        if first_chunk.startswith(opener) or f"\n{opener}" in first_chunk[:250]:
            hit = opener
            break
    return {
        "pass": hit is None,
        "opener_found": hit,
        "details": f'Slop opener: "{hit}"'
        if hit
        else "no slop opener in first 200 chars",
    }


def i_this_openers(draft, formal=False):
    """Count sentences opening with 'I' or 'This'.

    Per the fingerprint's absolute rules 1 and 2, the ban is scoped to FORMAL
    channels (cover letters, formal external email). Elsewhere these openers are
    natural and restructuring every one becomes its own tic, so the check is
    advisory outside formal channels.
    """
    count_i = 0
    count_this = 0
    for s in _sentences(draft):
        if re.match(r"^I\b", s):
            count_i += 1
        elif re.match(r"^This\b", s):
            count_this += 1
    total = count_i + count_this
    return {
        "count": total,
        "i_openers": count_i,
        "this_openers": count_this,
        "formal_channel": formal,
        "pass": (total == 0) if formal else True,
        "advisory": not formal,
        "details": (
            f"{count_i} 'I' opener(s), {count_this} 'This' opener(s)"
            + ("" if formal else " (advisory: not a formal channel)")
        ),
    }


def sentence_length_profile(draft):
    """Burstiness tripwire: runs of 3+ consecutive sentences within 5 words of
    each other in length. Also reports the range for the fingerprint targets
    (3x ratio, one sentence under 8 words, one over 20) without failing on them;
    those are tripwires, not quotas."""
    lengths = [len(s.split()) for s in _sentences(draft)]
    if len(lengths) < 3:
        return {
            "sentences": len(lengths),
            "runs_of_3": 0,
            "pass": True,
            "advisory": True,
            "details": "too short to profile",
        }
    runs = _runs_of_similar(lengths, lambda w: max(w) - min(w) <= 5)
    ratio = round(max(lengths) / max(min(lengths), 1), 1)
    return {
        "sentences": len(lengths),
        "min_words": min(lengths),
        "max_words": max(lengths),
        "range_ratio": ratio,
        "runs_of_3": runs,
        "pass": runs == 0,
        "advisory": True,
        "details": (
            f"{len(lengths)} sentences, {min(lengths)}-{max(lengths)} words "
            f"(ratio {ratio}x), {runs} run(s) of 3 similar-length sentences"
        ),
    }


def paragraph_shape(draft):
    """Advisory: three or more consecutive paragraphs of near-identical length
    is a uniformity tell. Short drafts pass automatically."""
    text = _strip_frontmatter(draft)
    paras = [p for p in re.split(r"\n\s*\n", text) if len(p.split()) >= 15]
    counts = [len(p.split()) for p in paras]
    if len(counts) < 3:
        return {
            "paragraphs": len(counts),
            "similar_runs": 0,
            "pass": True,
            "advisory": True,
            "details": "too few paragraphs to profile",
        }
    runs = _runs_of_similar(counts, lambda w: max(w) <= min(w) * 1.25)
    return {
        "paragraphs": len(counts),
        "word_counts": counts,
        "similar_runs": runs,
        "pass": runs == 0,
        "advisory": True,
        "details": f"{len(counts)} paragraphs, {runs} run(s) of 3 similar-length paragraphs",
    }


def ause_count(draft):
    """Count distinct AusE spellings appearing in the draft.

    Tripwire, not a quota: a short natural piece can have zero -ise words.
    Treat as advisory in evals; never pad a draft to lift this number."""
    hits = {pattern for pattern in AUSE_ENDING_RES if pattern.search(draft)}
    return {
        "count": len(hits),
        "pass": len(hits) >= 2,
        "advisory": True,
        "patterns_matched": len(hits),
        "details": f"{len(hits)} distinct AusE spelling pattern(s) found (tripwire, not quota)",
    }


def us_spelling_clean(draft):
    """For US-tagged content: confirm no AusE leakage."""
    ause_hits = _spelling_leaks(draft, AUSE_ENDING_RES)
    return {
        "pass": len(ause_hits) == 0,
        "ause_leaks": len(ause_hits),
        "details": f"{len(ause_hits)} AusE spelling(s) in US content"
        if ause_hits
        else "clean",
    }


def ause_spelling_clean(draft):
    """For AU-tagged content: confirm no US leakage on key endings."""
    us_hits = _spelling_leaks(draft, US_ENDING_RES)
    return {
        "pass": len(us_hits) == 0,
        "us_leaks": len(us_hits),
        "details": f"{len(us_hits)} US spelling(s) in AU content"
        if us_hits
        else "clean",
    }


def contraction_types(draft):
    # Normalise curly apostrophes to straight: in docx, curly (U+2019) is the human
    # default, but the CONTRACTIONS patterns are written with straight apostrophes.
    normalised = draft.replace("’", "'")
    types_found = sum(1 for pattern in CONTRACTION_RES if pattern.search(normalised))
    return {
        "distinct_types": types_found,
        "pass": types_found >= 3,
        "advisory": True,
        "details": f"{types_found} distinct contraction type(s) (tripwire, not quota)",
    }


def word_count(draft):
    # strip markdown frontmatter, headers, bullets
    cleaned = _strip_frontmatter_headers(draft)
    words = WORD_RE.findall(cleaned)
    return {
        "count": len(words),
        "details": f"{len(words)} words",
    }


def structural_tell_count(draft, contrast_hits=None):
    """Heuristic count of structural tells. Not exhaustive and noisy at the
    edges (the triple regex both over- and under-fires); treat as a flag for a
    human re-read, not as ground truth.

    June 2026: no longer truncates the binary-inline hit list (a long doc used
    to hide forty contrasts behind a reported three), adds the 'not just X but
    Y' / 'not only X but also Y' form, and the pass threshold is now density-
    aware: short pieces keep the <=1 absolute budget, long docs are graded on
    contrasts per 1000 words by `binary_contrast_density`. See that function for
    the scaled view."""
    hits = []

    # Binary contrasts (inline / classic / not-just / negated-copula) - shared with
    # binary_contrast_density so both views measure the same thing. all_checks passes
    # the hits in so the five-regex scan runs once per draft, not once per view.
    binary_inline, classic_binary, not_just, negated_copula, neg_pivot = (
        contrast_hits if contrast_hits is not None else _binary_contrast_hits(draft)
    )
    hits.extend([f'binary_inline: "{m}"' for m in binary_inline])
    if classic_binary:
        hits.append(f"classic_binary_contrast: {len(classic_binary)}")
    if not_just:
        hits.append(f"not_just_but: {len(not_just)}")
    if negated_copula:
        hits.append(f"negated_copula_contrast: {len(negated_copula)}")
    if neg_pivot:
        hits.append(f"negation_pivot: {len(neg_pivot)}")

    # Triple (three items separated by commas, same structure)
    # "X, Y, and Z" where X, Y, Z are short phrases of similar length.
    triples = TRIPLE_AND_RE.findall(draft)
    if len(triples) >= 2:
        hits.append(f"triples: {len(triples)} (threshold 2+)")
    # Triple without "and": three short parallel comma-separated phrases closing a
    # sentence ("Ship fast, learn deeply, repeat endlessly."). The rhythmic LinkedIn
    # triple the with-"and" regex misses. Drop matches whose items start with a
    # connector, which are usually the tail of a longer Oxford list, not a triple.
    triples_no_and = TRIPLE_NO_AND_RE.findall(draft)
    triples_no_and = [
        t
        for t in triples_no_and
        if not any(p.split()[0].lower() in ("and", "or", "but", "nor") for p in t)
    ]
    if triples_no_and:
        hits.append(f"triple_no_and: {len(triples_no_and)}")

    # Transition slop
    for pat in TRANSITION_SLOP_RES:
        if pat.search(draft):
            hits.append(f'transition_slop: "{pat.pattern}"')

    # Sentence template: "The [X] don't Y. They Z."
    template = SENTENCE_TEMPLATE_RE.search(draft)
    if template:
        hits.append("sentence_template")

    return {
        "count": len(hits),
        "pass": len(hits) <= 1,
        "hits": hits,
        "details": f"{len(hits)} structural tell(s): {hits}",
    }


def binary_contrast_density(draft, contrast_hits=None):
    """Scale-aware view of the antithesis tic ('X, not Y', 'it's not X it's Y',
    'not just X but Y'). The per-piece budget breaks down on long documents:
    one contrast per section across sixteen sections is sixteen across the doc,
    and every one reads as a tic. This measures contrasts per 1000 words so a
    30-page memo gets graded on rate, not on an absolute count tuned for a tweet.

    Advisory: the script can't tell a load-bearing contrast (a the user signature)
    from an empty one, so this flags density for a human or the adversarial
    reviewer to adjudicate. Threshold: more than 1 contrast per 600 words on a
    piece over 300 words."""
    inline, classic, not_just, negated_copula, neg_pivot = (
        contrast_hits if contrast_hits is not None else _binary_contrast_hits(draft)
    )
    total = len(inline) + len(classic) + len(not_just) + len(negated_copula) + len(neg_pivot)
    words = len(WORD_RE.findall(draft))
    per_1000 = round(total / words * 1000, 2) if words else 0
    # Short pieces: any more than one is suspect. Long pieces: grade on density.
    if words < 300:
        ok = total <= 1
    else:
        ok = per_1000 <= 1.67  # ~1 per 600 words
    return {
        "count": total,
        "per_1000_words": per_1000,
        "words": words,
        "inline": len(inline),
        "classic": len(classic),
        "not_just": len(not_just),
        "negated_copula": len(negated_copula),
        "neg_pivot": len(neg_pivot),
        "pass": ok,
        "advisory": True,
        "details": f"{total} binary contrast(s), {per_1000} per 1000 words "
        f"(inline {len(inline)}, classic {len(classic)}, "
        f"not-just {len(not_just)}, negated-copula {len(negated_copula)})",
    }


def fragment_colon_headers(draft):
    """The fragment-then-colon drumbeat: 'The recommendation.' / 'The ask.' /
    'The key finding:' used as a section opener. Punchy once, a template by the
    third. Flags a cluster of three or more short label-fragments (1-4 words,
    ending in a full stop or colon, followed by a capitalised sentence), not the
    single deliberate beat."""
    # Sentence- or line-initial short fragment ending in . or : then a capital.
    pattern = re.compile(
        r"(?:^|(?<=[.!?])\s+|\n)\*{0,2}((?:The\s+)?[A-Z][a-z]+(?:\s+\w+){0,2})([.:])\*{0,2}(?=\s+[A-Z*])",
        re.MULTILINE,
    )
    # A colon is an unambiguous label signal (cap 4 words). A full stop is ambiguous,
    # so only count it as a label when very short (<=2 words, "The ask."); longer
    # period fragments are ordinary terse sentences ("Tests passed cleanly."), not a
    # drumbeat, and must not false-fire here.
    hits = []
    for m in pattern.finditer(draft):
        label, terminator = m.group(1), m.group(2)
        words = len(label.split())
        if (terminator == ":" and words <= 4) or (terminator == "." and words <= 2):
            hits.append(label)
    return {
        "count": len(hits),
        "pass": len(hits) < 3,
        "advisory": True,
        "examples": hits[:6],
        "details": f"{len(hits)} fragment-colon label opener(s)"
        + (f": {hits[:6]}" if len(hits) >= 3 else " (cluster threshold 3)"),
    }


def self_narrated_honesty(draft):
    """Meta-candour: the writing captioning its own honesty ('Pipeline honesty:',
    'the honest version of', 'an honest label', 'to be honest'). Models reach for
    it to earn trust; people just are candid. Hard check, like vocabulary slop:
    delete the caption, keep the claim."""
    found = _count_terms(draft.lower(), META_CANDOUR)
    labels = META_CANDOUR_LABEL_RE.findall(draft)
    if labels:
        found["<Noun> honesty: label"] = len(labels)
    total = sum(found.values())
    return {
        "count": total,
        "pass": total == 0,
        "found": dict(found),
        "details": f"Self-narrated honesty: {dict(found)}" if found else "clean",
    }


def academic_register(draft):
    """Register-paper verbs and phrases ('operationalises', 'stems from',
    'predicated on', 'constitutes', 'indicative of'). Copula avoidance's fancier
    cousin. One or two in a long piece is tolerable; clustering is a rewrite.
    Threshold mirrors severity-2/3 slop: pass at <= 2."""
    found = _count_terms(draft.lower(), ACADEMIC_REGISTER)
    total = sum(found.values())
    return {
        "count": total,
        "pass": total <= 2,
        "found": dict(found),
        "details": f"Academic-register count: {total} {dict(found)}"
        if found
        else "clean",
    }


def burstiness(draft):
    """Coefficient of variation of sentence length (stdev / mean). Burstiness is
    one of the two axes AI detectors actually use: human prose mixes short and
    long sentences, AI prose clusters around the mean. Low CoV reads as machine.

    Advisory and diagnostic only. Never a target to pad to (the skill bans
    writing engineered to pass a detector). Flags a piece with >= 8 sentences
    and CoV below 0.45 for a human look at rhythm. Short pieces auto-pass."""
    lengths = [len(s.split()) for s in _sentences(draft)]
    if len(lengths) < 8:
        return {
            "sentences": len(lengths),
            "cov": None,
            "pass": True,
            "advisory": True,
            "details": "too short to score burstiness",
        }
    mean = sum(lengths) / len(lengths)
    var = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    cov = round((var**0.5) / mean, 3) if mean else 0
    return {
        "sentences": len(lengths),
        "mean_words": round(mean, 1),
        "cov": cov,
        "pass": cov >= 0.45,
        "advisory": True,
        "details": f"sentence-length CoV {cov} over {len(lengths)} sentences "
        f"(target >= 0.45; lower means too uniform)",
    }


def contains_any(draft, patterns, case_insensitive=True):
    """Helper: check if any pattern appears in draft."""
    text = draft.lower() if case_insensitive else draft
    for p in patterns:
        check = p.lower() if case_insensitive else p
        if check in text:
            return True
    return False


def number_count(draft):
    """Count standalone numbers (heuristic for specificity)."""
    # No trailing \b: it sits between '%' (non-word) and the next char, which fails
    # after a percent, so '%' would be dropped from the match and 100% read as 100.
    numbers = re.findall(r"\b\d+(?:[.,]\d+)?%?", draft)
    return {
        "count": len(numbers),
        "details": f"{len(numbers)} numbers found",
    }


def all_checks(draft, audience_tag="aus", medium="plain", formal=False):
    """Run every check. Returns a dict of results.

    medium: 'plain' (Slack/email/markdown) or 'docx' (word-processed deliverable).
    formal: True for cover letters and formal external email, where the I/This
    opener ban is hard rather than advisory.
    """
    draft = strip_sweep_ignore(draft)
    # Scan the five binary-contrast regexes once and share with both views.
    contrast_hits = _binary_contrast_hits(draft)
    results = {
        "em_dash": em_dash_count(draft),
        "en_dash_non_range": en_dash_count(draft, allow_in_ranges=True),
        "spaced_hyphen_dash": spaced_hyphen_dash(draft),
        "curly_quotes": curly_quote_count(draft, medium=medium),
        "severity_1_slop": severity_1_slop_count(draft),
        "severity_2_3_slop": severity_2_3_slop_count(draft),
        "slop_opener": slop_opener_check(draft),
        "i_this_openers": i_this_openers(draft, formal=formal),
        "ause_visible": ause_count(draft),
        "contractions": contraction_types(draft),
        "word_count": word_count(draft),
        "structural_tells": structural_tell_count(draft, contrast_hits),
        "binary_contrast_density": binary_contrast_density(draft, contrast_hits),
        "fragment_colon_headers": fragment_colon_headers(draft),
        "self_narrated_honesty": self_narrated_honesty(draft),
        "academic_register": academic_register(draft),
        "sentence_profile": sentence_length_profile(draft),
        "burstiness": burstiness(draft),
        "paragraph_shape": paragraph_shape(draft),
        "numbers": number_count(draft),
    }
    # Tag-specific spelling gate. US-tagged content is checked for AusE leakage;
    # everything else (AusE, UK, internal, investor-mixed, public, or any unknown
    # tag) defaults to the AusE cleanliness check, matching cultural-calibration's
    # "default AusE". Defaulting stops a non-standard tag (e.g. 'seed-investors-mixed'
    # or 'public-pm-tech') silently skipping the gate and making an assertion
    # unresolvable, which used to cap those evals below pass regardless of the draft.
    if audience_tag and audience_tag.startswith("us"):
        results["us_spelling_clean"] = us_spelling_clean(draft)
    else:
        results["ause_spelling_clean"] = ause_spelling_clean(draft)

    # Overall pass: advisory checks report but don't count against the summary.
    hard = {k: r for k, r in results.items() if "pass" in r and not r.get("advisory")}
    advisory = {k: r for k, r in results.items() if "pass" in r and r.get("advisory")}
    passed = sum(1 for r in hard.values() if r.get("pass") is True)
    failed = [k for k, r in hard.items() if r.get("pass") is False]
    advisory_flagged = [k for k, r in advisory.items() if r.get("pass") is False]
    wc = results["word_count"]["count"]
    # Structural density dashboard: tells per 1000 words, for the long-form pass.
    density = {
        "binary_contrasts_per_1000": results["binary_contrast_density"][
            "per_1000_words"
        ],
        "fragment_colon_labels": results["fragment_colon_headers"]["count"],
        "self_narrated_honesty": results["self_narrated_honesty"]["count"],
        "academic_register": results["academic_register"]["count"],
        "burstiness_cov": results["burstiness"]["cov"],
        "structural_tell_total": results["structural_tells"]["count"],
    }
    results["_summary"] = {
        "word_count": wc,
        "long_form": wc >= 1500,
        "passed": passed,
        "total_checks": len(hard),
        "pass_rate": passed / len(hard) if hard else 0,
        "failed": failed,
        "advisory_flagged": advisory_flagged,
        "structural_density": density,
    }
    return results


if __name__ == "__main__":
    import sys
    import json as json_lib

    if len(sys.argv) < 2:
        print(
            "Usage: python writing_checks.py <draft_file> [audience_tag] [medium] [formal]"
        )
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        draft = f.read()
    tag = sys.argv[2] if len(sys.argv) > 2 else "aus"
    medium = sys.argv[3] if len(sys.argv) > 3 else "plain"
    formal = len(sys.argv) > 4 and sys.argv[4].lower() in ("formal", "true", "1")
    results = all_checks(draft, tag, medium=medium, formal=formal)
    print(json_lib.dumps(results, indent=2, default=str))
