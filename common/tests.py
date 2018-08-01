from django.test import TestCase
from common.language import join_and


class LanguageTestCase(TestCase):
    def setUp(self):
        self.fruits_singular = ["apple", "orange", "banana"]
        self.fruits_plural = ["apples", "oranges", "bananas"]

    def test_join_and(self):
        """
        Test join_and, normal and edge cases.
        The join_and function is expected to join string iterables into
        an English "coordinating conjunction" phrase.
        """
        self.assertEqual(join_and(self.fruits_singular, plural=False),
                         "apple, a orange and a banana")
        self.assertEqual(join_and(self.fruits_plural, plural=True),
                         "apples, oranges and bananas")
        self.assertEqual(join_and(["apple"], plural=False),
                         "apple")
        self.assertEqual(join_and(["apples"], plural=True),
                         "apples")
        self.assertEqual(join_and([], plural=True),
                         "")
        self.assertEqual(join_and([], plural=False),
                         "")
