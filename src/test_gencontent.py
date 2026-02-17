import unittest
from gencontent import extract_title

# Let's imagine we are testing:
# def extract_username(text):
#     if not text.startswith("@"):
#         raise ValueError("not a username")
#     return text[1:]

class TestUsernameExtractor(unittest.TestCase):
    def test_extract(self):
        # Testing a normal case
        actual = extract_title("# boots")
        expected = "boots"
        self.assertEqual(actual, expected)

    def test_no_at_symbol(self):
        # Testing that an Exception (or ValueError) is raised
        with self.assertRaises(Exception):
            extract_title("boots")

    def test_no_working(self):
        actual = extract_title(
            """# Tolkien Fan Club
            ![JRR Tolkien sitting](/images/tolkien.png)
            Here('s the deal, **I like Tolkien**.'
            """)
        expected = "Tolkien Fan Club"
        self.assertEqual(actual, expected)