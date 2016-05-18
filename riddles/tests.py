from django.test import TestCase

from riddles import util


class TestIsSquare(TestCase):
    # Square numbers
    def test_0_is_square(self):
        self.assertTrue(util.is_square(0))

    def test_1_is_square(self):
        self.assertTrue(util.is_square(1))

    def test_4_is_square(self):
        self.assertTrue(util.is_square(4))

    def test_9_is_square(self):
        self.assertTrue(util.is_square(9))

    def test_81_is_square(self):
        self.assertTrue(util.is_square(81))

    # Non square numbers
    def test_2_is_not_square(self):
        self.assertFalse(util.is_square(2))

    def test_500_is_not_square(self):
        self.assertFalse(util.is_square(500))

    # Negative numbers
    def test_neg0_is_square(self):
        self.assertTrue(util.is_square(-0))

    def test_neg1_is_not_square(self):
        self.assertFalse(util.is_square(-1))

    def test_neg2_is_not_square(self):
        self.assertFalse(util.is_square(-2))

    def test_neg81_is_not_square(self):
        self.assertFalse(util.is_square(-81))

    def test_neg500_is_not_square(self):
        self.assertFalse(util.is_square(-500))
