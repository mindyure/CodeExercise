import re
import csv
import sys

# ASSUMPTIONS: 
#   Adults over 18 does not include those who are 18, but 19 and above.
#   Tacoma, FL is a real place.

def format_address(raw_address):
    """Returns formatted address for readability and normalization"""
    address, city, state = raw_address
    address = re.sub(r'[^A-Za-z0-9]', ' ', address)
    
    def capitalize_word(word):
        """Capitalize only beginning of word (ex. avoids instances like 2Nd)"""
        return word[0].upper() + word[1:]
    
    formatted_address = ' '.join(capitalize_word(word) for word in address.split())
    formatted_city = ' '.join(capitalize_word(word) for word in city.split())
    formatted_state = state.upper()
    
    return ', '.join([formatted_address, formatted_city, formatted_state])


def print_household_counts(households):
    """Print each household address and occupancy number"""
    print("Households and Occupants:")
    for household in households:
        occupants = households[household]
        print(f"{household}: {len(occupants)}")


def print_adults(adults):
    """Sort and print adults over 18 by last name, then first name"""
    sorted_adults = sorted(adults, key=lambda x: (x[0][1], x[0][0]))

    print("Adults Over 18:")
    for person, address in sorted_adults:
        first_name, last_name, age = person
        print(f"{first_name} {last_name}")
        print(f"{address}")
        print(f"Age: {age}\n")


def main():
    households = {}
    adults = []
    input_file = sys.argv[1]

    # Read and clean input file
    with open(input_file, "r") as input_data:
        csv_reader = csv.reader(input_data)
        rows = [list(field.strip('"').strip() for field in row) for row in csv_reader]

    # Process each line in input file
    for row in rows:
        raw_address = (row[2], row[3], row[4])
        age = int(row[5])
        person = (row[0], row[1], age)
        
        # Populate household dictionary
        address = format_address(raw_address)
        if address not in households:
            households[address] = [] # Init. occupants list for new address
        households[address].append(person)
        
        # Populate adults list
        if age > 18:
            adults.append((person, address))

    print_household_counts(households)
    print("\n" + "-" * 25 + "\n")
    print_adults(adults)


if __name__ == "__main__":
    main()