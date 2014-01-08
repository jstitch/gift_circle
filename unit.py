#!/usr/bin/pyrg
# coding: utf-8

import unittest

from giftcircle import GiftCircle

class GiftCircleTests(unittest.TestCase):
    def test_load_data(self):
        gift_circle = GiftCircle("test_unit.txt")
        self.assertEqual(str(gift_circle),
"""Javier Novoa Cataño,jstitch@gmail.com
Javier Naranjamecanica,naranjamecanica00@hotmail.com
""")

        gift_circle = GiftCircle("test_unit_2.txt")
        self.assertEqual(str(gift_circle),
"""Novoa,jstitch@gmail.com
Naranjamecanica,naranjamecanica00@hotmail.com
""")

        self.assertListEqual(gift_circle.data,
                             ["Novoa,jstitch@gmail.com",
                              "Naranjamecanica,naranjamecanica00@hotmail.com"])


if __name__ == '__main__':
    tl = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromTestCase(GiftCircleTests)
    testcases = tl.getTestCaseNames(GiftCircleTests)
    print("Testcases:")
    for t in testcases:
        print(" ", t)
    print("")

    unittest.TextTestRunner(verbosity=2).run(suite)
