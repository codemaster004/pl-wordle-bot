import unittest

from src.main import compare_word_with_key, does_word_fit


class TestWordPatterns(unittest.TestCase):

	def test_pattern_generation(self):
		self.assertEqual(list(compare_word_with_key('xxxde', 'speed')), [0, 0, 1, 0, 1])
		self.assertEqual(list(compare_word_with_key('exxse', 'speed')), [1, 0, 1, 1, 0])
		self.assertEqual(list(compare_word_with_key('sxexx', 'speed')), [2, 0, 2, 0, 0])
		self.assertEqual(list(compare_word_with_key('xxepe', 'speed')), [0, 1, 2, 1, 0])
		self.assertEqual(list(compare_word_with_key('xexex', 'speed')), [0, 0, 1, 2, 0])
		self.assertEqual(list(compare_word_with_key('sxeax', 'space')), [2, 0, 1, 0, 1])

	def test_single_word_pattern_apply(self):
		# Test for Green letters
		self.assertTrue(does_word_fit('xxxxE', (0, 0, 0, 0, 2), 'yyyyE'))
		self.assertFalse(does_word_fit('xxxxE', (2, 0, 0, 0, 0), 'Eyyyy'))

		# Test for Gray letters
		self.assertTrue(does_word_fit('xxxxx', (0, 0, 0, 0, 0), 'yyyyy'))
		self.assertFalse(does_word_fit('xxExx', (0, 0, 0, 0, 0), 'yyyEy'))

		# Test for Orange letters
		self.assertFalse(does_word_fit('xxExx', (0, 0, 1, 0, 0), 'yyEyy'))
		self.assertTrue(does_word_fit('xExxx', (0, 0, 1, 0, 0), 'yyEyy'))

		# Genera Test
		self.assertTrue(does_word_fit('abide', (0, 0, 1, 0, 1), 'speed'))
		self.assertTrue(does_word_fit('erase', (1, 0, 1, 1, 0), 'speed'))
		self.assertTrue(does_word_fit('steal', (2, 0, 2, 0, 0), 'speed'))
		self.assertTrue(does_word_fit('crepe', (0, 1, 2, 1, 0), 'speed'))
