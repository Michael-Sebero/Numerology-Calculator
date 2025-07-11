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
    # Note: No grounded emotional letters according to official chart
    for letter in name:
        if letter in 'IORZBSTX':
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
    
    # Based on the official chart from numerology.center - corrected categorization
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

def get_pythagorean_weights():
    """Define weights for Pythagorean numbers - higher weight = more influence"""
    return {
        'life_path': 5,        # Primary life direction - highest weight (increased from 4)
        'expression': 4,       # Natural abilities - high weight (increased from 3)
        'soul_urge': 4,        # Inner desires - high weight (increased from 3)
        'personality': 3,      # Outer appearance - medium weight (increased from 2)
    }

def get_planes_weights():
    """Define weights for Planes of Expression numbers - higher weight = more influence"""
    return {
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

def get_confidence_level(score, system='pythagorean'):
    """Determine confidence level based on score and system"""
    if system == 'pythagorean':
        # Pythagorean system uses higher weights, so higher thresholds
        if score >= 15:
            return "High Confidence"
        elif score >= 10:
            return "Moderate Confidence"
        elif score >= 6:
            return "Low Confidence"
        else:
            return "Very Low Confidence"
    else:  # planes system
        # Planes system uses lower weights, so lower thresholds
        if score >= 10:
            return "High Confidence"
        elif score >= 7:
            return "Moderate Confidence"
        elif score >= 4:
            return "Low Confidence"
        else:
            return "Very Low Confidence"

def calculate_pythagorean_trait_scores(pythagorean_numbers):
    """Calculate weighted trait scores based on Pythagorean numbers"""
    weights = get_pythagorean_weights()
    core_traits = get_core_traits()
    
    positive_scores = {}
    negative_scores = {}
    
    # Calculate weighted scores for each trait
    for num_type, number in pythagorean_numbers.items():
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

def calculate_planes_trait_scores(planes_numbers):
    """Calculate weighted trait scores based on Planes of Expression numbers"""
    weights = get_planes_weights()
    core_traits = get_core_traits()
    
    positive_scores = {}
    negative_scores = {}
    
    # Calculate weighted scores for each trait
    for num_type, number in planes_numbers.items():
        if number in core_traits and number != 0:  # Skip zero values
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

def filter_significant_traits(trait_scores, min_score=4):
    """Filter traits that meet minimum significance threshold"""
    return {trait: score for trait, score in trait_scores.items() if score >= min_score}

def get_dominant_traits(trait_scores, max_traits=10):
    """Get the most dominant traits, limited by max_traits"""
    sorted_traits = sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_traits[:max_traits])

def display_traits_with_confidence(traits, system='pythagorean'):
    """Display traits with confidence levels"""
    if not traits:
        print("• No significant traits detected")
        return
    
    for trait, score in sorted(traits.items(), key=lambda x: x[1], reverse=True):
        confidence = get_confidence_level(score, system)
        print(f"• {trait.title()} ({confidence})")

def generate_identity_titles(pyth_dominant_positive, pyth_dominant_negative, planes_dominant_positive, planes_dominant_negative):
    """Generate descriptive identity titles based on dominant traits"""
    
    # Combine positive traits from both systems
    all_positive_traits = {}
    all_positive_traits.update(pyth_dominant_positive)
    for trait, score in planes_dominant_positive.items():
        if trait in all_positive_traits:
            all_positive_traits[trait] += score
        else:
            all_positive_traits[trait] = score
    
    # Combine negative traits from both systems
    all_negative_traits = {}
    all_negative_traits.update(pyth_dominant_negative)
    for trait, score in planes_dominant_negative.items():
        if trait in all_negative_traits:
            all_negative_traits[trait] += score
        else:
            all_negative_traits[trait] = score
    
    # Get top 3 traits for each category
    top_positive = sorted(all_positive_traits.items(), key=lambda x: x[1], reverse=True)[:3]
    top_negative = sorted(all_negative_traits.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Define trait combinations and their descriptive titles
    positive_combinations = {
        # Leadership combinations
        ('leadership', 'confidence'): "Confident Leader",
        ('leadership', 'ambition'): "Ambitious Leader",
        ('leadership', 'determination'): "Determined Leader",
        ('leadership', 'innovation'): "Innovative Leader",
        ('leadership', 'independence'): "Independent Leader",
        ('leadership', 'authority'): "Authoritative Leader",
        ('leadership', 'goal-oriented'): "Goal-Driven Leader",
        
        # Creative combinations
        ('creativity', 'expressiveness'): "Creative Communicator",
        ('creativity', 'inspiration'): "Inspirational Creative",
        ('creativity', 'enthusiasm'): "Enthusiastic Creative",
        ('creativity', 'artistic'): "Artistic Visionary",
        ('creativity', 'innovation'): "Creative Innovator",
        ('creativity', 'intuition'): "Intuitive Creative",
        
        # Spiritual/Intuitive combinations
        ('spirituality', 'intuition'): "Spiritual Intuitive",
        ('spirituality', 'wisdom'): "Wise Spiritual Guide",
        ('spirituality', 'healing'): "Spiritual Healer",
        ('intuition', 'sensitivity'): "Intuitive Empath",
        ('intuition', 'psychic ability'): "Psychic Intuitive",
        ('analytical', 'wisdom'): "Analytical Sage",
        
        # Nurturing/Service combinations
        ('nurturing', 'compassion'): "Compassionate Nurturer",
        ('nurturing', 'healing'): "Healing Caregiver",
        ('nurturing', 'service'): "Service-Oriented Helper",
        ('responsibility', 'compassion'): "Responsible Caregiver",
        ('humanitarianism', 'generosity'): "Generous Humanitarian",
        ('master teacher', 'healing'): "Master Healer-Teacher",
        
        # Business/Success combinations
        ('business acumen', 'ambition'): "Ambitious Entrepreneur",
        ('business acumen', 'efficiency'): "Efficient Business Leader",
        ('material success', 'organization'): "Organized Success Builder",
        ('master builder', 'practical vision'): "Visionary Builder",
        ('capability', 'transformation'): "Transformational Leader",
        
        # Communication/Social combinations
        ('communication', 'charm'): "Charismatic Communicator",
        ('diplomacy', 'cooperation'): "Diplomatic Peacemaker",
        ('expressiveness', 'optimism'): "Optimistic Communicator",
        ('peacemaking', 'sensitivity'): "Sensitive Peacemaker",
        
        # Analytical/Intellectual combinations
        ('analytical', 'perfectionism'): "Analytical Perfectionist",
        ('wisdom', 'introspection'): "Wise Contemplative",
        ('practical vision', 'organization'): "Visionary Organizer",
        ('reliability', 'practicality'): "Reliable Pragmatist",
        
        # Freedom/Adventure combinations
        ('freedom-loving', 'versatility'): "Free-Spirited Adventurer",
        ('adaptability', 'curiosity'): "Curious Adapter",
        ('progressive', 'dynamic'): "Progressive Innovator",
        ('pioneering', 'determination'): "Pioneering Trailblazer",
        
        # Default single trait titles
        'leadership': "Natural Leader",
        'creativity': "Creative Visionary",
        'spirituality': "Spiritual Seeker",
        'nurturing': "Caring Nurturer",
        'business acumen': "Business Visionary",
        'intuition': "Intuitive Guide",
        'analytical': "Deep Thinker",
        'humanitarianism': "Humanitarian Helper",
        'freedom-loving': "Free Spirit",
        'reliability': "Dependable Anchor",
        'ambition': "Driven Achiever",
        'wisdom': "Wise Counselor",
        'innovation': "Creative Innovator",
        'compassion': "Compassionate Soul",
        'independence': "Independent Spirit"
    }
    
    negative_combinations = {
        # Control/Domination combinations
        ('controlling', 'demanding'): "Controlling Perfectionist",
        ('domineering', 'impatience'): "Impatient Dominator",
        ('stubbornness', 'rigidity'): "Rigid Traditionalist",
        ('demanding', 'ruthlessness'): "Ruthless Perfectionist",
        ('controlling', 'superiority'): "Superior Controller",
        
        # Isolation/Withdrawal combinations
        ('aloofness', 'secretiveness'): "Secretive Loner",
        ('isolation', 'pessimism'): "Pessimistic Isolator",
        ('emotional distance', 'aloofness'): "Emotionally Distant Observer",
        ('oversensitivity', 'nervousness'): "Anxious Overthinker",
        ('withdrawal', 'introspection'): "Self-Isolating Thinker",
        
        # Instability/Chaos combinations
        ('restlessness', 'impulsiveness'): "Restless Wanderer",
        ('scatteredness', 'unreliability'): "Scattered Dreamer",
        ('moodiness', 'emotional distance'): "Moody Detacher",
        ('nervousness', 'extremism'): "Anxious Extremist",
        ('carelessness', 'irresponsibility'): "Careless Drifter",
        
        # Perfectionism/Criticism combinations
        ('perfectionism', 'criticism'): "Critical Perfectionist",
        ('fault-finding', 'sarcasm'): "Sarcastic Critic",
        ('narrow-mindedness', 'resistance to change'): "Closed-Minded Traditionalist",
        ('pessimism', 'overly serious'): "Pessimistic Worrier",
        
        # Materialism/Status combinations
        ('materialism', 'status-conscious'): "Status-Driven Materialist",
        ('workaholism', 'stress'): "Stressed Workaholic",
        ('materialism', 'ruthlessness'): "Ruthless Materialist",
        
        # Emotional/Sensitivity combinations
        ('oversensitivity', 'moodiness'): "Emotionally Volatile",
        ('worry', 'anxiety'): "Anxious Worrier",
        ('jealousy', 'interference'): "Jealous Meddler",
        ('dependency', 'insecurity'): "Insecure Dependent",
        ('martyrdom', 'over-sacrificing'): "Self-Sacrificing Martyr",
        
        # Impulsiveness/Recklessness combinations
        ('impulsiveness', 'carelessness'): "Reckless Impulsive",
        ('irresponsibility', 'addiction prone'): "Addictive Escapist",
        ('superficiality', 'extravagance'): "Superficial Spender",
        ('unrealistic', 'impracticality'): "Unrealistic Dreamer",
        
        # Default single trait titles
        'stubbornness': "Stubborn Resister",
        'oversensitivity': "Overly Sensitive",
        'impatience': "Impatient Rusher",
        'controlling': "Control Seeker",
        'aloofness': "Distant Observer",
        'restlessness': "Restless Wanderer",
        'materialism': "Material Pursuer",
        'pessimism': "Pessimistic Thinker",
        'moodiness': "Moody Fluctuator",
        'perfectionism': "Perfectionist Critic",
        'isolation': "Self-Isolator",
        'demanding': "Demanding Perfectionist",
        'rigidity': "Rigid Traditionalist",
        'selfishness': "Self-Centered Individual",
        'worry': "Chronic Worrier"
    }
    
    def create_title(traits, combinations, is_positive=True):
        """Create a descriptive title from traits"""
        if not traits:
            return "Balanced Individual" if is_positive else "Internally Conflicted"
        
        trait_names = [trait[0] for trait in traits]
        
        # Try to find combination matches
        for combo_key, title in combinations.items():
            if isinstance(combo_key, tuple):
                # Check if we have both traits in the combination
                if all(trait in trait_names for trait in combo_key):
                    # Add context based on remaining traits
                    remaining_traits = [t for t in trait_names if t not in combo_key]
                    if remaining_traits:
                        context_trait = remaining_traits[0].replace('-', ' ').replace('_', ' ')
                        if is_positive:
                            return f"{title} with {context_trait.title()} Drive"
                        else:
                            return f"{title} with {context_trait.title()} Issues"
                    return title
        
        # If no combination found, use single trait
        primary_trait = trait_names[0]
        if primary_trait in combinations:
            title = combinations[primary_trait]
            # Add context from secondary trait if available
            if len(trait_names) > 1:
                secondary_trait = trait_names[1].replace('-', ' ').replace('_', ' ')
                if is_positive:
                    return f"{title} with {secondary_trait.title()} Qualities"
                else:
                    return f"{title} with {secondary_trait.title()} Tendencies"
            return title
        
        # Fallback to formatted trait name
        formatted_trait = primary_trait.replace('-', ' ').replace('_', ' ').title()
        if is_positive:
            return f"{formatted_trait} Focused Individual"
        else:
            return f"{formatted_trait} Challenged Individual"
    
    positive_title = create_title(top_positive, positive_combinations, True)
    negative_title = create_title(top_negative, negative_combinations, False)
    
    return positive_title, negative_title

def display_identity_titles(positive_title, negative_title):
    """Display the generated identity titles"""
    print("\n" + "=" * 50)
    print(" IDENTITY PROFILE")
    print("=" * 50)
    
    print(f"\n\033[1mPositive Identity:\033[0m")
    print(f"{positive_title}")
    
    print(f"\n\033[1mNegative Identity:\033[0m")
    print(f"{negative_title}")

def main():
    """Main function to run the numerology calculator"""
    try:
        
        # Get user input
        name = input(f"\033[1mEnter your full name: \033[0m").strip()
        birth_date = input(f"\033[1mEnter your birth date (MM-DD-YYYY or MM/DD/YYYY): \033[0m").strip()
        
        if not name or not birth_date:
            print("Error: Please provide both name and birth date.")
            return
        
        # Calculate all numbers
        life_path = calculate_life_path(birth_date)
        expression = calculate_expression(name)
        soul_urge = calculate_soul_urge(name)
        personality = calculate_personality(name)
        
        # Calculate planes
        physical_plane = calculate_physical_plane(name)
        mental_plane = calculate_mental_plane(name)
        emotional_plane = calculate_emotional_plane(name)
        intuitive_plane = calculate_intuitive_plane(name)
        
        print("\n" + "=" * 50)
        print(f" NUMEROLOGY REPORT FOR: {name.upper()}")
        print("=" * 50)
        print(f"")
        
        # Display results
        print(f"\033[1mPythagorean Numerology Profile\033[0m")  
        print(f"Life Path: {life_path}")
        print(f"Soul Urge: {soul_urge}")
        print(f"Expression: {expression}")
        print(f"Personality: {personality}")
        print(f"")
        print(f"\033[1mPlanes of Expression Profile\033[0m")
        print(f"Physical Plane: {physical_plane}")
        print(f"Mental Plane: {mental_plane}")
        print(f"Emotional Plane: {emotional_plane}")
        print(f"Intuitive Plane: {intuitive_plane}")
        
        # Calculate trait scores
        pythagorean_numbers = {
            'life_path': life_path,
            'expression': expression,
            'soul_urge': soul_urge,
            'personality': personality
        }
        
        planes_numbers = {
            'physical_plane': physical_plane,
            'mental_plane': mental_plane,
            'emotional_plane': emotional_plane,
            'intuitive_plane': intuitive_plane
        }
        
        pyth_positive, pyth_negative = calculate_pythagorean_trait_scores(pythagorean_numbers)
        planes_positive, planes_negative = calculate_planes_trait_scores(planes_numbers)
        
        # Filter and get dominant traits
        pyth_significant_positive = filter_significant_traits(pyth_positive, 4)
        pyth_significant_negative = filter_significant_traits(pyth_negative, 4)
        planes_significant_positive = filter_significant_traits(planes_positive, 4)
        planes_significant_negative = filter_significant_traits(planes_negative, 4)
        
        pyth_dominant_positive = get_dominant_traits(pyth_significant_positive, 10)
        pyth_dominant_negative = get_dominant_traits(pyth_significant_negative, 10)
        planes_dominant_positive = get_dominant_traits(planes_significant_positive, 10)
        planes_dominant_negative = get_dominant_traits(planes_significant_negative, 10)
        
        
        print("\n" + "=" * 50)
        print(" PYTHAGOREAN TRAIT ANALYSIS")
        print("=" * 50)
        print(f"")
        
        print(f"\033[1mPositive Traits:\033[0m")
        display_traits_with_confidence(pyth_dominant_positive, 'pythagorean')
        print(f"")
        print(f"\033[1mNegative Traits:\033[0m")
        display_traits_with_confidence(pyth_dominant_negative, 'pythagorean')
        
        print("\n" + "=" * 50)
        print(" PLANES OF EXPRESSION TRAIT ANALYSIS")
        print("=" * 50)
        print(f"")
        
        print(f"\033[1mPositive Traits:\033[0m")
        display_traits_with_confidence(planes_dominant_positive, 'planes')
        print(f"")
        print(f"\033[1mNegative Traits:\033[0m")
        display_traits_with_confidence(planes_dominant_negative, 'planes')
        
        # Generate and display identity titles
        positive_title, negative_title = generate_identity_titles(
            pyth_dominant_positive, pyth_dominant_negative,
            planes_dominant_positive, planes_dominant_negative
        )
        
        display_identity_titles(positive_title, negative_title)
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please try again with valid input.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please try again.")

if __name__ == "__main__":
    main()
