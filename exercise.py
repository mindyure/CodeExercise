import re
import csv
import sys

# ASSUMPTIONS: 
#   Adults over 18 does not include those who are 18, but 19 and above.
#   Tacoma, FL is a real place.

def format_address(address, city, state):
    """Return readable, user-friendly version of full address"""
    address = re.sub(r'[,.]', '', address)
    
    def capitalize_word(word):
        if any(char.isdigit() for char in word):
            return word.lower()  # Keep words with digits lowercase (ex. "2nd")
        else:
            return word.capitalize()
    
    formatted_address = ' '.join(capitalize_word(word) for word in address.split())
    formatted_city = ' '.join(word.capitalize() for word in city.split())
    formatted_state = state.upper()

    return f"{formatted_address}, {formatted_city}, {formatted_state}"

def determine_households(address, city, state, households):
    """Update households dictionary with given address"""
    capitalized_address = ''.join([address, city, state]).upper()
    standardized_address = re.sub(r'[^A-Za-z0-9]', '', capitalized_address)
    
    if standardized_address in households:
        households[standardized_address]['occupant_number'] += 1
    else:
        households[standardized_address] = {
            'formatted_address': format_address(address, city, state),
            'occupant_number': 1
        }

def get_adults(rows):
    """Get adults over 18 with their formatted addresses"""
    adults = []

    for row in rows:
        first_name, last_name, address, city, state, age_str = row
        age = int(age_str)

        if age > 18:
            formatted_address = format_address(address, city, state)
            adults.append({
                'first_name': first_name,
                'last_name': last_name,
                'address': formatted_address,
                'age': age
            })

    return sorted(adults, key=lambda person: (person['last_name'], person['first_name']))

def print_households_and_adults(households, adults):
    """Print households and adult occupants in a formatted manner."""
    print("\nHouseholds and Occupants:")
    for household in households.values():
        print(f"{household['formatted_address']}: {household['occupant_number']}")

    print("\n" + "-" * 25)

    print("\nAdults Over 18:")
    for person in adults:
        print(f"{person['first_name']} {person['last_name']}")
        print(f"{person['address']}")
        print(f"Age: {person['age']}\n")

def main():
    households = {}

    input_file = sys.argv[1]

    with open(input_file, "r") as input_data:
        csv_reader = csv.reader(input_data)

        # Remove quotes/whitespace and convert row to list (list of lists)
        rows = [list(field.strip('"').strip() for field in row) for row in csv_reader]

    # Process households
    for row in rows:
        address, city, state = row[2], row[3], row[4]
        determine_households(address, city, state, households)

    # Print results
    print_households_and_adults(households, get_adults(rows))

if __name__ == "__main__":
    main()