#!/usr/bin/env python3

# ─────────────────────────────────────────────────────────────────────────────
# CALENDAR NUMEROLOGY CALCULATOR 
# Five distinct numerological methods applied to any date:
#
#   1. GREEK PYTHAGOREAN (Isopsephy tradition)
#      Each component (month, day, year) reduced to 1-9 individually,
#      then summed and reduced again.  Source: Numerology Wikipedia;
#      Gematria Wikipedia -- Pythagorean / Isopsephy section.
#
#   2. HEBREW STANDARD  (Mispar Hechrachi)
#      Same arithmetic as Method 1, but sacred sums (13, 18, 26, 36)
#      are preserved before final reduction.
#      Source: Gematria Wikipedia -- Standard encoding; MyJewishLearning.
#
#   3. MISPAR KATAN  (All-Digits / Small Value)
#      Every individual digit of the full date string MMDDYYYY is summed
#      directly -- no intermediate component reduction.  Sacred sums
#      (13, 18, 26, 36, 40, 49, 50, 70) preserved before final reduction.
#      Source: Gematria Wikipedia -- "Mispar katan calculates the value of
#      each letter, but truncates all of the zeros."
#
#   4. FULL COMPONENT  (Mispar Gadol-inspired)
#      Month and day are used at full unreduced face value; year is summed
#      to its digit total but NOT pre-reduced.  Total then reduced.
#      Sacred sums preserved.  This preserves the larger intermediate
#      magnitudes that mispar gadol keeps for final letters.
#      Source: Gematria Wikipedia -- "Mispar gadol counts the final forms
#      of the Hebrew letters as a continuation of the numerical sequence."
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
# Letter values from Mathers Table (The Kabbalah Unveiled, 1887);
# Significant numbers from MyJewishLearning; Kabbalah from Britannica.
# ─────────────────────────────────────────────────────────────────────────────


# =============================================================================
# UTILITY
# =============================================================================

def reduce_to_single_digit(n):
    """Mispar katan mispari: repeatedly sum digits until 1-9."""
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def parse_date(date_str):
    """Accept MM-DD-YYYY or MM/DD/YYYY."""
    sep = '-' if '-' in date_str else '/'
    parts = date_str.split(sep)
    if len(parts) != 3:
        raise ValueError("Use MM-DD-YYYY or MM/DD/YYYY.")
    m, d, y = int(parts[0]), int(parts[1]), int(parts[2])
    if not (1 <= m <= 12):
        raise ValueError("Month must be 1-12.")
    if not (1 <= d <= 31):
        raise ValueError("Day must be 1-31.")
    if y < 1:
        raise ValueError("Year must be positive.")
    return m, d, y


# =============================================================================
# FIVE CALCULATION METHODS
# =============================================================================

def method_pythagorean(month, day, year):
    """
    Method 1 — Greek Pythagorean / Isopsephy.
    Reduce each component individually, sum, reduce.
    Returns (r_month, r_day, r_year, raw_sum, final).
    """
    rm = reduce_to_single_digit(month)
    rd = reduce_to_single_digit(day)
    ry = reduce_to_single_digit(sum(int(d) for d in str(year)))
    raw = rm + rd + ry
    return rm, rd, ry, raw, reduce_to_single_digit(raw)


# Sacred sums reachable by the standard 3-component method (max raw = 27):
HEBREW_SACRED_STANDARD = {13, 18, 26}  # 36 is impossible (max = 27); keep 36 for doc faithfulness
HEBREW_SACRED_STANDARD = {13, 18, 26}


def method_hebrew_standard(month, day, year):
    """
    Method 2 — Hebrew Standard (Mispar Hechrachi).
    Same arithmetic as Method 1 but preserves documented sacred sums
    13 (Echad / divine mercy), 18 (Chai / life), 26 (YHVH) before
    any final reduction.
    Returns (r_month, r_day, r_year, raw_sum, final).
    """
    rm = reduce_to_single_digit(month)
    rd = reduce_to_single_digit(day)
    ry = reduce_to_single_digit(sum(int(d) for d in str(year)))
    raw = rm + rd + ry
    if raw in {13, 18, 26}:
        return rm, rd, ry, raw, raw          # preserve the sacred value
    return rm, rd, ry, raw, reduce_to_single_digit(raw)


# Expanded sacred set for methods 3-4 (larger intermediate values possible):
HEBREW_SACRED_EXTENDED = {13, 18, 26, 36, 40, 49, 50, 70}


def method_katan(month, day, year):
    """
    Method 3 — Mispar Katan (All-Digits Sum).
    Concatenate date as MMDDYYYY, sum every digit, reduce.
    Sacred sums from HEBREW_SACRED_EXTENDED preserved.
    Returns (digits_used, raw_sum, final).
    """
    # Zero-pad month and day to 2 digits, year to 4
    date_str = f"{month:02d}{day:02d}{year:04d}"
    digits = [int(c) for c in date_str]
    raw = sum(digits)
    if raw in HEBREW_SACRED_EXTENDED:
        return digits, raw, raw
    return digits, raw, reduce_to_single_digit(raw)


def method_full_component(month, day, year):
    """
    Method 4 — Full Component (Mispar Gadol-inspired).
    Use month and day at full face value; sum year digits but do NOT
    pre-reduce that total.  Preserve sacred sums.
    Returns (month_val, day_val, year_digit_sum, raw_sum, final).
    """
    year_ds = sum(int(d) for d in str(year))
    raw = month + day + year_ds
    if raw in HEBREW_SACRED_EXTENDED:
        return month, day, year_ds, raw, raw
    return month, day, year_ds, raw, reduce_to_single_digit(raw)


def method_boneeh(month, day, year):
    """
    Method 5 — Bone'eh (Building / Cumulative Value).
    Source (Gematria Wikipedia, p.5):
      "adding the value of all previous letters and the value of the
       current letter to the running total."
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
    y = reduce_to_single_digit(sum(int(c) for c in str(year)))

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


# =============================================================================
# GREEK DATA  (Pythagorean / Isopsephy tradition)
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
            "for five. Sephardic tzitzit knots correspond to letters of the "
            "Tetragrammaton. "
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
            "Tikkun (cosmic restoration) is a central Kabbalistic concept -- "
            "the Lurianic doctrine of repairing broken vessels -- connected to "
            "this number's joining function. Source: Kabbalah Britannica. "
        ),
        "descriptor": (
            "Vav -- the peg and nail, the fastener that holds things together. "
            "Six days of creation preceded Shabbat; Vav is the energy of active "
            "connection and building. In Lurianic Kabbalah, the great work of tikkun "
            "(cosmic restoration) is carried out through unceasing effort against "
            "what has broken apart. This date calls for the work of fastening: "
            "what has been separated, reconnected; what broken, repaired."
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
            "Gematria value: 9. Literal meaning: Serpent (Mathers Table). "
            "The provided sources give the letter name and value only; "
            "no additional symbolism for Tet appears in the five source documents. "
        ),
        "descriptor": (
            "Tet -- the serpent, gematria value 9. Nine is the last single digit, "
            "the boundary before the Pythagorean most-perfect Ten. Ancient traditions "
            "associated nine with threshold and completion: the Styx coiled nine times, "
            "Welsh law counted nine steps, Islamic cosmology arranged nine spheres. "
            "This date stands at the edge of the cycle, holding all that has come "
            "before the final count turns."
        ),
    },
    13: {
        "name": "Thirteen — Echad (Divine Unity & Mercy)",
        "note": (
            "Gematria: 13 = Echad (One): aleph[1]+het[8]+dalet[4]=13. Verified in "
            "Gematria Wikipedia: 'achad (one) is 1+8+4=13.' The 13 attributes of "
            "divine mercy are recited on High Holidays (Exodus 34). Age of Bar Mitzvah. "
            "Maimonides' 13 principles of faith, codified in the Yigdal prayer. "
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
            "Jewish practice: gifts are given in multiples of 18 as an act of blessing, "
            "and the toast L'chaim -- to life -- invokes this number directly. The "
            "central prayer, the Amidah, is still called the Shemonah Esreh (The "
            "Eighteen). This date is saturated with life-force -- the sacred, "
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
            "numerical signature is 26. In Sephardic tradition, the five knots of "
            "tzitzit fringes correspond to the letters of this Name. A date carrying "
            "26 holds the quiet weight of divine presence: not dramatic, simply here."
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
            "righteous people whose goodness, completely unknown even to themselves, "
            "is the sole reason existence continues. Thirty-six is also twice Chai "
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
            "extraordinary completion and repair takes shape. Six was perfect to the "
            "Greeks mathematically: sum and product and divisor-sum all coincide. In "
            "Hebrew tradition six days of creation precede Shabbat, and in Lurianic "
            "Kabbalah the work of tikkun (cosmic restoration) is the great ongoing act "
            "of reconnecting what has been broken apart. This date heals what is broken, "
            "closes what is open, and restores what perfection was always intended to look like."
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
# MAIN
# =============================================================================

import calendar as _calendar


def calculate_day(month, day, year):
    """Run all five numerology methods for a single date and print results."""

    # ── Run all five methods ──────────────────────────────────────────────────

    # Method 1: Greek Pythagorean
    rm1, rd1, ry1, raw1, final1 = method_pythagorean(month, day, year)
    greek_num = final1

    # Method 2: Hebrew Standard
    rm2, rd2, ry2, raw2, final2 = method_hebrew_standard(month, day, year)
    hebrew_std_num = final2

    # Method 3: Mispar Katan (All-Digits)
    digits3, raw3, final3 = method_katan(month, day, year)
    katan_num = final3

    # Method 4: Full Component (Gadol-inspired)
    m4, d4, yd4, raw4, final4 = method_full_component(month, day, year)
    gadol_num = final4

    # Method 5: Bone'eh (Building Value)
    bm, bd, by_, (s1, s2, s3), final5 = method_boneeh(month, day, year)
    boneeh_num = final5

    # Combined synthesis uses Greek + reduced Hebrew standard
    combined_num = reduce_to_single_digit(
        greek_num + reduce_to_single_digit(hebrew_std_num)
    )

    # ── Master header ─────────────────────────────────────────────────────────

    header(f"DATE  ·  {MONTH_NAMES[month]} {day}, {year}")

    # ── Summary table ─────────────────────────────────────────────────────────

    W = 72
    print()
    print("  " + "─" * (W - 4))
    print(f"  {'METHOD':<32}  {'CALCULATION':<22}  {'RESULT':>6}")
    print("  " + "─" * (W - 4))

    def row(label, calc, result, color_fn):
        sacred = " ★" if isinstance(result, int) and result > 9 else ""
        print(f"  {color_fn(label):<43}  {dim(calc):<22}  "
              f"{bold(color_fn(str(result)))}{sacred}")

    calc1 = f"{rm1}+{rd1}+{ry1}={raw1}→{final1}"
    row("1. Greek Pythagorean",          calc1,           greek_num,      cyan)

    sacred_flag = " ★" if hebrew_std_num > 9 else ""
    print(f"  {amber('2. Hebrew Standard (Hechrachi)'):<43}  "
          f"{dim(calc1):<22}  {bold(amber(str(hebrew_std_num)))}{sacred_flag}")

    digit_str = "+".join(str(d) for d in digits3)
    calc3 = f"digits→{raw3}→{final3}"
    row("3. Mispar Katan (All-Digits)",  calc3,           katan_num,      green)

    calc4 = f"{m4}+{d4}+{yd4}={raw4}→{final4}"
    row("4. Full Component (Gadol)",     calc4,           gadol_num,      blue)

    calc5 = f"3×{bm}+2×{bd}+{by_}={s3}→{final5}"
    row("5. Bone'eh (Building Value)",   calc5,           boneeh_num,     magenta)

    print("  " + "─" * (W - 4))
    print(f"  {magenta('SYNTHESIS (Greek ⊕ Hebrew Std)'):<43}  "
          f"{dim(f'{greek_num}+{reduce_to_single_digit(hebrew_std_num)}'+'→'+str(combined_num)):<22}  "
          f"{bold(magenta(str(combined_num)))}")
    print("  " + "─" * (W - 4))
    print()
    if any(x > 9 for x in [hebrew_std_num, katan_num, gadol_num]):
        print(dim("  ★ = sacred number preserved before final reduction"))
        print()

    # ── Method 1: Greek Pythagorean ───────────────────────────────────────────

    g = GREEK_DATA.get(greek_num, GREEK_DATA[9])
    subheader(
        f"METHOD 1 · GREEK PYTHAGOREAN (ISOPSEPHY)  —  {greek_num}  ·  {g['name']}",
        cyan
    )
    print()
    print(wrap(g["descriptor"]))
    print()
    print(dim(wrap(f"Source note: {g['note']}")))

    # ── Method 2: Hebrew Standard ─────────────────────────────────────────────

    h2 = lookup_hebrew(hebrew_std_num)
    preserved2 = " (sacred sum preserved)" if hebrew_std_num > 9 else ""
    subheader(
        f"METHOD 2 · HEBREW STANDARD (MISPAR HECHRACHI)  —  {hebrew_std_num}  ·  {h2['name']}{preserved2}",
        amber
    )
    print()
    print(wrap(h2["descriptor"]))
    print()
    print(dim(wrap(f"Source note: {h2['note']}")))

    # ── Method 3: Mispar Katan (All-Digits) ───────────────────────────────────

    h3 = lookup_hebrew(katan_num)
    preserved3 = " (sacred sum preserved)" if katan_num > 9 else ""
    digit_display = " + ".join(str(d) for d in digits3)
    subheader(
        f"METHOD 3 · MISPAR KATAN (ALL-DIGITS SUM)  —  {katan_num}  ·  {h3['name']}{preserved3}",
        green
    )
    print()
    print(dim(f"  Date digits: {digit_display} = {raw3}"
              f"{' (sacred, preserved)' if katan_num > 9 else ' → ' + str(katan_num)}"))
    print()
    print(wrap(
        "Mispar Katan sums all individual digits of the date without any "
        "intermediate component reduction, treating the full MMDDYYYY string "
        "as a sequence of values. Each zero is present but contributes nothing "
        "to the total, in keeping with the documented principle that this method "
        "'truncates all of the zeros.'"
    ))
    print()
    print(wrap(h3["descriptor"]))
    print()
    print(dim(wrap(f"Source note: {h3['note']}")))

    # ── Method 4: Full Component (Gadol-inspired) ─────────────────────────────

    h4 = lookup_hebrew(gadol_num)
    preserved4 = " (sacred sum preserved)" if gadol_num > 9 else ""
    subheader(
        f"METHOD 4 · FULL COMPONENT (MISPAR GADOL-INSPIRED)  —  {gadol_num}  ·  {h4['name']}{preserved4}",
        blue
    )
    print()
    print(dim(f"  Month {m4} (unreduced)  +  Day {d4} (unreduced)  +  "
              f"Year digit-sum {yd4} (not pre-reduced)  =  {raw4}"
              f"{' (sacred, preserved)' if gadol_num > 9 else ' → ' + str(gadol_num)}"))
    print()
    print(wrap(
        "In mispar gadol, larger letter forms (the 'final' forms of five Hebrew "
        "letters) retain values from 500 to 900 rather than being reduced. "
        "Applied to a date, this method preserves the full magnitudes of month "
        "and day as they are -- not pre-collapsing them to a single digit -- "
        "and sums the year's digits without early reduction, keeping the larger "
        "intermediate value before a single final reduction."
    ))
    print()
    print(wrap(h4["descriptor"]))
    print()
    print(dim(wrap(f"Source note: {h4['note']}")))

    # ── Method 5: Bone'eh (Building Value) ────────────────────────────────────

    h5 = GREEK_DATA.get(boneeh_num, GREEK_DATA[9])   # bone'eh is a structural method
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
        "bone'eh total itself. This makes the result sensitive to sequence: "
        "earlier components carry more cumulative weight, just as the first "
        "letters of a Hebrew word shape the resonance of those that follow. "
        "The month, as the first 'letter' of the date, is thus the heaviest "
        "contributor (weight 3x), the day next (2x), and the year last (1x)."
    ))
    print()
    print(f"  {magenta(bold(str(boneeh_num)))}  Greek: {h5['name']}  |  Hebrew: {boneeh_hebrew['name']}")
    print()
    print(wrap(h5["descriptor"]))

    # ── Synthesis ─────────────────────────────────────────────────────────────

    cd = COMBINED_DATA.get(combined_num, COMBINED_DATA[9])
    subheader(
        f"SYNTHESIS (GREEK ⊕ HEBREW STANDARD)  —  {combined_num}  ·  {cd['name']}",
        magenta
    )
    print()
    print(wrap(
        f"The Greek Pythagorean value ({greek_num}) and the Hebrew Standard value "
        f"({hebrew_std_num}, reduced to "
        f"{reduce_to_single_digit(hebrew_std_num)}) are combined and reduced to "
        f"a single synthesis number: {combined_num}."
    ))
    print()
    print(wrap(cd["descriptor"]))
    print()


def main():
    raw = input(bold("Enter month and year (MM-YYYY or MM/YYYY): ")).strip()

    sep = '-' if '-' in raw else '/'
    parts = raw.split(sep)
    if len(parts) != 2:
        print("\n  Error: Use MM-YYYY or MM/YYYY.")
        return
    try:
        month, year = int(parts[0]), int(parts[1])
    except ValueError:
        print("\n  Error: Month and year must be numbers.")
        return
    if not (1 <= month <= 12):
        print("\n  Error: Month must be 1-12.")
        return
    if year < 1:
        print("\n  Error: Year must be positive.")
        return

    days_in_month = _calendar.monthrange(year, month)[1]

    print()
    print("=" * 72)
    print(f"  CALENDAR NUMEROLOGY  ·  {MONTH_NAMES[month]} {year}")
    print(f"  Calculating all {days_in_month} days  ·  5 methods each")
    print("=" * 72)

    for day in range(1, days_in_month + 1):
        calculate_day(month, day, year)

    print()
    print("=" * 72)
    print(f"  END OF {MONTH_NAMES[month].upper()} {year}")
    print("=" * 72)
    print()


if __name__ == "__main__":
    main()
