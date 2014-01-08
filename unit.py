#!/usr/bin/pyrg
# coding: utf-8

import unittest

from giftcircle import GiftCircle

class GiftCircleTests(unittest.TestCase):
    def test_load_data(self):
        gift_circle = GiftCircle("test_unit.txt")
        print(gift_circle)


if __name__ == '__main__':
    tl = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromTestCase(GiftCircleTests)
    testcases = tl.getTestCaseNames(GiftCircleTests)
    print("Testcases:")
    for t in testcases:
        print(" ", t)
    print("")

    unittest.TextTestRunner(verbosity=2).run(suite)
