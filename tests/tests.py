import unittest

from src.main import compare_word_with_key


class TestWordPatterns(unittest.TestCase):

	def test_pattern_generation(self):
		self.assertEqual(list(compare_word_with_key('xxxde', 'speed')), [0, 0, 1, 0, 1])
		self.assertEqual(list(compare_word_with_key('exxse', 'speed')), [1, 0, 1, 1, 0])
		self.assertEqual(list(compare_word_with_key('sxexx', 'speed')), [2, 0, 2, 0, 0])
		self.assertEqual(list(compare_word_with_key('xxepe', 'speed')), [0, 1, 2, 1, 0])
		self.assertEqual(list(compare_word_with_key('xexex', 'speed')), [0, 0, 1, 2, 0])
		self.assertEqual(list(compare_word_with_key('sxeax', 'space')), [2, 0, 1, 0, 1])

