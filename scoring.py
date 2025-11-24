# scoring.py
"""
Scoring logic for Nirmaan Self-Introduction Case Study
(NO Java, NO LanguageTool API — FULLY OFFLINE)

Uses:
- PySpellChecker for grammar errors
- VADER for sentiment
- Rule-based scoring EXACTLY matching rubric
"""

import re
from spellchecker import SpellChecker
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

spell = SpellChecker()
sentiment_analyzer = SentimentIntensityAnalyzer()

FILLER_WORDS = {
    "um", "uh", "like", "you know", "so", "actually", "basically",
    "right", "i mean", "well", "kinda", "sort of", "okay", "ok",
    "hmm", "ah"
}

# ===== TOKENS =====

def simple_tokens(text: str):
    return re.findall(r"\b[\w']+\b", text.lower())

def word_count(text: str):
    return len(simple_tokens(text))


# ===== CONTENT & STRUCTURE (40) =====

def salutation_score(text: str) -> int:
    t = text.lower()

    if "excited to introduce" in t or "feeling great" in t:
        return 5
    if any(k in t for k in ["good morning", "good afternoon", "good evening", "good day", "hello everyone"]):
        return 4
    if t.startswith("hi") or t.startswith("hello") or "hi " in t or "hello " in t:
        return 2
    return 0

# keyword helpers
def has_name(text): return "my name is" in text.lower() or "myself " in text.lower() or re.search(r"\bi am [A-Z][a-z]+", text)
def has_age(text): return re.search(r"\b\d{1,2} (years old|year old|yrs old)\b", text.lower())
def has_school(text): return any(k in text.lower() for k in ["class", "grade", "standard", "school"])
def has_family(text): return any(k in text.lower() for k in ["family", "mother", "father", "parents", "brother", "sister"])
def has_hobbies(text): return any(k in text.lower() for k in ["i like to", "i love to", "i enjoy", "my hobby", "my hobbies"])
def has_about_family(text): return "about my family" in text.lower()
def has_origin(text): return any(k in text.lower() for k in ["i am from", "i'm from", "i live in", "we live in"])
def has_ambition(text): return any(k in text.lower() for k in ["my ambition", "my goal", "my dream", "i want to be"])
def has_fun_fact(text): return "fun fact" in text.lower() or "one thing people" in text.lower()
def has_strengths(text): return any(k in text.lower() for k in ["my strength", "achievement", "i am good at"])

def keyword_presence_score(text):
    score = 0
    
    must = [has_name, has_age, has_school, has_family, has_hobbies]
    for c in must:
        if c(text): score += 4

    good = [has_about_family, has_origin, has_ambition, has_fun_fact, has_strengths]
    for c in good:
        if c(text): score += 2

    return min(score, 30)

def flow_score(text):
    t = text.lower()

    def idx(phrases):
        found = [t.find(p) for p in phrases if p in t]
        return min(found) if found else -1

    sal = idx(["good morning", "hello", "hi"])
    basic = idx(["my name is", "myself", "i am "])
    close = idx(["thank you", "thanks"])

    if sal != -1 and basic != -1 and close != -1 and sal <= basic <= close:
        return 5
    if basic != -1 and close != -1 and basic <= close:
        return 5
    return 0

def content_structure_score(text):
    sal = salutation_score(text)
    kw = keyword_presence_score(text)
    fl = flow_score(text)
    total = min(sal + kw + fl, 40)
    return total, {"salutation": sal, "keywords": kw, "flow": fl}


# ===== SPEECH RATE (10) =====

def speech_rate_score(text, duration_sec):
    wc = word_count(text)
    if duration_sec <= 0:
        return 0, wc, 0

    wpm = wc / (duration_sec / 60)

    if wpm > 161: s = 2
    elif 141 <= wpm <= 160: s = 6
    elif 111 <= wpm <= 140: s = 10
    elif 81 <= wpm <= 110: s = 6
    else: s = 2

    return s, wc, wpm


# ===== LANGUAGE & GRAMMAR (20) =====

def grammar_score(text):
    tokens = simple_tokens(text)
    misspelled = spell.unknown(tokens)
    err_count = len(misspelled)

    wc = max(1, len(tokens))
    errors_per_100 = (err_count * 100) / wc
    grammar_raw = 1 - min(errors_per_100 / 10, 1)

    if grammar_raw > 0.9: s = 10
    elif grammar_raw >= 0.7: s = 8
    elif grammar_raw >= 0.5: s = 6
    elif grammar_raw >= 0.3: s = 4
    else: s = 2

    return s, grammar_raw, errors_per_100, err_count

def vocab_ttr_score(text):
    tokens = simple_tokens(text)
    if not tokens:
        return 0, 0.0
    ttr = len(set(tokens)) / len(tokens)
    if ttr >= 0.9: s = 10
    elif ttr >= 0.7: s = 8
    elif ttr >= 0.5: s = 6
    elif ttr >= 0.3: s = 4
    else: s = 2
    return s, ttr


# ===== CLARITY (15) =====

def clarity_score(text):
    tokens = simple_tokens(text)
    wc = max(1, len(tokens))
    t = text.lower()

    filler_count = 0
    for fw in FILLER_WORDS:
        if " " in fw:
            filler_count += t.count(fw)
        else:
            filler_count += sum(1 for tok in tokens if tok == fw)

    rate = filler_count * 100 / wc

    if rate <= 3: s = 15
    elif rate <= 6: s = 12
    elif rate <= 9: s = 9
    elif rate <= 12: s = 6
    else: s = 3

    return s, filler_count, rate


# ===== ENGAGEMENT (15) =====

def engagement_score(text):
    vs = sentiment_analyzer.polarity_scores(text)
    pos = vs["pos"]

    if pos >= 0.9: s = 15
    elif pos >= 0.7: s = 12
    elif pos >= 0.5: s = 9
    elif pos >= 0.3: s = 6
    else: s = 3

    return s, pos, vs


# ===== MAIN =====

def score_transcript(text: str, duration_sec: float):
    content_total, content_detail = content_structure_score(text)
    speech_s, wc, wpm = speech_rate_score(text, duration_sec)
    grammar_s, grammar_raw, err100, err_count = grammar_score(text)
    vocab_s, ttr = vocab_ttr_score(text)
    clarity_s, filler_count, filler_rate = clarity_score(text)
    engagement_s, pos, vader = engagement_score(text)

    lang_total = grammar_s + vocab_s

    overall = content_total + speech_s + lang_total + clarity_s + engagement_s

    return {
        "overall_score": round(overall, 2),

        "content_structure": {
            "total": content_total,
            **content_detail
        },

        "speech_rate": {
            "score": speech_s,
            "word_count": wc,
            "wpm": round(wpm, 2)
        },

        "language_grammar": {
            "total": lang_total,
            "grammar_score": grammar_s,
            "grammar_raw": round(grammar_raw, 3),
            "errors_per_100": round(err100, 2),
            "error_count": err_count,
            "vocab_score": vocab_s,
            "ttr": round(ttr, 3)
        },

        "clarity": {
            "score": clarity_s,
            "filler_count": filler_count,
            "filler_rate": round(filler_rate, 2)
        },

        "engagement": {
            "score": engagement_s,
            "positive_prob": round(pos, 3),
            "vader_scores": vader
        }
    }
