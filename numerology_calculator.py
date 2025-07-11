#!/usr/bin/env python3

def get_letter_value(letter):
    """Convert letter to numerological value using Pythagorean system"""
    letter_values = {
        'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
        'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
        'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
    }
    return letter_values.get(letter.upper(), 0)

def reduce_to_single_digit(number):
    """Reduce number to single digit, preserving master numbers 11, 22, 33"""
    if number in [11, 22, 33]:
        return number
    
    while number > 9:
        number = sum(int(digit) for digit in str(number))
        if number in [11, 22, 33]:
            return number
    
    return number

def calculate_life_path(birth_date):
    """Calculate Life Path number from birth date"""
    try:
        # Parse the date (MM-DD-YYYY or MM/DD/YYYY)
        if '-' in birth_date:
            parts = birth_date.split('-')
        elif '/' in birth_date:
            parts = birth_date.split('/')
        else:
            raise ValueError("Invalid date format")
        
        month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
        
        # Reduce each part separately first
        reduced_month = reduce_to_single_digit(month)
        reduced_day = reduce_to_single_digit(day)
        
        # Reduce year by adding all digits first, then reducing
        year_sum = sum(int(digit) for digit in str(year))
        reduced_year = reduce_to_single_digit(year_sum)
        
        # Add the three reduced parts and reduce again
        total = reduced_month + reduced_day + reduced_year
        return reduce_to_single_digit(total)
        
    except (ValueError, IndexError):
        raise ValueError("Invalid date format. Please use MM-DD-YYYY or MM/DD/YYYY")

def get_vowels(name):
    """Extract vowels from name, including Y when used as vowel"""
    vowels = []
    name = name.upper().replace(' ', '')
    vowel_letters = 'AEIOU'
    
    for i, letter in enumerate(name):
        if letter in vowel_letters:
            vowels.append(letter)
        elif letter == 'Y':
            # Include Y if it's used as a vowel (simple heuristic)
            # Y is typically a vowel when not at the beginning of a syllable
            if i > 0 and name[i-1] not in vowel_letters:
                vowels.append(letter)
    
    return vowels

def get_consonants(name):
    """Extract consonants from name"""
    consonants = []
    name = name.upper().replace(' ', '')
    vowel_letters = 'AEIOU'
    
    for i, letter in enumerate(name):
        if letter.isalpha() and letter not in vowel_letters:
            if letter == 'Y':
                # Include Y as consonant if at beginning or after vowel
                if i == 0 or name[i-1] in vowel_letters:
                    consonants.append(letter)
            else:
                consonants.append(letter)
    
    return consonants

def get_physical_plane_letters(name):
    """Extract Physical Plane letters from name"""
    physical_plane_letters = []
    name = name.upper().replace(' ', '')
    
    # Physical Plane letters: E (Creative), W (Vacillating), D, M (Grounded)
    for letter in name:
        if letter in 'EWDM':
            physical_plane_letters.append(letter)
    
    return physical_plane_letters

def get_mental_plane_letters(name):
    """Extract Mental Plane letters from name"""
    mental_plane_letters = []
    name = name.upper().replace(' ', '')
    
    # Mental Plane letters: A (Creative), H, J, N, P (Vacillating), G, L (Grounded)
    for letter in name:
        if letter in 'AHJNPGL':
            mental_plane_letters.append(letter)
    
    return mental_plane_letters

def get_emotional_plane_letters(name):
    """Extract Emotional Plane letters from name"""
    emotional_plane_letters = []
    name = name.upper().replace(' ', '')
    
    # Emotional Plane letters: I, O, R, Z (Creative), B, S, T, X (Vacillating)
    # Note: No grounded emotional letters according to documentation
    for letter in name:
        if letter in 'IORZSTXB':
            emotional_plane_letters.append(letter)
    
    return emotional_plane_letters

def get_intuitive_plane_letters(name):
    """Extract Intuitive Plane letters from name"""
    intuitive_plane_letters = []
    name = name.upper().replace(' ', '')
    
    # Intuitive Plane letters: K (Creative), F, Q, U, Y (Vacillating), C, V (Grounded)
    for letter in name:
        if letter in 'KFQUYCV':
            intuitive_plane_letters.append(letter)
    
    return intuitive_plane_letters

def calculate_soul_urge(name):
    """Calculate Soul Urge number from vowels in name"""
    vowels = get_vowels(name)
    
    # Special vowel values
    vowel_values = {'A': 1, 'E': 5, 'I': 9, 'O': 6, 'U': 3, 'Y': 7}
    
    total = sum(vowel_values.get(vowel, 0) for vowel in vowels)
    return reduce_to_single_digit(total)

def calculate_expression(name):
    """Calculate Expression number from all letters in name"""
    name = name.upper().replace(' ', '')
    total = sum(get_letter_value(letter) for letter in name if letter.isalpha())
    return reduce_to_single_digit(total)

def calculate_physical_plane(name):
    """Calculate Physical Plane number from Physical Plane letters only"""
    physical_letters = get_physical_plane_letters(name)
    if not physical_letters:
        return 0
    total = sum(get_letter_value(letter) for letter in physical_letters)
    return reduce_to_single_digit(total)

def calculate_mental_plane(name):
    """Calculate Mental Plane number from Mental Plane letters only"""
    mental_letters = get_mental_plane_letters(name)
    if not mental_letters:
        return 0
    total = sum(get_letter_value(letter) for letter in mental_letters)
    return reduce_to_single_digit(total)

def calculate_emotional_plane(name):
    """Calculate Emotional Plane number from Emotional Plane letters only"""
    emotional_letters = get_emotional_plane_letters(name)
    if not emotional_letters:
        return 0
    total = sum(get_letter_value(letter) for letter in emotional_letters)
    return reduce_to_single_digit(total)

def calculate_intuitive_plane(name):
    """Calculate Intuitive Plane number from Intuitive Plane letters only"""
    intuitive_letters = get_intuitive_plane_letters(name)
    if not intuitive_letters:
        return 0
    total = sum(get_letter_value(letter) for letter in intuitive_letters)
    return reduce_to_single_digit(total)

def calculate_personality(name):
    """Calculate Personality number from consonants in name"""
    consonants = get_consonants(name)
    total = sum(get_letter_value(consonant) for consonant in consonants)
    return reduce_to_single_digit(total)

def get_creative_grounded_vacillating_totals(name):
    """Calculate totals for Creative, Vacillating, and Grounded letters"""
    name = name.upper().replace(' ', '')
    
    # Based on the documentation table - corrected categorization
    creative_letters = 'EAIORZK'      # E, A, I, O, R, Z, K
    vacillating_letters = 'WHJNPBSTXFQUY'  # W, H, J, N, P, B, S, T, X, F, Q, U, Y
    grounded_letters = 'DMGLCV'       # D, M, G, L, C, V
    
    creative_total = sum(get_letter_value(letter) for letter in name if letter in creative_letters)
    vacillating_total = sum(get_letter_value(letter) for letter in name if letter in vacillating_letters)
    grounded_total = sum(get_letter_value(letter) for letter in name if letter in grounded_letters)
    
    return {
        'creative': reduce_to_single_digit(creative_total),
        'vacillating': reduce_to_single_digit(vacillating_total),
        'grounded': reduce_to_single_digit(grounded_total)
    }

def get_trait_weights():
    """Define weights for each number type - higher weight = more influence"""
    return {
        'life_path': 4,        # Primary life direction - highest weight
        'expression': 3,       # Natural abilities - high weight
        'soul_urge': 3,        # Inner desires - high weight
        'personality': 2,      # Outer appearance - medium weight
        'physical_plane': 2,   # Physical expression - medium weight
        'mental_plane': 2,     # Mental expression - medium weight
        'emotional_plane': 2,  # Emotional expression - medium weight
        'intuitive_plane': 2   # Intuitive expression - medium weight
    }

def get_core_traits():
    """Define core traits for each number with strength ratings"""
    return {
        1: {
            "positive": {
                "leadership": 5, "independence": 5, "pioneering": 4, "confidence": 4, 
                "determination": 4, "innovation": 3, "ambition": 3
            },
            "negative": {
                "impatience": 4, "stubbornness": 4, "selfishness": 3, "domineering": 3, 
                "impulsiveness": 3, "intolerance": 2
            }
        },
        2: {
            "positive": {
                "cooperation": 5, "diplomacy": 5, "sensitivity": 4, "peacemaking": 4, 
                "supportiveness": 4, "intuition": 3, "gentleness": 3
            },
            "negative": {
                "oversensitivity": 4, "indecisiveness": 4, "dependency": 3, "moodiness": 3, 
                "passive-aggressiveness": 3, "insecurity": 2
            }
        },
        3: {
            "positive": {
                "creativity": 5, "expressiveness": 5, "optimism": 4, "charm": 4, 
                "communication": 4, "enthusiasm": 3, "inspiration": 3
            },
            "negative": {
                "scatteredness": 4, "superficiality": 4, "moodiness": 3, "gossip": 3, 
                "extravagance": 3, "criticism": 2
            }
        },
        4: {
            "positive": {
                "reliability": 5, "practicality": 5, "organization": 4, "hard work": 4, 
                "loyalty": 4, "honesty": 3, "methodical": 3
            },
            "negative": {
                "rigidity": 4, "narrow-mindedness": 4, "pessimism": 3, "stubbornness": 3, 
                "overly serious": 3, "resistance to change": 2
            }
        },
        5: {
            "positive": {
                "freedom-loving": 5, "versatility": 5, "adaptability": 4, "curiosity": 4, 
                "progressive": 4, "dynamic": 3, "quick-witted": 3
            },
            "negative": {
                "restlessness": 4, "irresponsibility": 4, "impulsiveness": 3, "unreliability": 3, 
                "carelessness": 3, "addiction prone": 2
            }
        },
        6: {
            "positive": {
                "nurturing": 5, "responsibility": 5, "compassion": 4, "healing": 4, 
                "family-oriented": 4, "harmony": 3, "service": 3
            },
            "negative": {
                "interference": 4, "worry": 4, "controlling": 3, "jealousy": 3, 
                "anxiety": 3, "self-righteousness": 2
            }
        },
        7: {
            "positive": {
                "analytical": 5, "spiritual": 5, "wisdom": 4, "introspection": 4, 
                "intuition": 4, "perfectionism": 3, "mystery": 3
            },
            "negative": {
                "aloofness": 4, "pessimism": 4, "secretiveness": 3, "isolation": 3, 
                "sarcasm": 3, "fault-finding": 2
            }
        },
        8: {
            "positive": {
                "ambition": 5, "business acumen": 5, "authority": 4, "efficiency": 4, 
                "material success": 4, "organization": 3, "goal-oriented": 3
            },
            "negative": {
                "materialism": 4, "workaholism": 4, "demanding": 3, "ruthlessness": 3, 
                "status-conscious": 3, "stress": 2
            }
        },
        9: {
            "positive": {
                "humanitarianism": 5, "generosity": 5, "wisdom": 4, "compassion": 4, 
                "tolerance": 4, "artistic": 3, "global thinking": 3
            },
            "negative": {
                "impracticality": 4, "emotional distance": 4, "moodiness": 3, "resentment": 3, 
                "superiority": 3, "financial carelessness": 2
            }
        },
        11: {
            "positive": {
                "intuition": 5, "inspiration": 5, "spirituality": 4, "idealism": 4, 
                "vision": 4, "sensitivity": 3, "psychic ability": 3
            },
            "negative": {
                "oversensitivity": 4, "impracticality": 4, "nervousness": 3, "extremism": 3, 
                "unrealistic": 3, "fanaticism": 2
            }
        },
        22: {
            "positive": {
                "master builder": 5, "practical vision": 5, "transformation": 4, "capability": 4, 
                "organization": 4, "inspiration": 3, "dedication": 3
            },
            "negative": {
                "demanding": 4, "controlling": 4, "impatience": 3, "stress": 3, 
                "domineering": 3, "nervous energy": 2
            }
        },
        33: {
            "positive": {
                "master teacher": 5, "healing": 5, "spiritual service": 4, "altruism": 4, 
                "devotion": 4, "compassion": 3, "inspiration": 3
            },
            "negative": {
                "martyrdom": 4, "over-sacrificing": 4, "superiority": 3, "controlling": 3, 
                "burn-out": 3, "emotional demands": 2
            }
        }
    }

def calculate_trait_scores(numbers):
    """Calculate weighted trait scores based on all numbers"""
    weights = get_trait_weights()
    core_traits = get_core_traits()
    
    positive_scores = {}
    negative_scores = {}
    
    # Calculate weighted scores for each trait
    for num_type, number in numbers.items():
        if number in core_traits:
            weight = weights[num_type]
            
            # Add positive traits
            for trait, strength in core_traits[number]["positive"].items():
                if trait not in positive_scores:
                    positive_scores[trait] = 0
                positive_scores[trait] += strength * weight
            
            # Add negative traits
            for trait, strength in core_traits[number]["negative"].items():
                if trait not in negative_scores:
                    negative_scores[trait] = 0
                negative_scores[trait] += strength * weight
    
    return positive_scores, negative_scores

def filter_significant_traits(trait_scores, min_score=8):
    """Filter traits that meet minimum significance threshold"""
    return {trait: score for trait, score in trait_scores.items() if score >= min_score}

def get_dominant_traits(trait_scores, max_traits=8):
    """Get the most dominant traits, limited by max_traits"""
    sorted_traits = sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_traits[:max_traits])

def main():
    try:
        name = input("Enter your full name (as on birth certificate): ").strip()
        if not name:
            raise ValueError("Name cannot be empty")
        
        birth_date = input("Enter your birth date (MM-DD-YYYY or MM/DD/YYYY): ").strip()
        if not birth_date:
            raise ValueError("Birth date cannot be empty")
        
        print("\n" + "=" * 50)
        print(f" NUMEROLOGY REPORT FOR: {name.upper()}")
        print("=" * 50)
        
        # Calculate all numbers
        numbers = {
            'life_path': calculate_life_path(birth_date),
            'physical_plane': calculate_physical_plane(name),
            'mental_plane': calculate_mental_plane(name),
            'emotional_plane': calculate_emotional_plane(name),
            'intuitive_plane': calculate_intuitive_plane(name),
            'soul_urge': calculate_soul_urge(name),
            'expression': calculate_expression(name),
            'personality': calculate_personality(name)
        }
        
        # Calculate Creative/Grounded/Vacillating totals
        cgv_totals = get_creative_grounded_vacillating_totals(name)
        
        # Display calculated numbers
        print()
        print(f"\033[1mPythagorean Numerology Profile\033[0m")      
        print(f"Life Path:        {numbers['life_path']}")
        print(f"Soul Urge:        {numbers['soul_urge']}")
        print(f"Expression:       {numbers['expression']}")
        print(f"Personality:      {numbers['personality']}")
        print(f"")
        print(f"\033[1mPlanes of Expression Profile\033[0m")         
        print(f"Physical Plane:   {numbers['physical_plane']}")
        print(f"Mental Plane:     {numbers['mental_plane']}")
        print(f"Emotional Plane:  {numbers['emotional_plane']}")
        print(f"Intuitive Plane:  {numbers['intuitive_plane']}")
        
        # Calculate trait scores
        positive_scores, negative_scores = calculate_trait_scores(numbers)
        
        # Filter and get dominant traits
        significant_positive = filter_significant_traits(positive_scores)
        significant_negative = filter_significant_traits(negative_scores)
        
        dominant_positive = get_dominant_traits(significant_positive)
        dominant_negative = get_dominant_traits(significant_negative)
        
        # Display results
        print("\n" + "=" * 50)
        print(" POSITIVE TRAITS & STRENGTHS")
        print("=" * 50)
        print()
        if dominant_positive:
            for trait, score in sorted(dominant_positive.items(), key=lambda x: x[1], reverse=True):
                intensity = "High Confidence" if score >= 15 else "Moderate Confidence" if score >= 12 else "Low Confidence"
                print(f"• {trait.title()} ({intensity})")
        
        print("\n" + "=" * 50)
        print(" NEGATIVE TRAITS & WEAKNESSES")
        print("=" * 50)
        print()
        if dominant_negative:
            for trait, score in sorted(dominant_negative.items(), key=lambda x: x[1], reverse=True):
                intensity = "High Confidence" if score >= 15 else "Moderate Confidence" if score >= 12 else "Low Confidence"
                print(f"• {trait.title()} ({intensity})")
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please try again with valid input.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please try again.")

if __name__ == "__main__":
    main()
