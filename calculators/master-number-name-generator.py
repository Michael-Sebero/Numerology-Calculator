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

def calculate_personality(name):
    """Calculate Personality number from consonants in name"""
    consonants = get_consonants(name)
    total = sum(get_letter_value(consonant) for consonant in consonants)
    return reduce_to_single_digit(total)

def get_male_names():
    """Return list of popular male first names"""
    return [
        "Aaron", "Abel", "Abraham", "Adam", "Adrian", "Aidan", "Alan", "Albert", "Alec",
        "Alexander", "Alfred", "Andre", "Andrew", "Anthony", "Antonio", "Archer", "Arthur",
        "Ashton", "Austin", "Avery", "Axel", "Barron", "Barry", "Benjamin", "Bennett", "Blake", 
        "Bradley", "Brandon", "Brayden", "Brian", "Bruce", "Bryan", "Caleb", "Calvin",
        "Cameron", "Carl", "Carter", "Chandler", "Charles", "Chase", "Christian", "Christopher",
        "Clayton", "Colby", "Cole", "Colin", "Connor", "Cooper", "Corey", "Cory", "Craig",
        "Curtis", "Dale", "Damian", "Daniel", "Danny", "Darren", "David", "Dean", "Dennis",
        "Derek", "Devin", "Diego", "Dominic", "Donald", "Douglas", "Drew", "Duncan", "Dylan",
        "Earl", "Eddie", "Edgar", "Edward", "Eli", "Elijah", "Elliott", "Eric", "Ernest",
        "Ethan", "Eugene", "Evan", "Felix", "Fernando", "Frank", "Franklin", "Frederick",
        "Gabriel", "Garrett", "Gary", "Gavin", "George", "Gerald", "Gilbert", "Gordon",
        "Graham", "Grant", "Gregory", "Griffin", "Harold", "Harrison", "Harvey", "Hayden",
        "Hector", "Henry", "Hudson", "Hugh", "Hunter", "Ian", "Isaac", "Isaiah", "Ivan",
        "Jack", "Jackson", "Jacob", "Jake", "James", "Jared", "Jason", "Javier", "Jay",
        "Jeffrey", "Jeremy", "Jerome", "Jesse", "Jesus", "Joel", "John", "Jonah", "Jonathan",
        "Jordan", "Jose", "Joseph", "Joshua", "Juan", "Julian", "Julius", "Justin", "Karl",
        "Keith", "Kenneth", "Kevin", "Kyle", "Lance", "Larry", "Lawrence", "Leo", "Leonard",
        "Levi", "Lewis", "Liam", "Lincoln", "Logan", "Louis", "Lucas", "Luke", "Malcolm",
        "Marcus", "Mark", "Martin", "Mason", "Matthew", "Maurice", "Max", "Maxwell", "Michael",
        "Miles", "Mitchell", "Morgan", "Nathan", "Nathaniel", "Neil", "Nicholas", "Noah",
        "Nolan", "Oliver", "Omar", "Oscar", "Owen", "Parker", "Patrick", "Paul", "Peter",
        "Philip", "Preston", "Quentin", "Ralph", "Randall", "Raymond", "Reed", "Richard",
        "Riley", "Robert", "Roger", "Ronald", "Ross", "Roy", "Russell", "Ryan", "Samuel",
        "Scott", "Sean", "Sebastian", "Shane", "Shawn", "Simon", "Spencer", "Stephen",
        "Steven", "Stewart", "Theodore", "Thomas", "Timothy", "Todd", "Tommy", "Tony",
        "Travis", "Trevor", "Tyler", "Victor", "Vincent", "Wade", "Walter", "Warren",
        "Wayne", "Wesley", "William", "Wyatt", "Xavier", "Zachary"
    ]

def get_female_names():
    """Return list of popular female first names"""
    return [
        "Abigail", "Ada", "Addison", "Adelaide", "Adriana", "Adrienne", "Agnes", "Alexandra",
        "Alice", "Allison", "Amanda", "Amber", "Amelia", "Amy", "Andrea", "Angela", "Angelica",
        "Anita", "Anna", "Anne", "Annie", "Aria", "Ariana", "Ashley", "Aubrey", "Audrey",
        "Aurora", "Ava", "Avery", "Barbara", "Beatrice", "Bella", "Beth", "Betty", "Beverly",
        "Bianca", "Bonnie", "Brenda", "Brianna", "Bridget", "Brittany", "Brooke", "Brooklyn",
        "Camila", "Candace", "Carmen", "Carol", "Caroline", "Carolyn", "Catherine", "Cathy",
        "Charlotte", "Chelsea", "Cheryl", "Chloe", "Christina", "Christine", "Clara", "Claire",
        "Claudia", "Courtney", "Crystal", "Cynthia", "Daisy", "Dana", "Danielle", "Dawn",
        "Deborah", "Debra", "Denise", "Diana", "Diane", "Dolores", "Donna", "Doris", "Dorothy",
        "Eden", "Edith", "Eleanor", "Elizabeth", "Ella", "Ellen", "Emily", "Emma", "Erin",
        "Esther", "Eva", "Evelyn", "Faith", "Fiona", "Frances", "Gabriella", "Gail", "Georgia",
        "Gina", "Gloria", "Grace", "Hailey", "Hannah", "Harper", "Heather", "Helen", "Holly",
        "Hope", "Isabella", "Isabelle", "Ivy", "Jackie", "Jacqueline", "Jane", "Janet",
        "Janice", "Jasmine", "Jean", "Jenna", "Jennifer", "Jessica", "Jill", "Joan", "Joanne",
        "Jocelyn", "Jordan", "Josephine", "Joyce", "Judith", "Judy", "Julia", "Julie", "June",
        "Karen", "Katherine", "Kathleen", "Kathryn", "Katie", "Kayla", "Kelly", "Kendra",
        "Kennedy", "Kimberly", "Kylie", "Laura", "Lauren", "Leah", "Leslie", "Lillian", "Lily",
        "Linda", "Lisa", "Lori", "Louise", "Lucy", "Luna", "Lynn", "Madison", "Margaret",
        "Maria", "Marie", "Marilyn", "Martha", "Mary", "Megan", "Melanie", "Melissa", "Mia",
        "Michelle", "Mila", "Miranda", "Monica", "Morgan", "Nancy", "Naomi", "Natalie",
        "Natasha", "Nicole", "Nina", "Nora", "Olivia", "Paige", "Pamela", "Patricia", "Paula",
        "Penelope", "Phoenix", "Phyllis", "Quinn", "Rachel", "Rebecca", "Regina", "Riley",
        "Robin", "Rosa", "Rose", "Ruby", "Ruth", "Samantha", "Sandra", "Sara", "Sarah",
        "Savannah", "Scarlett", "Sharon", "Shirley", "Sophia", "Stephanie", "Susan", "Suzanne",
        "Taylor", "Teresa", "Theresa", "Tiffany", "Tracy", "Valentina", "Valerie", "Vanessa",
        "Vera", "Victoria", "Violet", "Virginia", "Vivian", "Wendy", "Whitney", "Zoe", "Zoey"
    ]

def get_male_middle_names():
    """Return list of popular male middle names"""
    return [
        "Aaron", "Abel", "Adam", "Alan", "Albert", "Alexander", "Andre", "Andrew", "Anthony",
        "Antonio", "Arthur", "Austin", "Benjamin", "Blake", "Bradley", "Brandon", "Brian",
        "Bruce", "Bryan", "Caleb", "Calvin", "Carl", "Carter", "Charles", "Chase", "Christian",
        "Christopher", "Cole", "Connor", "Craig", "Curtis", "Dale", "Daniel", "David", "Dean",
        "Dennis", "Derek", "Douglas", "Drew", "Dylan", "Earl", "Eddie", "Edward", "Eli",
        "Elliott", "Eric", "Ernest", "Ethan", "Eugene", "Evan", "Felix", "Frank", "Franklin",
        "Frederick", "Gabriel", "Gary", "George", "Gerald", "Gilbert", "Gordon", "Graham",
        "Grant", "Gregory", "Harold", "Harrison", "Harvey", "Henry", "Hugh", "Hunter", "Ian",
        "Isaac", "Isaiah", "Jack", "Jacob", "James", "Jared", "Jason", "Jay", "Jeffrey",
        "Jeremy", "Jerome", "Jesse", "Joel", "John", "Jonathan", "Jordan", "Jose", "Joseph",
        "Joshua", "Julian", "Justin", "Keith", "Kenneth", "Kevin", "Kyle", "Lance", "Larry",
        "Lawrence", "Lee", "Leo", "Leonard", "Lewis", "Louis", "Lucas", "Luke", "Malcolm",
        "Marcus", "Mark", "Martin", "Matthew", "Maurice", "Max", "Michael", "Miles", "Mitchell",
        "Nathan", "Neil", "Nicholas", "Noah", "Oliver", "Oscar", "Owen", "Parker", "Patrick",
        "Paul", "Peter", "Philip", "Preston", "Ralph", "Raymond", "Reed", "Richard", "Robert",
        "Roger", "Ronald", "Ross", "Roy", "Russell", "Ryan", "Samuel", "Scott", "Sean",
        "Sebastian", "Shane", "Simon", "Spencer", "Stephen", "Steven", "Theodore", "Thomas",
        "Timothy", "Todd", "Travis", "Trevor", "Tyler", "Victor", "Vincent", "Wade", "Walter",
        "Warren", "Wayne", "Wesley", "William", "Zachary"
    ]

def get_female_middle_names():
    """Return list of popular female middle names"""
    return [
        "Abigail", "Ada", "Adelaide", "Alice", "Amanda", "Amy", "Andrea", "Angela", "Ann",
        "Anna", "Anne", "Ashley", "Aubrey", "Audrey", "Ava", "Barbara", "Beth", "Beverly",
        "Brenda", "Brianna", "Brooke", "Carol", "Caroline", "Catherine", "Charlotte", "Cheryl",
        "Chloe", "Christina", "Christine", "Claire", "Clara", "Claudia", "Crystal", "Cynthia",
        "Dana", "Dawn", "Deborah", "Denise", "Diana", "Diane", "Donna", "Doris", "Dorothy",
        "Eden", "Eleanor", "Elizabeth", "Ellen", "Emily", "Emma", "Erin", "Esther", "Eva",
        "Evelyn", "Faith", "Fiona", "Frances", "Gabrielle", "Gail", "Georgia", "Gloria",
        "Grace", "Hannah", "Harper", "Heather", "Helen", "Holly", "Hope", "Isabella", "Ivy",
        "Jackie", "Jane", "Janet", "Janice", "Jean", "Jenna", "Jennifer", "Jessica", "Jill",
        "Joan", "Joanne", "Jordan", "Josephine", "Joyce", "Judith", "Julia", "Julie", "June",
        "Karen", "Katherine", "Kathleen", "Katie", "Kayla", "Kelly", "Kimberly", "Laura",
        "Lauren", "Leah", "Leslie", "Lillian", "Linda", "Lisa", "Lori", "Louise", "Lucy",
        "Lynn", "Madison", "Margaret", "Maria", "Marie", "Marilyn", "Martha", "Mary", "Megan",
        "Melanie", "Michelle", "Miranda", "Monica", "Nancy", "Natalie", "Nicole", "Nina",
        "Nora", "Olivia", "Paige", "Pamela", "Patricia", "Paula", "Penelope", "Phyllis",
        "Rachel", "Rebecca", "Regina", "Robin", "Rose", "Ruby", "Ruth", "Samantha", "Sandra",
        "Sara", "Sarah", "Sharon", "Shirley", "Sophia", "Stephanie", "Susan", "Suzanne",
        "Taylor", "Teresa", "Theresa", "Tiffany", "Tracy", "Valerie", "Vanessa", "Victoria",
        "Violet", "Virginia", "Vivian", "Wendy", "Whitney"
    ]

def get_middle_names():
    """Return combined list of popular middle names (for backward compatibility)"""
    return get_male_middle_names() + get_female_middle_names()

def calculate_numerology_profile(full_name, birth_date):
    """Calculate complete numerology profile for a name"""
    life_path = calculate_life_path(birth_date)
    soul_urge = calculate_soul_urge(full_name)
    expression = calculate_expression(full_name)
    personality = calculate_personality(full_name)
    
    return {
        'life_path': life_path,
        'soul_urge': soul_urge,
        'expression': expression,
        'personality': personality
    }

def has_master_number(profile, target_numbers=[11, 22, 33]):
    """Check if profile contains any master numbers"""
    master_numbers = []
    for component, value in profile.items():
        if value in target_numbers:
            master_numbers.append((component, value))
    return master_numbers

def find_master_number_names(birth_date, gender, last_name, target_numbers=[11, 22, 33], 
                           target_components=None, max_results=10, fixed_first_name=None):
    """Find name combinations that result in master numbers"""
    
    if target_components is None:
        target_components = ['life_path', 'soul_urge', 'expression', 'personality']
    
    # Get appropriate name lists
    if gender.lower() in ['male', 'm', 'boy']:
        first_names = get_male_names()
        middle_names = get_male_middle_names()
    elif gender.lower() in ['female', 'f', 'girl']:
        first_names = get_female_names()
        middle_names = get_female_middle_names()
    else:
        # If gender not specified or other, use both lists
        first_names = get_male_names() + get_female_names()
        middle_names = get_middle_names()
    
    # If a fixed first name is provided, use only that
    if fixed_first_name:
        first_names = [fixed_first_name]
        print(f"Searching with fixed first name: {fixed_first_name}")
    
    results = []
    combinations_checked = 0
    
    print(f"Searching for names with master numbers {target_numbers} in components: {target_components}")
    print(f"Checking {len(first_names)} first names × {len(middle_names)} middle names = {len(first_names) * len(middle_names)} combinations...")
    print("This may take a moment...\n")
    
    for first_name in first_names:
        for middle_name in middle_names:
            if len(results) >= max_results:
                break
                
            combinations_checked += 1
            if combinations_checked % 1000 == 0:
                print(f"Checked {combinations_checked} combinations, found {len(results)} matches so far...")
            
            full_name = f"{first_name} {middle_name} {last_name}"
            profile = calculate_numerology_profile(full_name, birth_date)
            
            # Check if any of the target components have master numbers
            master_numbers_found = []
            for component in target_components:
                if component in profile and profile[component] in target_numbers:
                    master_numbers_found.append((component, profile[component]))
            
            if master_numbers_found:
                results.append({
                    'full_name': full_name,
                    'first_name': first_name,
                    'middle_name': middle_name,
                    'profile': profile,
                    'master_numbers': master_numbers_found
                })
        
        if len(results) >= max_results:
            break
    
    print(f"\nSearch complete! Checked {combinations_checked} combinations.")
    return results

def display_results(results):
    """Display the found name combinations in a formatted way"""
    if not results:
        print("No name combinations found with the specified master numbers.")
        return
    
    print(f"\n{'='*60}")
    print(f" FOUND {len(results)} NAME COMBINATIONS WITH MASTER NUMBERS")
    print(f"{'='*60}")
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['full_name']}")
        print(f"   Life Path: {result['profile']['life_path']}", end="")
        if result['profile']['life_path'] in [11, 22, 33]:
            print(" ✅")
        else:
            print()
            
        print(f"   Soul Urge: {result['profile']['soul_urge']}", end="")
        if result['profile']['soul_urge'] in [11, 22, 33]:
            print(" ✅")
        else:
            print()
            
        print(f"   Expression: {result['profile']['expression']}", end="")
        if result['profile']['expression'] in [11, 22, 33]:
            print(" ✅")
        else:
            print()
            
        print(f"   Personality: {result['profile']['personality']}", end="")
        if result['profile']['personality'] in [11, 22, 33]:
            print(" ✅")
        else:
            print()
        
def main():
    """Main function to run the master number name generator"""
    try:
        
        # Get user input
        birth_date = input("\033[1mEnter birth date (MM-DD-YYYY or MM/DD/YYYY):\033[0m ").strip()
        gender = input("Enter gender (M/F): ").strip()
        last_name = input("Enter last name: ").strip()
        first_name = input("Enter first name (optional): ").strip()
        
        if not birth_date or not last_name:
            print("Error: Birth date and last name are required.")
            return
        
        # Use None if first name is empty
        fixed_first_name = first_name if first_name else None
        
        # Optional filters
        print("\nOptional Filters (press Enter to use defaults):")
        
        target_input = input("Target master numbers (default: 11,22,33): ").strip()
        if target_input:
            try:
                target_numbers = [int(x.strip()) for x in target_input.split(',')]
                # Validate master numbers
                valid_masters = [11, 22, 33]
                target_numbers = [num for num in target_numbers if num in valid_masters]
                if not target_numbers:
                    target_numbers = [11, 22, 33]
            except ValueError:
                target_numbers = [11, 22, 33]
        else:
            target_numbers = [11, 22, 33]
        
        components_input = input("Target components (optional) [life_path, soul_urge, expression, personality]: ").strip()
        if components_input:
            valid_components = ['life_path', 'soul_urge', 'expression', 'personality']
            target_components = [comp.strip() for comp in components_input.split(',') 
                               if comp.strip() in valid_components]
            if not target_components:
                target_components = valid_components
        else:
            target_components = ['life_path', 'soul_urge', 'expression', 'personality']
        
        max_results_input = input("Maximum results to show: ").strip()
        if max_results_input:
            try:
                max_results = int(max_results_input)
                if max_results <= 0:
                    max_results = 10
            except ValueError:
                max_results = 10
        else:
            max_results = 10
        
        print(f"\nSearching for names with master numbers {target_numbers}")
        print(f"Target components: {target_components}")
        print(f"Maximum results: {max_results}")
        if fixed_first_name:
            print(f"Using fixed first name: {fixed_first_name}")
        print("-" * 60)
        
        # Find matching names
        results = find_master_number_names(
            birth_date, gender, last_name, 
            target_numbers, target_components, max_results, fixed_first_name
        )
        
        # Display results
        display_results(results)
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please try again with valid input.")
    except KeyboardInterrupt:
        print("\n\nSearch interrupted by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please try again.")

if __name__ == "__main__":
    main()
