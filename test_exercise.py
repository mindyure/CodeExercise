import unittest

from exercise import (
    format_address,
    determine_households,
    get_adults
)


class TestAddressFunctions(unittest.TestCase):
    
    def test_format_address(self):
        # Test capitalization and state uppercasing
        self.assertEqual(
            format_address("123 main st.", "seattle", "wa"),
            "123 Main St, Seattle, WA"
        )

        # Test if words with digits are lowercase
        self.assertEqual(
            format_address("2ND ave", "new york", "ny"),
            "2nd Ave, New York, NY"
        )
        
        # Test removal of punctuation
        self.assertEqual(
            format_address("1st. ave.", "los angeles", "ca"),
            "1st Ave, Los Angeles, CA"
        )

    def test_determine_households(self):
        # Test adding a new household to dictionary
        households = {}
        determine_households("123 main st", "seattle", "wa", households)
        self.assertIn("123MAINSTSEATTLEWA", households)
        self.assertEqual(households["123MAINSTSEATTLEWA"]['occupant_number'], 1)
        self.assertEqual(
            households["123MAINSTSEATTLEWA"]['formatted_address'],
            "123 Main St, Seattle, WA"
        )

        # Test incrementing occupant number if the address already exists
        determine_households("123 main st", "seattle", "wa", households)
        self.assertEqual(households["123MAINSTSEATTLEWA"]['occupant_number'], 2)

    def test_get_adults(self):
        rows = [
            ["John", "Doe", "123 Main St", "Seattle", "WA", "25"],
            ["Jane", "Doe", "123 Main St", "Seattle", "WA", "18"],
            ["Alice", "Smith", "1st Ave", "Los Angeles", "CA", "19"]
        ]

        # Test that only adults over 18 are returned, in sorted order
        adults = get_adults(rows)
        self.assertEqual(len(adults), 2)
        self.assertEqual(adults[0]['first_name'], "John")
        self.assertEqual(adults[1]['first_name'], "Alice")

        # Test the formatted address in the result
        self.assertEqual(adults[0]['address'], "123 Main St, Seattle, WA")
        self.assertEqual(adults[1]['address'], "1st Ave, Los Angeles, CA")


if __name__ == "__main__":
    unittest.main()
