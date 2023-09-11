import unittest
from Infraestructure.RandomNumber import RandomNumber


class TestRandom(unittest.TestCase):

    def setUp(self):
        self.random = RandomNumber()

    def test_generate_random_number(self):
        for i in range(100):
            print(self.random.random_number_generator(0, 10))


if __name__ == '__main__':
    unittest.main()
