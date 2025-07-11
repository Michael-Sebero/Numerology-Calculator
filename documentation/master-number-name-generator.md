## Description

**Master Number Name Generator** searches thousands of first and middle name combinations to find names that produce master numbers - 11, 22, or 33 - in your numerological profile. By fixing your last name and birth date, the script systematically tests name pairings and surfaces combinations where one or more core numbers (Life Path, Soul Urge, Expression, or Personality) resolve to a master number via Pythagorean Numerology. This tool is designed for parents choosing a name, individuals exploring a name change, or anyone seeking a name aligned with master number energy.

## How to Use Master Number Name Generator

* Input your birth date, gender, last name, and optionally a fixed first name when prompted
* Configure optional filters for which master numbers and profile components to target
* The script searches all valid name combinations and calculates each numerological profile
* You'll receive a ranked list of matching names with their full numerological breakdown

```
Example:

Enter birth date (MM-DD-YYYY or MM/DD/YYYY): 03-20-2028
Enter gender (M/F): M
Enter last name: Floyd
Enter first name (optional): 

Optional Filters (press Enter to use defaults):
Target master numbers (default: 11,22,33): 
Target components (optional) [life_path, soul_urge, expression, personality]: 
Maximum results to show: 10

Searching for names with master numbers [11, 22, 33]
Target components: ['life_path', 'soul_urge', 'expression', 'personality']
Maximum results: 10
------------------------------------------------------------
Searching for names with master numbers [11, 22, 33] in components: ['life_path', 'soul_urge', 'expression', 'personality']
Checking 229 first names × 164 middle names = 37556 combinations...
This may take a moment...


Search complete! Checked 40 combinations.

============================================================
 FOUND 10 NAME COMBINATIONS WITH MASTER NUMBERS
============================================================

1. Aaron Aaron Floyd
   Life Path: 8
   Soul Urge: 22 ✅
   Expression: 7
   Personality: 3

2. Aaron Benjamin Floyd
   Life Path: 8
   Soul Urge: 11 ✅
   Expression: 8
   Personality: 6

3. Aaron Brian Floyd
   Life Path: 8
   Soul Urge: 6
   Expression: 11 ✅
   Personality: 5

4. Aaron Bruce Floyd
   Life Path: 8
   Soul Urge: 22 ✅
   Expression: 7
   Personality: 3

5. Aaron Bryan Floyd
   Life Path: 8
   Soul Urge: 22 ✅
   Expression: 9
   Personality: 5

6. Aaron Christian Floyd
   Life Path: 8
   Soul Urge: 33 ✅
   Expression: 5
   Personality: 8

7. Aaron Cole Floyd
   Life Path: 8
   Soul Urge: 7
   Expression: 11 ✅
   Personality: 4

8. Aaron Connor Floyd
   Life Path: 8
   Soul Urge: 8
   Expression: 1
   Personality: 11 ✅

9. Aaron Daniel Floyd
   Life Path: 8
   Soul Urge: 11 ✅
   Expression: 3
   Personality: 1

10. Aaron Dylan Floyd
    Life Path: 8
    Soul Urge: 22 ✅
    Expression: 5
    Personality: 1
```

## Understanding the Generator

### What Are Master Numbers?
Master numbers - 11, 22, and 33 - are special values in Pythagorean Numerology that are not reduced further to a single digit. They carry amplified energy and are considered rare and significant in a numerological profile.

### How the Search Works
The script holds your last name and birth date constant (since they are fixed), then systematically pairs every first name in its database with every middle name appropriate to your gender. For each three-part name combination, it calculates the full numerological profile and checks whether any targeted component resolves to a master number. Results are returned in the order they are discovered.

### Fixed First Name Option
If you provide a first name, the search is restricted to that name only, pairing it with all eligible middle names. This dramatically narrows the search space and is ideal when you already know the first name but want to find a middle name that introduces master number energy.

### Gender Selection
The script maintains separate curated lists of first and middle names for male and female searches. Entering M or F ensures results reflect culturally appropriate name pairings. If no gender is specified, both lists are combined.

### Target Master Numbers
By default the script searches for all three master numbers (11, 22, 33). You can restrict the search to specific master numbers - for example, entering `11` will return only name combinations where a targeted component resolves to 11 and not 22 or 33.

### Target Components
You can limit the search to one or more specific profile components: `life_path`, `soul_urge`, `expression`, and/or `personality`. By default all four components are checked. For example, specifying `expression` will only flag a name if its Expression number is a master number, ignoring the other three components.

### Maximum Results
Controls how many matching name combinations are returned before the search stops. The default is 10. Increasing this number will extend search time.

## How Numbers Are Calculated

### Life Path Number
Calculated from your birth date. The month, day, and year are each reduced separately to a single digit or master number, then summed and reduced again. Since your birth date is fixed, your Life Path number does not change regardless of what name is tested.

### Expression Number (Destiny Number)
Calculated from all letters in the full name using the Pythagorean chart. Each letter is assigned a value of 1–9, all values are summed, and the total is reduced - stopping if a master number is reached.

### Soul Urge Number (Heart's Desire)
Calculated from the vowels in the full name. A, E, I, O, and U each carry specific values (1, 5, 9, 6, and 3 respectively). Y is treated as a vowel when it follows a consonant and is not at the start of a syllable. All vowel values are summed and reduced.

### Personality Number
Calculated from the consonants in the full name. Y is treated as a consonant when it appears at the start of a name or immediately follows a vowel. All consonant values are summed and reduced.

### Master Number Preservation
At every reduction step, the script checks whether the current total is 11, 22, or 33. If it is, reduction stops and the master number is preserved rather than collapsed to a single digit.

## Pythagorean Letter Values

| Value | Letters         |
|-------|-----------------|
| 1     | A, J, S         |
| 2     | B, K, T         |
| 3     | C, L, U         |
| 4     | D, M, V         |
| 5     | E, N, W         |
| 6     | F, O, X         |
| 7     | G, P, Y         |
| 8     | H, Q, Z         |
| 9     | I, R            |

## Master Number Meanings

### 11 - The Intuitive
The Master Intuitive carries heightened spiritual sensitivity and inspirational potential. Names that produce an 11 in any component suggest a person wired for vision, psychic awareness, and the ability to uplift others through insight and creativity.

### 22 - The Master Builder
The most powerful of the master numbers in practical terms. Names producing a 22 suggest the capacity to channel grand visions into tangible reality. This number combines the sensitivity of 11 with the discipline and ambition needed to manifest large-scale achievements.

### 33 - The Master Teacher
The rarest master number, associated with selfless service, healing, and spiritual upliftment. Names producing a 33 suggest a life oriented toward compassion, guidance, and nurturing others on a broad scale. It is considered the number of the master healer and teacher.
