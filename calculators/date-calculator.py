#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────────────────────
# DATE NUMEROLOGY CALCULATOR
#
# Combines three calculation modes behind one arrow-key menu:
#   • Date Calculator   -- single date, results printed to the terminal
#   • Month Calculator  -- every day in a chosen month, printed to the terminal
#   • Year Calculator   -- every day in a chosen year, printed to the terminal,
#     saved to ~/calendar-numerology-<year>.txt, AND plotted as an
#     interactive, zoomable line graph (highs & lows of the Greek ⊕ Hebrew
#     Bone'eh synthesis number) saved to
#     ~/calendar-numerology-<year>-graph.html
#
# Five numerological methods applied to any date:
#
#   1. GREEK PYTHAGOREAN (Modern Pythagorean Numerology Method)
#      Each component (month, day, year) reduced to 1-9 individually,
#      then summed and reduced again.  Source: Numerology Wikipedia --
#      "Pythagorean method" section (Latin letters assigned 1-9, "a kind
#      of place-value ... as do the ancient Hebrew and Greek systems").
#      NOTE: this is the modern numerology convention, not ancient
#      isopsephy, which kept raw Greek letter totals unreduced (the name
#      of Jesus in Greek = 888; the Pompeii graffito "phi mu epsilon
#      (545)" -- Gematria Wikipedia, Britannica).
#
#   Methods 2 and 3 write the date the way Hebrew writes numbers -- with
#   letters (Gematria Wikipedia: Hebrew letters used as numerals from
#   78 BCE; Mathers Table: thousands are "denoted by a larger letter")
#   -- and apply the documented gematria methods to those letters.
#
#   2. HEBREW STANDARD  (Mispar Hechrachi -- absolute value)
#      Every letter keeps its full standard value (1-9, 10-90, 100-400;
#      e.g. 28 = Kaf 20 + Het 8, 2026 = Bet 2000 + Kaf 20 + Vav 6).
#      A Hebrew numeral's absolute value is the number itself, so the
#      total is month + day + year.
#
#   3. MISPAR KATAN  (small value)
#      Each letter's value with its zeros truncated (Kaf 20 -> 2,
#      Tav 400 -> 4, Bet-as-2000 -> 2), summed.  Source: Gematria
#      Wikipedia -- "calculates the value of each letter, but truncates
#      all of the zeros."  This equals the date's digit sum, except that
#      Hebrew writes 15 and 16 as Tet+Vav (9+6) and Tet+Zayin (9+7).
#
#   4. FULL COMPONENT  (adaptation)
#      Month and day at full value; year summed to its digit total but
#      NOT pre-reduced.  Not a documented gematria method: it is a hybrid
#      of the absolute value (month, day) and the small value (year).
#      (Earlier versions called this "Mispar Gadol-inspired", but mispar
#      gadol differs from the standard values only for the five final
#      letter forms, 500-900, which never arise in a date.)
#
#   5. BONE'EH  (Building / Cumulative Value)
#      Treats the three date components as sequential "letters" and applies
#      the bone'eh formula: each step adds the running total plus the new
#      value.  For components m, d, y (each reduced to 1-9):
#        Bone'eh = 3m + 2d + y  (then reduced).
#      Source: Gematria Wikipedia -- "Mispar bone'eh is calculated by
#      walking over each letter, adding the value of all previous letters
#      and the current letter to the running total."
#
#   Methods 2-4 reduce their totals by Mispar katan mispari (repeatedly
#   summing digits) and stop at the first sacred number reached along the
#   way (see HEBREW_SACRED).
#
#   WHY THE SYNTHESIS USES BONE'EH
#   Summing digits never changes a number's remainder when divided by 9,
#   so methods 1-4 always arrive at the SAME final digit -- Gematria
#   Wikipedia says this of mispar katan mispari: "The same value will be
#   arrived at regardless of whether it is the absolute values, the
#   ordinal values, or the reduced values that are being counted."  They
#   differ only in which sacred number (if any) they pass through.
#   Bone'eh weights the components by position, so it is the one Hebrew
#   method whose digit is independent of method 1; the Greek ⊕ Hebrew
#   synthesis pairs those two.  (Pairing methods 1 and 2, as earlier
#   versions did, always produced method 1 doubled.)
#
# Letter values from Gematria Wikipedia (standard encoding); letter meanings
# from the Mathers Table (The Kabbalah Unveiled, 1887); significant numbers
# from MyJewishLearning; Kabbalah from Britannica.
# ─────────────────────────────────────────────────────────────────────────────


# =============================================================================
# UTILITY
# =============================================================================

import calendar as _calendar
import io
import os
import re as _re
import sys
import termios
import tty
from datetime import date


def digit_sum(n):
    return sum(int(d) for d in str(n))


def reduce_to_single_digit(n):
    """Mispar katan mispari: repeatedly sum digits until 1-9."""
    while n > 9:
        n = digit_sum(n)
    return n


def parse_date(date_str):
    """Accept MM-DD-YYYY or MM/DD/YYYY and reject dates that don't exist."""
    parts = _re.split(r'[-/]', date_str.strip())
    if len(parts) != 3:
        raise ValueError("Use MM-DD-YYYY or MM/DD/YYYY.")
    try:
        m, d, y = (int(p) for p in parts)
    except ValueError:
        raise ValueError("Month, day and year must be numbers.")
    if not (1 <= m <= 12):
        raise ValueError("Month must be 1-12.")
    if not (1 <= y <= 9999):
        raise ValueError("Year must be 1-9999.")
    days_in_month = _calendar.monthrange(y, m)[1]
    if not (1 <= d <= days_in_month):
        raise ValueError(f"{MONTH_NAMES[m]} {y} has {days_in_month} days.")
    return m, d, y


def parse_month_year(raw_str):
    """Accept MM-YYYY or MM/YYYY."""
    parts = _re.split(r'[-/]', raw_str.strip())
    if len(parts) != 2:
        raise ValueError("Use MM-YYYY or MM/YYYY.")
    try:
        m, y = int(parts[0]), int(parts[1])
    except ValueError:
        raise ValueError("Month and year must be numbers.")
    if not (1 <= m <= 12):
        raise ValueError("Month must be 1-12.")
    if not (1 <= y <= 9999):
        raise ValueError("Year must be 1-9999.")
    return m, y


# ---------------------------------------------------------------------------
# ANSI escape-code stripper  (keeps the year-mode .txt export clean)
# ---------------------------------------------------------------------------
_ANSI_RE = _re.compile(r'\033\[[0-9;]*m')


def _strip_ansi(text: str) -> str:
    return _ANSI_RE.sub('', text)


class _TeeWriter:
    """Write to both the terminal (with colour) and a buffer (plain text)."""
    def __init__(self, terminal, buffer):
        self._terminal = terminal
        self._buffer   = buffer

    def write(self, data):
        self._terminal.write(data)
        self._buffer.write(_strip_ansi(data))

    def flush(self):
        self._terminal.flush()
        self._buffer.flush()

    # Make it a valid file-like object
    def fileno(self):          return self._terminal.fileno()
    @property
    def encoding(self):        return getattr(self._terminal, 'encoding', 'utf-8')
    @property
    def errors(self):          return getattr(self._terminal, 'errors', 'replace')



# =============================================================================
# HEBREW NUMERALS
# Letter values: Gematria Wikipedia, "Standard encoding" table (names use that
# table's spelling).  Thousands: Mathers Table -- "an Aleph larger than the
# rest of the letters among which it is, signifies not 1, but 1000."
# =============================================================================

_HEBREW_UNITS = [None, ('א', 'Aleph'), ('ב', 'Bet'), ('ג', 'Gimel'),
                 ('ד', 'Dalet'), ('ה', 'He'), ('ו', 'Vav'), ('ז', 'Zayin'),
                 ('ח', 'Het'), ('ט', 'Tet')]
_HEBREW_TENS = [None, ('י', 'Yod'), ('כ', 'Kaf'), ('ל', 'Lamed'),
                ('מ', 'Mem'), ('נ', 'Nun'), ('ס', 'Samekh'), ('ע', 'Ayin'),
                ('פ', 'Pe'), ('צ', 'Tsadi')]
_HEBREW_HUNDREDS = [None, ('ק', 'Kof'), ('ר', 'Resh'), ('ש', 'Shin'),
                    ('ת', 'Tav')]


def hebrew_numeral(n):
    """
    Spell a positive integer in Hebrew numerals.
    Returns a list of (glyph, name, value) tuples in reading order.

    Hundreds above 400 are built from Tav (700 = Tav + Shin).  15 and 16
    are written Tet+Vav (9+6) and Tet+Zayin (9+7), the standard Hebrew
    convention for avoiding Yod+He and Yod+Vav, which spell part of the
    divine name.  (This convention is not in the five source documents.)
    """
    letters = []
    thousands, n = divmod(n, 1000)
    if thousands:
        letters += [(g, name, v * 1000) for g, name, v in hebrew_numeral(thousands)]
    hundreds, rest = divmod(n, 100)
    while hundreds >= 4:
        letters.append((*_HEBREW_HUNDREDS[4], 400))
        hundreds -= 4
    if hundreds:
        letters.append((*_HEBREW_HUNDREDS[hundreds], hundreds * 100))
    if rest in (15, 16):
        letters.append((*_HEBREW_UNITS[9], 9))
        letters.append((*_HEBREW_UNITS[rest - 9], rest - 9))
    else:
        tens, units = divmod(rest, 10)
        if tens:
            letters.append((*_HEBREW_TENS[tens], tens * 10))
        if units:
            letters.append((*_HEBREW_UNITS[units], units))
    return letters


def format_hebrew(letters):
    """Glyphs with geresh / gershayim:  2 -> ב׳,  28 -> כ״ח,  2026 -> ב׳כ״ו."""
    big = ''.join(g for g, _, v in letters if v >= 1000)
    small = [g for g, _, v in letters if v < 1000]
    out = big + '׳' if big else ''
    if len(small) == 1:
        out += small[0] + '׳'
    elif small:
        out += ''.join(small[:-1]) + '״' + small[-1]
    return out


def katan_value(value):
    """Mispar katan: a letter's value with its zeros truncated (400 -> 4)."""
    return int(str(value).rstrip('0'))


# =============================================================================
# THE FIVE METHODS
# =============================================================================

# Sacred numbers preserved by methods 2-4 when a reduction reaches them.
# 13, 18, 26, 36, 40, 49, 50, 70: see HEBREW_DATA.  32: the "32 paths of
# secret wisdom" of Sefer Yetzira (Kabbalah Britannica).
HEBREW_SACRED = {13, 18, 26, 32, 36, 40, 49, 50, 70}


def reduce_preserving_sacred(n):
    """
    Mispar katan mispari (repeated digit-summing), stopping at the first
    sacred number reached -- the raw total included.
    Returns (final, chain), where chain lists every value passed through.
    """
    chain = [n]
    while n > 9 and n not in HEBREW_SACRED:
        n = digit_sum(n)
        chain.append(n)
    return n, chain


def method_pythagorean(month, day, year):
    """
    Method 1 — Modern Pythagorean Numerology (digit-reduction method).
    Reduce each component individually, sum, reduce.
    Returns (r_month, r_day, r_year, raw_sum, final).
    """
    rm = reduce_to_single_digit(month)
    rd = reduce_to_single_digit(day)
    ry = reduce_to_single_digit(digit_sum(year))
    raw = rm + rd + ry
    return rm, rd, ry, raw, reduce_to_single_digit(raw)


def method_hechrachi(month, day, year):
    """
    Method 2 — Hebrew Standard (Mispar Hechrachi, absolute value).
    Sum the full standard values of every letter of the date written in
    Hebrew numerals (= month + day + year), then reduce, preserving sacred
    numbers.
    Returns (component_values, raw_sum, chain, final).
    """
    values = [sum(v for _, _, v in hebrew_numeral(x)) for x in (month, day, year)]
    raw = sum(values)
    final, chain = reduce_preserving_sacred(raw)
    return values, raw, chain, final


def method_katan(month, day, year):
    """
    Method 3 — Mispar Katan (small value).
    Sum the zero-truncated value of every letter of the date written in
    Hebrew numerals, then reduce, preserving sacred numbers.
    Returns (katan_values_per_component, raw_sum, chain, final).
    """
    parts = [[katan_value(v) for _, _, v in hebrew_numeral(x)]
             for x in (month, day, year)]
    raw = sum(sum(p) for p in parts)
    final, chain = reduce_preserving_sacred(raw)
    return parts, raw, chain, final


def method_full_component(month, day, year):
    """
    Method 4 — Full Component (adaptation; not a documented gematria method).
    Use month and day at full face value; sum year digits but do NOT
    pre-reduce that total.  Reduce, preserving sacred numbers.
    Returns (month_val, day_val, year_digit_sum, raw_sum, chain, final).
    """
    year_ds = digit_sum(year)
    raw = month + day + year_ds
    final, chain = reduce_preserving_sacred(raw)
    return month, day, year_ds, raw, chain, final


def method_boneeh(month, day, year):
    """
    Method 5 — Bone'eh (Building / Cumulative Value).
    Source (Gematria Wikipedia, "Other methods"):
      "adding the value of all previous letters and the value of the
       current letter to the running total.  Therefore, the value of the
       word achad (one) is 1 + (1+8) + (1+8+4) = 23."
    'All previous letters' means the sum of the ORIGINAL letter values
    seen so far, NOT the accumulated bone'eh running total.

    For three date 'letters' [m, d, y] (each reduced 1-9):
      Step 1: prev_orig=0;   running += (0 + m)       → running = m
      Step 2: prev_orig=m;   running += (m + d)        → running = 2m + d
      Step 3: prev_orig=m+d; running += (m + d + y)    → running = 3m + 2d + y

    Final value then reduced to single digit.
    Returns (m, d, y, (step1, step2, step3), final).
    """
    m = reduce_to_single_digit(month)
    d = reduce_to_single_digit(day)
    y = reduce_to_single_digit(digit_sum(year))

    # Track cumulative original-letter sum separately from running bone'eh total
    running = 0
    prev_orig = 0
    steps = []
    for letter in (m, d, y):
        running += prev_orig + letter
        prev_orig += letter
        steps.append(running)

    step1, step2, step3 = steps
    return m, d, y, (step1, step2, step3), reduce_to_single_digit(step3)


def compute_synthesis_number(month, day, year):
    """
    Greek ⊕ Hebrew synthesis: Method 1 (Greek Pythagorean) plus Method 5
    (Hebrew Bone'eh), reduced to 1-9.  See "WHY THE SYNTHESIS USES BONE'EH"
    in the header.  Prints nothing, so it can run across a whole year for
    graphing.
    """
    greek_num = method_pythagorean(month, day, year)[-1]
    boneeh_num = method_boneeh(month, day, year)[-1]
    return reduce_to_single_digit(greek_num + boneeh_num)


# =============================================================================
# GREEK DATA  (Pythagorean number symbolism)
# Sources: Numerology Wikipedia; Gematria Wikipedia; Britannica Pythagoreanism
# =============================================================================

GREEK_DATA = {
    1: {
        "name": "The Monad",
        "note": (
            "Greek: Monas -- unity and the source of all numbers. The Pythagoreans "
            "did not consider 1 a number because number implies plurality; 1 was the "
            "source from which all numbers arise by addition. It changed odd to even "
            "and even to odd, belonging to neither class. "
        ),
        "descriptor": (
            "The Monad -- unity and the origin of all things. The Pythagoreans did "
            "not consider 1 to be a number at all, because number implies plurality; "
            "instead, it was the singular source from which every other number is "
            "generated. This date vibrates with absolute first-cause energy: the "
            "singular, undivided originating impulse before multiplicity was born, "
            "the ground zero from which everything else proceeds."
        ),
    },
    2: {
        "name": "The Dyad — Female Principle",
        "note": (
            "Greek: Duas -- the female principle; the first even number. In Pythagorean "
            "tradition all even numbers were female and all odd numbers male. Two was "
            "the first even, the first expression of the feminine, introducing duality, "
            "opposition, and the possibility of difference. "
        ),
        "descriptor": (
            "The Dyad -- the female principle, the first even number, and the first "
            "departure from unity. The Pythagoreans held all even numbers to be female "
            "and all odd numbers male; Two embodied the feminine principle and introduced "
            "the possibility of polarity. This date carries the energy of receptivity, "
            "reflection, and the relational power that requires another to complete it."
        ),
    },
    3: {
        "name": "The Triad — Male Principle",
        "note": (
            "Greek: Trias -- the male principle; the first odd number beyond unity. "
            "Plato saw 3 as symbolic of the triangle, the simplest spatial shape. "
            "Three is also the dimension of the smallest magic square (rows, columns, "
            "and diagonals summing to 15). "
        ),
        "descriptor": (
            "The Triad -- the male principle, the first odd number generated from unity. "
            "Plato saw Three as the triangle -- the simplest shape possible in space, "
            "from which all visible form is constructed. This date moves with active, "
            "initiating energy: the assertion of form into the void, the first "
            "articulation of structure in the world."
        ),
    },
    4: {
        "name": "The Tetrad — Justice",
        "note": (
            "Greek: Tetras -- justice. Explicitly documented: 'The number 4 represented "
            "justice' in Pythagorean tradition. Four generates the most perfect number: "
            "1+2+3+4=10 (the Tetractys). It encodes the four elements, four seasons, "
            "and four cardinal directions. "
        ),
        "descriptor": (
            "The Tetrad -- justice and the order of the material world. The Pythagoreans "
            "explicitly held that Four represented justice: balanced, four-square, and "
            "impartially structured. It is the seed of the most perfect number because "
            "1+2+3+4=10. This date calls for honest reckoning and right measure -- and "
            "the patient building of structures that will hold because they are just."
        ),
    },
    5: {
        "name": "The Pentad — Marriage",
        "note": (
            "Greek: Pentas -- marriage; the sum of the female 2 and the male 3. "
            "Five symbolizes human life and -- in Platonic and Pythagorean traditions "
            "-- marriage, as the sum of the female 2 and the male 3. The pentagram "
            "(five-pointed star) was associated in antiquity with the Babylonian "
            "goddess Ishtar and her Roman parallel Venus (Britannica). A human "
            "placed in a circle with arms and legs outstretched approximates "
            "the five points of a pentagon; joining alternate points produces a pentagram. "
        ),
        "descriptor": (
            "The Pentad -- marriage and human life, the sacred union of the female "
            "Two and the male Three. Five symbolizes marriage because it is the sum "
            "of the first female number (2) and the first male number (3): even and "
            "odd joined in one. It also represents the five fingers and the five "
            "extremities of the human body. This date pulses with the vitality of "
            "the fully human -- embodied, relational, alive precisely at the "
            "intersection of opposites."
        ),
    },
    6: {
        "name": "The Hexad — Perfection",
        "note": (
            "Greek: Hexas -- the first perfect number. Six is both the sum (1+2+3) "
            "and the product (1x2x3) of the first three numbers -- a remarkable "
            "mathematical coincidence explicitly documented as marking it 'perfect.' "
            "Mathematically, a perfect number equals the sum of its proper divisors "
            "(1+2+3=6). "
        ),
        "descriptor": (
            "The Hexad -- the first perfect number, displaying a remarkable "
            "mathematical coincidence: Six is both the sum (1+2+3) and the product "
            "(1x2x3) of the first three numbers. The six days of Creation in Genesis "
            "mirror this structure. This date carries the quiet completeness of "
            "things that are exactly as they should be."
        ),
    },
    7: {
        "name": "The Heptad",
        "note": (
            "Greek: Heptas -- a number of great mystical significance. The Britannica "
            "source notes that 7 is 'the sum of the spiritual 3 and the material 4.' "
            "Many ancient cultures recognized seven visible planets (Sun, Moon, Mercury, "
            "Venus, Mars, Jupiter, Saturn); note that the Pythagoreans themselves "
            "recognized nine heavenly bodies (adding Earth and the Central Fire), "
            "not seven. Seven names the days of the week, and there are seven distinct "
            "notes in the musical scale. "
        ),
        "descriptor": (
            "The Heptad -- seven as the union of the spiritual Three and the material "
            "Four: the number that bridges the higher and lower orders of existence. "
            "Seven gives the days of the week their structure, and there are seven "
            "distinct notes in the musical scale, a pattern the Pythagoreans found "
            "deeply significant given their discovery that musical harmony obeys "
            "whole-number ratios. Seven visible planets named the days of the week "
            "across many ancient cultures. This date opens a space of stillness and "
            "high perception -- the kind of knowing that comes not from activity "
            "but from patient observation of what is already circling."
        ),
    },
    8: {
        "name": "The Ogdoad — Auspicious Fullness",
        "note": (
            "Greek: Ogdoas -- the Britannica source states 8 is 'generally considered "
            "to be an auspicious number.' In Babylonian myth (per Britannica) there "
            "were seven spheres plus an eighth realm -- the fixed stars -- where the "
            "gods lived; as a result, 8 is associated with paradise and divine "
            "fullness beyond the seven planetary spheres. The Greek name of Jesus "
            "(Iesous) sums to 888 in isopsephy. "
        ),
        "descriptor": (
            "The Ogdoad -- generally considered auspicious, and the number of divine "
            "fullness above the seven planetary spheres. In Babylonian cosmology there "
            "were seven spheres of planets, and above them an eighth realm -- the "
            "fixed stars -- where the gods themselves resided. Eight is therefore the "
            "number of what lies beyond ordinary cycles. The Greek name of Jesus "
            "(Iesous) sums to 888 in isopsephy, three repetitions of 8. This date "
            "carries an energy of passage into a realm above the sevenfold structure."
        ),
    },
    9: {
        "name": "The Ennead — Boundary of the Decade",
        "note": (
            "Greek: Enneas -- the boundary number before the perfect Ten. The Britannica "
            "source notes that 9 'often represents pain or sadness' in ancient traditions, "
            "and that in Islamic cosmology the universe comprises nine spheres. In "
            "Welsh law, nine steps was a unit of legal distance. In "
            "Greek mythology the River Styx has nine twists. The 'boundary before Ten' "
            "framing comes from 10 being the Pythagorean most-perfect number (Tetractys). "
        ),
        "descriptor": (
            "The Ennead -- the last single digit, standing at the boundary before Ten, "
            "the Pythagorean most perfect number. Ancient traditions widely associated "
            "nine with a threshold quality: the Styx had nine twists separating the "
            "living from the dead; Welsh law measured distances in units of nine steps; "
            "Islamic cosmology arranged the universe across nine spheres. Nine carries "
            "the weight of everything that must be traversed before the great completion "
            "of Ten. This date stands at that threshold -- gathering what the journey "
            "has accumulated, just before the cycle reaches its fullness."
        ),
    },
}


# =============================================================================
# HEBREW DATA  (Standard Gematria / Kabbalistic tradition)
#
# Letter values: standard gematria table (mispar hechrachi)
#   Source: Gematria Wikipedia -- Standard encoding section
# Letter meanings: Mathers Table (The Kabbalah Unveiled, 1887)
#   Aleph=Ox, Bet=House, Gimel=Camel, Dalet=Door, He=Window, Vav=Peg/Nail,
#   Zayin=Weapon/Sword, Het=Enclosure/Fence, Tet=Serpent, Yod=Hand
# Sacred numbers (preserved before reduction):
#   13: Echad (aleph[1]+het[8]+dalet[4])  -- divine unity, 13 attributes of mercy
#   18: Chai  (het[8]+yod[10])            -- life
#   26: YHVH  (yod[10]+he[5]+vav[6]+he[5])
#   32: 10 sefirot + 22 letters           -- the 32 paths of secret wisdom
#   36: Lamed-Vav (30+6) / 2×Chai        -- hidden righteous ones
#   40: Forty                             -- radical transformation (flood; Sinai)
#   49: Seven×Seven                       -- the Omer count before Shavuot
#   50: Jubilee year (yovel)              -- liberation and return
#   70: Seventy nations / Sanhedrin       -- fullness of the world
# =============================================================================

HEBREW_DATA = {
    1: {
        "name": "Aleph — Ox",
        "note": (
            "Gematria value: 1. Literal meaning: Ox (Mathers Table). Judaism's "
            "foundational declaration, the Shema, centers on the Oneness of God: "
            "'the Lord is one.' One is the number of divine unity. "
        ),
        "descriptor": (
            "Aleph -- whose literal form means Ox. Its gematria value of 1 speaks "
            "directly to the core of Jewish theology: the Oneness of God declared "
            "in the Shema -- 'Hear O Israel, the Lord is our God, the Lord is one.' "
            "This date breathes with that primordial singular unity: the undivided "
            "source before any word."
        ),
    },
    2: {
        "name": "Bet — House",
        "note": (
            "Gematria value: 2. Literal meaning: House (Mathers Table). "
            "Pairs recur throughout Jewish practice: two Shabbat candles, two "
            "challahs on the table, the two tablets of the Ten Commandments, "
            "Noah's animals two by two. Source: MyJewishLearning. "
        ),
        "descriptor": (
            "Bet -- the house. Pairs permeate Jewish life: two candles are lit at "
            "the start of Shabbat, two challahs sit on the table, two tablets held "
            "the Ten Commandments, and Noah's animals entered the ark two by two. "
            "This date resonates with covenantal relationship and the sacred home "
            "built only in partnership."
        ),
    },
    3: {
        "name": "Gimel — Camel",
        "note": (
            "Gematria value: 3. Literal meaning: Camel (Mathers Table). Three "
            "patriarchs: Abraham, Isaac, Jacob. Three pilgrimage festivals: Passover, "
            "Shavuot, Sukkot. Three groups: Priests (Kohanim), Levites, Israelites. "
            "The Amidah addresses God as the God of the three patriarchs. "
        ),
        "descriptor": (
            "Gimel -- the camel, the animal that travels great distances carrying "
            "what others need. Judaism was born in three generations: the three "
            "patriarchs Abraham, Isaac, and Jacob. Three pilgrimage festivals "
            "structure the Jewish year, each a journey to remember who you are. "
            "This date moves with purposeful carrying -- the generosity that keeps "
            "traveling forward, bearing gifts, refusing to stop short."
        ),
    },
    4: {
        "name": "Dalet — Door",
        "note": (
            "Gematria value: 4. Literal meaning: Door (Mathers Table). Four "
            "matriarchs: Sarah, Rebecca, Rachel, Leah. Four cups at Passover; Four "
            "Questions; Four Sons. Four rivers from Eden; four winds; four corners "
            "of heaven and earth. Four corners of tzitzit garments. "
        ),
        "descriptor": (
            "Dalet -- the door, the threshold that marks an entrance. Four structures "
            "Jewish life at its foundations: the four matriarchs Sarah, Rebecca, Rachel, "
            "and Leah; and the four cups that frame the Passover seder, along with the "
            "Four Questions and Four Sons. Four also describes the shape of the world: "
            "four rivers flowed from Eden, four winds blow from four directions. "
            "This date stands at a threshold that opens in every direction at once."
        ),
    },
    5: {
        "name": "He — Window",
        "note": (
            "Gematria value: 5. Literal meaning: Window (Mathers Table). He appears "
            "twice in the Tetragrammaton (YHVH: Yod-He-Vav-He). The Torah is in five "
            "books (Chumash, from the Hebrew for five). The hamsa relates to the Hebrew "
            "for five. Each tzitzit fringe is tied with five double knots; in "
            "Sephardic tradition the windings between them (10, 5, 6, 5) correspond "
            "to the letters of the Tetragrammaton. Source: MyJewishLearning. "
        ),
        "descriptor": (
            "He -- the window: the opening through which light and breath pass between "
            "inner and outer worlds. He appears twice in the Tetragrammaton (YHVH), "
            "the most sacred Name, framing Yod and Vav on both sides. The Torah "
            "unfolds in five books. The hamsa, shaped like a five-fingered hand, "
            "guards those who carry it. This date opens a window: what was hidden "
            "may now be seen."
        ),
    },
    6: {
        "name": "Vav — Peg, Nail",
        "note": (
            "Gematria value: 6. Literal meaning: Peg, nail (Mathers Table). "
            "Six days of creation precede Shabbat rest (MyJewishLearning). "
            "Tikkun ('cosmic restoration') is a central Lurianic Kabbalistic "
            "doctrine, achieved through intense mystical life and unceasing "
            "struggle against evil; it follows tzimtzum (the withdrawal of "
            "divine light) and qellipot (the sinking of luminous particles "
            "into matter, or 'shells'). Source: Kabbalah Britannica. "
        ),
        "descriptor": (
            "Vav -- the peg and nail, the fastener that holds things together. "
            "Six days of creation preceded Shabbat; Vav is the energy of active "
            "connection and building. In Lurianic Kabbalah, the great work of tikkun "
            "(cosmic restoration) is carried out not through ease but through "
            "unceasing struggle against evil and an intensely lived mystical life. "
            "This date calls for the work of fastening: sustained effort that "
            "holds things in place."
        ),
    },
    7: {
        "name": "Zayin — Weapon, Sword",
        "note": (
            "Gematria value: 7. Literal meaning: Weapon, sword (Mathers Table). Seven "
            "is among the most significant numbers in Judaism. 'All the sevenths are "
            "always beloved' (Leviticus Rabbah 29:11). Shabbat is the seventh day. "
            "Sheva Brachot (seven blessings) at weddings. Shmita every seventh year. "
            "Seven Noahide laws; seven-branched menorah. "
        ),
        "descriptor": (
            "Zayin -- whose literal form is weapon or sword, yet which carries in "
            "Jewish tradition the highest crown of sacred completion. An ancient midrash "
            "from Leviticus Rabbah declares: 'All the sevenths are always beloved' -- "
            "the seventh day, the seventh year (shmita), the seven blessings at every "
            "wedding, the seven-branched menorah in the Temple. This date is crowned "
            "with the gift that cannot be forced: stop striving, receive what is complete."
        ),
    },
    8: {
        "name": "Het — Enclosure, Fence",
        "note": (
            "Gematria value: 8. Literal meaning: Enclosure, fence (Mathers Table). "
            "Jewish boys are circumcised on the eighth day of life. "
            "Source: MyJewishLearning. "
        ),
        "descriptor": (
            "Het -- the enclosure and fence, a boundary that marks the edge of ordinary "
            "space. Yet in Jewish tradition, eight is the number that crosses into "
            "covenant: circumcision on the eighth day of life marks the child's entry "
            "into the covenant of Abraham. Eight comes after the complete seven-day "
            "cycle, belonging to the order beyond the natural. This date opens a gate "
            "at the edge of the ordinary."
        ),
    },
    9: {
        "name": "Tet — Serpent",
        "note": (
            "Gematria value: 9. Literal meaning: Serpent (Mathers Table). The "
            "Hanukkah menorah has nine branches, modeled on the seven-branched "
            "Temple menorah (MyJewishLearning). Gematria Wikipedia's worked "
            "example of mispar katan mispari reduces emet (truth: aleph 1 + mem "
            "40 + tav 400 = 441) to 4+4+1 = 9, and 3 Baruch's snake that drinks "
            "from 360 rivers takes its number from the Greek drakon written in "
            "Hebrew (דרקון = 360, which reduces to 9). "
        ),
        "descriptor": (
            "Tet -- the serpent, gematria value 9, the last of the single-digit "
            "letters. Gematria's own worked example lands here: emet, truth "
            "(aleph + mem + tav = 441), reduces to 9 -- and so does emet repeated "
            "twice or three times. The Hanukkah menorah carries nine branches. "
            "This date asks what remains true once everything else has been "
            "reduced away."
        ),
    },
    13: {
        "name": "Thirteen — Echad (Divine Unity & Mercy)",
        "note": (
            "Gematria: 13 = Echad (One): aleph[1]+het[8]+dalet[4]=13 -- stated "
            "directly in Gematria Wikipedia ('\"achad\" (one) is 1+8+4 = 13'), "
            "which also gives its bone'eh value as 23. The 13 attributes of "
            "divine mercy are recited during Selichot and High Holiday prayers "
            "(MyJewishLearning). Age of Bar Mitzvah. Maimonides' 13 principles of "
            "faith, codified in the Yigdal prayer. The 13 lunar months of the "
            "year led the Hebrews to consider 13 auspicious (Britannica). "
        ),
        "descriptor": (
            "Thirteen -- the gematric value of Echad (One): Aleph (1) + Het (8) + "
            "Dalet (4) = 13. God is declared One in the Shema, and thirteen is the "
            "number through which that Oneness expresses its mercy: the 13 attributes "
            "of divine compassion recited on the High Holidays are the face God turns "
            "toward those who have strayed. Thirteen is also the age of Bar Mitzvah -- "
            "when a boy becomes responsible for all 613 mitzvot. This date vibrates "
            "with the mercy of the One who counts every soul as infinitely precious."
        ),
    },
    18: {
        "name": "Eighteen — Chai (Life)",
        "note": (
            "Gematria: 18 = Chai (life): het[8]+yod[10]=18. Explicitly documented: "
            "'Perhaps the most famous example [of gematria] is that the numerical "
            "value of the word chai, which means life, is 18. Eighteen is therefore "
            "considered a lucky Jewish number.' The Amidah is called Shemonah Esreh "
            "(The Eighteen) for its original 18 blessings. "
        ),
        "descriptor": (
            "Eighteen -- Chai: Het (8) + Yod (10) = 18, the Hebrew word for life "
            "itself. This is perhaps the most famous example of gematria in living "
            "Jewish practice: gifts are given in multiples of 18 ($18, $180) as an "
            "act of blessing. The central prayer, the Amidah, is still called the "
            "Shemonah Esreh (The Eighteen) after its original 18 blessings, though "
            "it has 19 today. This date is saturated with life-force -- the sacred, "
            "irreducible gift of being alive and present in this moment."
        ),
    },
    26: {
        "name": "Twenty-Six — The Divine Name (YHVH)",
        "note": (
            "Gematria: 26 = YHVH: yod[10]+he[5]+vav[6]+he[5]=26. From the standard "
            "gematria table (mispar hechrachi). The Tetragrammaton is the personal "
            "name of God in Hebrew Scripture. Source: Gematria Wikipedia. "
        ),
        "descriptor": (
            "Twenty-six -- the sum of the four letters of the divine Name: Yod (10) "
            "+ He (5) + Vav (6) + He (5) = 26. The Tetragrammaton (YHVH) is the "
            "personal name of God in Hebrew Scripture -- the four-letter Name whose "
            "numerical signature is 26. In Sephardic tradition the tzitzit fringes "
            "are wound 10, 5, 6 and 5 times between their five knots -- the letters "
            "of this Name, totalling 26. A date carrying 26 holds the quiet weight "
            "of divine presence: not dramatic, simply here."
        ),
    },
    32: {
        "name": "Thirty-Two — The Paths of Secret Wisdom",
        "note": (
            "Sefer Yetzira ('Book of Creation', 3rd-6th century), the earliest "
            "known Jewish text on magic and cosmology, explained creation through "
            "the 10 divine numbers (sefirot) and the 22 letters of the Hebrew "
            "alphabet; 'taken together, they were said to constitute the 32 paths "
            "of secret wisdom.' Source: Kabbalah Britannica. Ten sefirot: "
            "MyJewishLearning. Written in Hebrew numerals, 32 is Lamed (30) + "
            "Bet (2). "
        ),
        "descriptor": (
            "Thirty-two -- the 32 paths of secret wisdom: the ten sefirot, the "
            "divine numbers or emanations through which God creates, joined with "
            "the 22 letters of the Hebrew alphabet. Sefer Yetzira taught that the "
            "world was made from exactly these: number and letter together, the "
            "same marriage that gematria itself depends on. A date carrying 32 "
            "sits where counting and naming meet -- a day for understanding how "
            "things are put together, not only what they are."
        ),
    },
    36: {
        "name": "Thirty-Six — The Lamed-Vav (Hidden Righteous)",
        "note": (
            "Gematria: 36 = Lamed (30) + Vav (6) = 36. Explicitly documented: "
            "'These 36 are called the lamed vavniks (from the Hebrew letters lamed "
            "and vav whose value adds up to 36).' A Hasidic teaching holds that 36 "
            "hidden righteous ones sustain the world in every generation. Also 2×Chai "
            "(2x18=36). "
        ),
        "descriptor": (
            "Thirty-six -- Lamed (30) + Vav (6) = 36: the number of the hidden "
            "righteous ones, the lamed vavniks. A Hasidic teaching holds that in "
            "every generation there are exactly 36 tzadikim nistarim -- hidden "
            "righteous people whose identities are unknown, yet on account of whose "
            "goodness the world is not destroyed. Thirty-six is also twice Chai "
            "(2x18). This date draws near the consciousness of anonymous goodness: "
            "the kind that asks nothing and sustains everything."
        ),
    },
    40: {
        "name": "Forty — The Great Transformation",
        "note": (
            "Forty appears frequently in the Hebrew Bible as a significant span "
            "of time during which radical transformation is wrought. God caused rain "
            "for 40 days and nights (Noah). Moses spent 40 days on Mount Sinai to "
            "receive the Torah. The Israelites wandered 40 years in the wilderness "
            "until the generation of Egypt had passed away. Source: MyJewishLearning. "
        ),
        "descriptor": (
            "Forty -- the number of radical and irreversible transformation in "
            "Hebrew Scripture. God sent forty days of rain before the world was "
            "renewed through Noah. Moses spent forty days on Sinai, absent from "
            "the human world, to receive the Torah whole. The Israelites spent "
            "forty years in the wilderness -- not as punishment alone, but as the "
            "time required for a generation shaped by slavery to give way to a "
            "generation born in freedom. A date bearing forty asks: what must "
            "be dissolved completely before the new world can be entered?"
        ),
    },
    49: {
        "name": "Forty-Nine — Seven Times Seven (The Omer)",
        "note": (
            "Forty-nine is seven times seven, the counting of the Omer: the 49 days "
            "between Passover and Shavuot. 'Between Passover and Shavuot, Jews count "
            "seven times seven weeks, or 49 days.' The fiftieth day is Shavuot, "
            "the revelation of Torah at Sinai. Also: after seven cycles of shmita, "
            "the fiftieth year is the yovel (Jubilee). Source: MyJewishLearning. "
        ),
        "descriptor": (
            "Forty-nine -- seven times seven, the full count of the Omer: the 49 "
            "days of active preparation that stretch between Passover (liberation "
            "from Egypt) and Shavuot (revelation of Torah at Sinai). To count "
            "forty-nine is to move through every day of that period of preparation "
            "-- to have traveled the full distance between liberation and revelation. "
            "This date stands at the completion of that great journey, with the "
            "fiftieth day already waiting at the threshold."
        ),
    },
    50: {
        "name": "Fifty — The Jubilee (Yovel)",
        "note": (
            "Fifty is the Jubilee year (yovel): the 50th year after seven cycles of "
            "shmita. 'During this year, not only was the land permitted to rest, but "
            "slaves were freed, debts were forgiven and land was returned to its "
            "original owners. The practice was meant as a societal reset.' It is "
            "also the fiftieth day after Passover: Shavuot (the giving of the Torah). "
            "Source: MyJewishLearning. "
        ),
        "descriptor": (
            "Fifty -- the Jubilee: the year that arrives after seven sevens, when "
            "the entire social order is reset. Slaves go free, debts are forgiven, "
            "land returns to its original families. Fifty does not merely conclude "
            "the forty-nine; it exceeds the count entirely, arriving at a new kind "
            "of time that the counting itself could not contain. And fifty is also "
            "Shavuot -- the day revelation descended from Sinai, the gift that no "
            "preparation fully earns but only readiness can receive. This date "
            "carries the quality of liberation that reorders everything."
        ),
    },
    70: {
        "name": "Seventy — The Fullness of the World",
        "note": (
            "According to Jewish tradition, there are 70 nations and 70 languages "
            "in the world, so 70 represents the totality of humanity. The Sanhedrin, "
            "the highest ancient Jewish court, was composed of 70 sages. Seventy is "
            "also considered the full span of a human life, and was the number of "
            "years granted to King David. Source: MyJewishLearning. "
        ),
        "descriptor": (
            "Seventy -- the fullness of the world. Jewish tradition holds that there "
            "are exactly 70 nations and 70 languages in the world: seventy is the "
            "complete accounting of human diversity, the number at which nothing is "
            "left out. The Sanhedrin, the supreme Jewish court of 70 sages, embodied "
            "this universality in its judgments. And seventy is the full span of a "
            "human life -- the years granted to King David. A date carrying seventy "
            "touches the whole of things: not one fragment, not one perspective, "
            "but the complete circle of human experience held at once."
        ),
    },
}


# =============================================================================
# COMBINED DATA  (Synthesis: Greek + Hebrew reduced values read together)
# =============================================================================

COMBINED_DATA = {
    1: {
        "name": "The Sovereign Origin",
        "descriptor": (
            "Where the Pythagorean Monad -- unity, the source from which all numbers "
            "are generated -- meets the Aleph of Hebrew tradition -- the Oneness of "
            "God before all speech -- a date of absolute originating power emerges. "
            "Both traditions agree: One is not a quantity but a quality, the ground "
            "from which all else proceeds. This is a day to act from first principles, "
            "to begin what has never existed before, to trust that singular clarity "
            "of purpose is the most powerful force in the world."
        ),
    },
    2: {
        "name": "The Sacred Pairing",
        "descriptor": (
            "The Pythagorean female principle meets the Bet of the house, and a day "
            "of sacred duality and dwelling emerges. Greek tradition gave Two the "
            "feminine -- receptive, relational, the first to depart from unity into "
            "otherness. Hebrew tradition built a house with Two as its first letter, "
            "because creation itself is a dwelling between God and humanity. The "
            "gift of this date belongs entirely to those willing to share it."
        ),
    },
    3: {
        "name": "The Active Completion",
        "descriptor": (
            "The Pythagorean male principle -- active, generative, the first odd force "
            "beyond unity -- meets Gimel's tireless camel-generosity, and a day of "
            "purposeful forward movement takes shape. Three in Greek tradition was the "
            "masculine impulse that gives form to the void; three in Hebrew tradition "
            "is the three patriarchs and three festivals that define a people's journey. "
            "This date asks for purposeful action: carry what you have been given, "
            "travel the full distance, and deliver it without stopping short."
        ),
    },
    4: {
        "name": "The Just Foundation",
        "descriptor": (
            "The Pythagorean number of justice meets Dalet, the humble door -- and a "
            "day of serious, right-ordered building presents itself. The Greeks "
            "explicitly named Four the number of justice: balanced, four-square, "
            "impartially structured. Hebrew tradition humbled Four into a threshold "
            "requiring surrender. Both traditions call for the same thing: build "
            "with integrity, hold the line of what is right, do so without pride "
            "or demand for recognition. This is a day for irreversible work."
        ),
    },
    5: {
        "name": "The Living Marriage",
        "descriptor": (
            "The Pythagorean number of marriage -- the sacred union of the female Two "
            "and male Three -- meets He, the window of the divine Name breathed outward. "
            "In both traditions Five is alive at the intersection of opposites: the "
            "Pythagoreans saw it as human life itself, the sum and embodiment of the "
            "female 2 and male 3; the Hebrews encoded it in the divine Name and the "
            "five books of the Torah. This date is alive precisely at that crossing "
            "point -- fully human, fully open."
        ),
    },
    6: {
        "name": "The Perfect Repair",
        "descriptor": (
            "The first perfect number meets Vav, the connecting peg -- and a day of "
            "extraordinary completion takes shape. Six was perfect to the "
            "Greeks mathematically: sum and product and divisor-sum all coincide. In "
            "Hebrew tradition six days of creation precede Shabbat, and in Lurianic "
            "Kabbalah the work of tikkun (cosmic restoration) is the great ongoing act, "
            "carried out through unceasing struggle against evil and an intensely "
            "lived mystical life. This date calls for sustained, active effort -- "
            "the patient work of building toward what perfection was always intended "
            "to look like."
        ),
    },
    7: {
        "name": "The Beloved Crown",
        "descriptor": (
            "The Pythagorean seven of heavenly order meets the Hebrew seven that "
            "the midrash declares 'always beloved' -- and the most universally sacred "
            "of all numbers asserts itself across both traditions. Many ancient cultures "
            "recognized seven visible planets that named the days of the week; Israel "
            "rested on the seventh day and recited seven blessings at every wedding. "
            "A date vibrating at Seven carries a single clear instruction: stop, "
            "receive. The gift that belongs to this day does not come to those who "
            "pursue it -- only to those still enough to notice it."
        ),
    },
    8: {
        "name": "The Transcendent Eight",
        "descriptor": (
            "The auspicious Ogdoad -- the number of divine fullness above the seven "
            "planetary spheres, rooted in Babylonian cosmology's eighth realm of the "
            "fixed stars where the gods resided -- meets Het, the enclosure that "
            "becomes a gate beyond the natural order. Both traditions consecrate "
            "Eight as the number that exceeds the sevenfold cycle: ancient cosmology "
            "placed divine fullness at the eighth level; Jewish tradition marks the "
            "eighth day of life with the covenant of circumcision. This date opens "
            "the gate at the edge of what is ordinary."
        ),
    },
    9: {
        "name": "The Great Threshold",
        "descriptor": (
            "The Ennead -- standing at the boundary before Ten, the most perfect "
            "Pythagorean number -- meets Tet, the serpent. Nine marks the last step "
            "before the great completion: ancient traditions across cultures placed "
            "threshold imagery at nine "
            "(the nine-twist Styx, the nine steps of Welsh law, the nine spheres "
            "of Islamic cosmology). This date stands at that threshold -- everything "
            "has been accumulated, the full count nearly complete, the next cycle "
            "waiting just beyond the edge of the visible."
        ),
    },
}


# =============================================================================
# DISPLAY HELPERS
# =============================================================================

def wrap(text, width=72, indent="  "):
    words = text.split()
    lines = []
    cur = indent
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur.rstrip())
            cur = indent + w + " "
        else:
            cur += w + " "
    if cur.strip():
        lines.append(cur.rstrip())
    return "\n".join(lines)


def bold(t):   return f"\033[1m{t}\033[0m"
def dim(t):    return f"\033[90m{t}\033[0m"
def cyan(t):   return f"\033[36m{t}\033[0m"
def amber(t):  return f"\033[33m{t}\033[0m"
def green(t):  return f"\033[32m{t}\033[0m"
def blue(t):   return f"\033[34m{t}\033[0m"
def magenta(t):return f"\033[35m{t}\033[0m"


def header(title, width=72):
    print(); print("=" * width)
    print(f"  {title}"); print("=" * width)


def subheader(title, color_fn=None, width=72):
    line = "-" * width
    label = f"  {title}"
    print(); print(color_fn(line) if color_fn else line)
    print(color_fn(label) if color_fn else label)
    print(color_fn(line) if color_fn else line)


def lookup_hebrew(n):
    if n in HEBREW_DATA:
        return HEBREW_DATA[n]
    r = reduce_to_single_digit(n)
    return HEBREW_DATA.get(r, HEBREW_DATA[9])


MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


# =============================================================================
# CALCULATE & PRINT A SINGLE DAY
# =============================================================================

def chain_text(chain):
    """[2056, 13] -> '2056→13'."""
    return "→".join(str(n) for n in chain)


def preserved_note(final):
    return " (sacred number preserved)" if final > 9 else ""


def calculate_day(month, day, year):
    """Run all five numerology methods for a single date and print results."""

    # ── Run all five methods ──────────────────────────────────────────────────

    # Method 1: Greek Pythagorean
    rm1, rd1, ry1, raw1, greek_num = method_pythagorean(month, day, year)

    # Method 2: Hebrew Standard (Mispar Hechrachi)
    abs_vals, raw2, chain2, hebrew_std_num = method_hechrachi(month, day, year)

    # Method 3: Mispar Katan
    katan_parts, raw3, chain3, katan_num = method_katan(month, day, year)

    # Method 4: Full Component
    m4, d4, yd4, raw4, chain4, full_num = method_full_component(month, day, year)

    # Method 5: Bone'eh (Building Value)
    bm, bd, by_, (s1, s2, s3), boneeh_num = method_boneeh(month, day, year)

    # Synthesis: Greek Pythagorean ⊕ Hebrew Bone'eh
    combined_num = compute_synthesis_number(month, day, year)

    numerals = [hebrew_numeral(x) for x in (month, day, year)]

    # ── Master header ─────────────────────────────────────────────────────────

    header(f"DATE  ·  {MONTH_NAMES[month]} {day}, {year}")

    # ── The date in Hebrew numerals (used by Methods 2 and 3) ────────────────

    print()
    print(dim("  In Hebrew numerals (letters as numbers):"))
    for label, value, letters in zip(("Month", "Day", "Year"),
                                     (month, day, year), numerals):
        spelled = " + ".join(f"{name} {v}" for _, name, v in letters)
        print(dim(f"    {label:<6}{value:>5}  =  {spelled:<34}") + f"  {format_hebrew(letters)}")

    # ── Summary table ─────────────────────────────────────────────────────────

    W = 72
    print()
    print("  " + "─" * (W - 4))
    print(f"  {'METHOD':<30}  {'CALCULATION':<24}  {'RESULT':>6}")
    print("  " + "─" * (W - 4))

    def row(label, calc, result, color_fn):
        star = " ★" if result > 9 else ""
        # Pad before colouring: ANSI codes would otherwise count toward width
        print(f"  {color_fn(f'{label:<30}')}  {dim(f'{calc:<24}')}  "
              f"{bold(color_fn(f'{result:>6}'))}{star}")

    katan_sums = [sum(p) for p in katan_parts]
    row("1. Greek Pythagorean",
        f"{rm1}+{rd1}+{ry1}={chain_text([raw1] + ([greek_num] if raw1 > 9 else []))}",
        greek_num, cyan)
    row("2. Hebrew Standard (Hechrachi)",
        f"{'+'.join(map(str, abs_vals))}={chain_text(chain2)}", hebrew_std_num, amber)
    row("3. Mispar Katan (Small Value)",
        f"{'+'.join(map(str, katan_sums))}={chain_text(chain3)}", katan_num, green)
    row("4. Full Component",
        f"{m4}+{d4}+{yd4}={chain_text(chain4)}", full_num, blue)
    row("5. Bone'eh (Building Value)",
        f"3×{bm}+2×{bd}+{by_}={chain_text([s3] + ([boneeh_num] if s3 > 9 else []))}",
        boneeh_num, magenta)
    print("  " + "─" * (W - 4))
    synth_raw = greek_num + boneeh_num
    row("SYNTHESIS (Greek ⊕ Bone'eh)",
        f"{greek_num}+{boneeh_num}={chain_text([synth_raw] + ([combined_num] if synth_raw > 9 else []))}",
        combined_num, magenta)
    print("  " + "─" * (W - 4))
    print()
    if any(x > 9 for x in (hebrew_std_num, katan_num, full_num)):
        print(dim("  ★ = sacred number preserved before final reduction"))
    print(dim(f"  Methods 1-4 always share a final digit ({greek_num}); they differ only in"))
    print(dim("  the sacred numbers their totals pass through on the way down."))
    print()

    # ── Method 1: Greek Pythagorean ───────────────────────────────────────────

    g = GREEK_DATA[greek_num]
    subheader(
        f"METHOD 1 · GREEK PYTHAGOREAN NUMEROLOGY  —  {greek_num}  ·  {g['name']}",
        cyan
    )
    print()
    print(wrap(g["descriptor"]))
    print()
    print(dim(wrap(f"Source note: {g['note']}")))

    # ── Method 2: Hebrew Standard ─────────────────────────────────────────────

    h2 = lookup_hebrew(hebrew_std_num)
    subheader(
        f"METHOD 2 · HEBREW STANDARD (MISPAR HECHRACHI)  —  {hebrew_std_num}  ·  "
        f"{h2['name']}{preserved_note(hebrew_std_num)}",
        amber
    )
    print()
    print(dim(f"  Absolute value: {' + '.join(map(str, abs_vals))} = {chain_text(chain2)}"
              f"{'  (sacred, preserved)' if hebrew_std_num > 9 else ''}"))
    print()
    print(wrap(
        "In mispar hechrachi every letter keeps its full standard value "
        "(1-9, 10-90, 100-400). A number written in Hebrew numerals therefore "
        "has itself as its absolute value, so the date's total is simply "
        "month + day + year. The total is reduced by mispar katan mispari -- "
        "repeatedly summing its digits -- stopping at the first sacred number "
        "the reduction reaches."
    ))
    print()
    print(wrap(h2["descriptor"]))
    print()
    print(dim(wrap(f"Source note: {h2['note']}")))

    # ── Method 3: Mispar Katan ────────────────────────────────────────────────

    h3 = lookup_hebrew(katan_num)
    subheader(
        f"METHOD 3 · MISPAR KATAN (SMALL VALUE)  —  {katan_num}  ·  "
        f"{h3['name']}{preserved_note(katan_num)}",
        green
    )
    print()
    groups = "  |  ".join(" + ".join(map(str, p)) for p in katan_parts)
    print(dim(f"  Letter values, zeros truncated:  {groups}  =  {chain_text(chain3)}"
              f"{'  (sacred, preserved)' if katan_num > 9 else ''}"))
    print()
    print(wrap(
        "Mispar katan ('small value') counts each letter with all of its zeros "
        "truncated: Kaf (20) counts 2, Tav (400) counts 4, and a thousands "
        "letter such as Bet-as-2000 counts 2. For a date this is the sum of "
        "its digits -- except that Hebrew writes 15 and 16 as Tet + Vav (9+6) "
        "and Tet + Zayin (9+7), so those contribute 15 and 16 rather than 6 "
        "and 7. The total is then reduced the same way as Method 2."
    ))
    print()
    print(wrap(h3["descriptor"]))
    print()
    print(dim(wrap(f"Source note: {h3['note']}")))

    # ── Method 4: Full Component ──────────────────────────────────────────────

    h4 = lookup_hebrew(full_num)
    subheader(
        f"METHOD 4 · FULL COMPONENT  —  {full_num}  ·  {h4['name']}{preserved_note(full_num)}",
        blue
    )
    print()
    print(dim(f"  Month {m4} (unreduced)  +  Day {d4} (unreduced)  +  "
              f"Year digit-sum {yd4} (not pre-reduced)  =  {chain_text(chain4)}"
              f"{'  (sacred, preserved)' if full_num > 9 else ''}"))
    print()
    print(wrap(
        "An adaptation rather than a documented gematria method: month and "
        "day keep their full (absolute) values while the year contributes "
        "only its digit sum (its small value), without early reduction. The "
        "mid-sized totals this produces are where sacred numbers such as 40, "
        "49, 50 and 70 can appear. The total is reduced the same way as "
        "Method 2."
    ))
    print()
    print(wrap(h4["descriptor"]))
    print()
    print(dim(wrap(f"Source note: {h4['note']}")))

    # ── Method 5: Bone'eh (Building Value) ────────────────────────────────────

    # Bone'eh is documented only as a Hebrew gematria method (Gematria
    # Wikipedia, "Other methods"); no Greek/Pythagorean counterpart is
    # documented in these sources, so its meaning is drawn from Hebrew
    # letter data only.
    boneeh_hebrew = lookup_hebrew(boneeh_num)
    subheader(
        f"METHOD 5 · BONE'EH (BUILDING VALUE)  —  {boneeh_num}",
        magenta
    )
    print()
    print(dim(
        f"  Components: Month → {bm}   Day → {bd}   Year → {by_}\n"
        f"  Step 1 (month):  prev_orig=0;       running = 0 + {bm} = {s1}\n"
        f"  Step 2 (day):    prev_orig={bm};      running = {s1} + ({bm}+{bd}) = {s2}\n"
        f"  Step 3 (year):   prev_orig={bm}+{bd}={bm+bd}; running = {s2} + ({bm}+{bd}+{by_}) = {s3}  →  {boneeh_num}"
    ))
    print()
    print(wrap(
        "Bone'eh (building value) walks through each 'letter' of a word and "
        "at each step adds the cumulative sum of all ORIGINAL letter values seen "
        "so far plus the current letter value to a running total -- not the "
        "bone'eh total itself (Gematria Wikipedia: achad = 1 + (1+8) + (1+8+4) "
        "= 23). This makes the result sensitive to sequence: earlier components "
        "carry more cumulative weight. The month, as the first 'letter' of the "
        "date, is thus the heaviest contributor (weight 3x), the day next (2x), "
        "and the year last (1x)."
    ))
    print()
    print(f"  {magenta(bold(str(boneeh_num)))}  Hebrew: {boneeh_hebrew['name']}")
    print()
    print(wrap(boneeh_hebrew["descriptor"]))

    # ── Synthesis ─────────────────────────────────────────────────────────────

    cd = COMBINED_DATA[combined_num]
    subheader(
        f"SYNTHESIS (GREEK ⊕ HEBREW BONE'EH)  —  {combined_num}  ·  {cd['name']}",
        magenta
    )
    print()
    print(wrap(
        f"The Greek Pythagorean value ({greek_num}) and the Hebrew Bone'eh "
        f"value ({boneeh_num}) are combined and reduced to a single synthesis "
        f"number: {combined_num}. Bone'eh is the Hebrew partner because it is "
        f"the only Hebrew method here whose digit can differ from the Greek "
        f"one -- Methods 2-4 always reduce to the same digit as Method 1."
    ))
    print()
    print(wrap(cd["descriptor"]))
    print()


# =============================================================================
# ARROW-KEY MENU
# (Same interaction style as the numerology-calculator launcher script:
#  Up/Down arrows move the highlighted ➤ selector, Enter confirms.)
# =============================================================================

def _get_key():
    """Read a single keypress (handles multi-byte arrow-key escape sequences)."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def run_menu(title, options):
    """
    Display an arrow-key navigable menu and return the selected option string.
    Mirrors the numerology-calculator bash launcher's highlighted ➤ style.
    """
    selected = 0
    while True:
        os.system("clear")
        print(bold(f"  {title}"))
        print("  " + "-" * len(title))
        for i, opt in enumerate(options):
            if i == selected:
                print(bold(f"➤ {opt}") + "\n")
            else:
                print(f"  {opt}\n")

        key = _get_key()
        if key == '\x1b[A':                       # Up arrow
            selected = (selected - 1) % len(options)
        elif key == '\x1b[B':                     # Down arrow
            selected = (selected + 1) % len(options)
        elif key in ('\r', '\n'):                  # Enter
            return options[selected]
        elif key == 'q':                           # quick-quit
            return "Quit"


# =============================================================================
# MODE RUNNERS
# =============================================================================

def run_date_mode():
    """Single date -> printed to the terminal."""
    date_str = input(bold("Enter a date (MM-DD-YYYY or MM/DD/YYYY): ")).strip()

    try:
        month, day, year = parse_date(date_str)
    except ValueError as e:
        print(f"\n  Error: {e}")
        return

    calculate_day(month, day, year)


def run_month_mode():
    """Every day in a chosen month -> printed to the terminal."""
    raw = input(bold("Enter month and year (MM-YYYY or MM/YYYY): ")).strip()

    try:
        month, year = parse_month_year(raw)
    except ValueError as e:
        print(f"\n  Error: {e}")
        return

    days_in_month = _calendar.monthrange(year, month)[1]

    print()
    print("=" * 72)
    print(f"  MONTH NUMEROLOGY  ·  {MONTH_NAMES[month]} {year}")
    print(f"  Calculating all {days_in_month} days  ·  5 methods each")
    print("=" * 72)

    for day in range(1, days_in_month + 1):
        calculate_day(month, day, year)

    print()
    print("=" * 72)
    print(f"  END OF {MONTH_NAMES[month].upper()} {year}")
    print("=" * 72)
    print()


def run_year_mode():
    """
    Every day in a chosen year -> printed to the terminal, saved to
    ~/calendar-numerology-<year>.txt (colour stripped from the saved file),
    AND plotted as an interactive, zoomable line graph saved to
    ~/calendar-numerology-<year>-graph.html.
    """
    raw = input(bold("Enter year (YYYY): ")).strip()

    try:
        year = int(raw)
    except ValueError:
        print("\n  Error: Year must be a number.")
        return
    if year < 1:
        print("\n  Error: Year must be positive.")
        return

    # ── Output file ──────────────────────────────────────────────────────────
    home_dir  = os.path.expanduser("~")
    out_path  = os.path.join(home_dir, f"calendar-numerology-{year}.txt")
    plain_buf = io.StringIO()

    # Tee all print() output: colour → terminal, plain → buffer
    original_stdout = sys.stdout
    sys.stdout = _TeeWriter(original_stdout, plain_buf)

    graph_dates, graph_values = [], []

    try:
        total_days = sum(
            _calendar.monthrange(year, m)[1] for m in range(1, 13)
        )

        print()
        print("=" * 72)
        print(f"  CALENDAR NUMEROLOGY  ·  FULL YEAR {year}")
        print(f"  Calculating all {total_days} days  ·  5 methods each")
        print("=" * 72)

        for month in range(1, 13):
            days_in_month = _calendar.monthrange(year, month)[1]

            print()
            print("=" * 72)
            print(f"  {MONTH_NAMES[month].upper()}  {year}  ·  {days_in_month} days")
            print("=" * 72)

            for day in range(1, days_in_month + 1):
                calculate_day(month, day, year)
                graph_dates.append(date(year, month, day))
                graph_values.append(compute_synthesis_number(month, day, year))

        print()
        print("=" * 72)
        print(f"  END OF {year}  ·  {total_days} days calculated")
        print("=" * 72)
        print()

    finally:
        sys.stdout = original_stdout          # always restore

    # ── Write plain-text file ────────────────────────────────────────────────
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(plain_buf.getvalue())

    print()
    print(bold(f"  Results saved to: {out_path}"))

    # ── Graph (highs & lows, star on peak days, x on low days) ───────────────
    graph_result = _build_year_graph(year, graph_dates, graph_values)
    if graph_result:
        graph_path, peaks_n, lows_n = graph_result
        print(bold(f"  Graph saved to: {graph_path}"))
        print(dim(
            f"  {peaks_n} peak day(s) marked with a star, {lows_n} low day(s) "
            f"marked with an x -- drag the range slider (or scroll/box-select "
            f"on the chart) to zoom into any week or day."
        ))
    else:
        print(dim(
            "  (Skipped the graph -- install 'plotly' to also get a "
            "zoomable HTML chart:  pip install plotly)"
        ))
    print()


def _build_year_graph(year, dates, values):
    """
    Build the interactive, zoomable highs & lows line graph for a year's
    worth of (date, synthesis_number) pairs and save it next to the .txt
    export as a self-contained HTML file.

    The line traces the daily high/low wave for the whole year. Peak
    days (9, "The Great Threshold") get a star marker; low days
    (1, "The Sovereign Origin") get an x marker. A range slider sits
    under the chart so the whole year stays visible while you drag to
    zoom into any week or day -- scrolling or box-selecting on the plot
    itself zooms too.

    Returns (out_path, peak_count, low_count), or None if the optional
    'plotly' package isn't installed.
    """
    try:
        import plotly.graph_objects as go
    except ImportError:
        return None

    peak_dates = [d for d, v in zip(dates, values) if v == 9]
    low_dates  = [d for d, v in zip(dates, values) if v == 1]

    def hover(d, v, tag=""):
        name = COMBINED_DATA[v]["name"]
        suffix = f" ({tag})" if tag else ""
        return f"{d:%B} {d.day}, {d.year}<br>Number {v} · {name}{suffix}"

    hover_main = [hover(d, v) for d, v in zip(dates, values)]
    hover_peak = [hover(d, 9, "peak") for d in peak_dates]
    hover_low  = [hover(d, 1, "low") for d in low_dates]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates, y=values, mode="lines", name="Daily number",
        line=dict(width=2, color="#2a78d6"),
        hovertext=hover_main, hoverinfo="text",
    ))
    fig.add_trace(go.Scatter(
        x=peak_dates, y=[9] * len(peak_dates), mode="markers",
        name="Peak day (9)",
        marker=dict(symbol="star", size=10, color="#0ca30c",
                    line=dict(width=1, color="#085041")),
        hovertext=hover_peak, hoverinfo="text",
    ))
    fig.add_trace(go.Scatter(
        x=low_dates, y=[1] * len(low_dates), mode="markers",
        name="Low day (1)",
        marker=dict(symbol="x", size=9, color="#d03b3b",
                    line=dict(width=1, color="#791f1f")),
        hovertext=hover_low, hoverinfo="text",
    ))

    # Dropped the "Date" axis title -- with the range slider on, it was
    # rendering right where the legend sits and colliding with "Peak day".
    # The month labels already make the axis self-explanatory. Also
    # opened up the figure generally (taller, bigger bottom margin) so
    # the plot, slider, and legend each get clear room of their own.
    fig.update_layout(
        title=dict(
            text=f"Calendar numerology {year} — daily synthesis (Greek ⊕ Hebrew Bone'eh)",
            x=0.5, xanchor="center", y=0.97, yanchor="top",
            font=dict(size=17),
        ),
        template="plotly_white",
        hovermode="closest",
        width=2600,
        height=650,
        legend=dict(
            orientation="h", x=0.5, xanchor="center", y=-0.40, yanchor="top",
            font=dict(size=11), bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(t=90, b=220, l=60, r=40),
    )
    fig.update_yaxes(title="Synthesis number", dtick=1, range=[0.5, 9.5])
    fig.update_xaxes(
        rangeslider=dict(visible=True),
    )

    home_dir = os.path.expanduser("~")
    out_path = os.path.join(home_dir, f"calendar-numerology-{year}-graph.html")
    fig.write_html(out_path)

    return out_path, len(peak_dates), len(low_dates)


# =============================================================================
# MAIN
# =============================================================================

def main():
    options = ["Date Calculator", "Month Calculator", "Year Calculator", "Quit"]
    choice = run_menu("Date Numerology Calculator", options)

    os.system("clear")

    if choice == "Date Calculator":
        run_date_mode()
    elif choice == "Month Calculator":
        run_month_mode()
    elif choice == "Year Calculator":
        run_year_mode()
    else:
        print(bold("\nExiting script"))
        return


if __name__ == "__main__":
    main()
