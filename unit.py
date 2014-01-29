#!/usr/bin/python
# coding: utf-8

import unittest
import random

from giftcircle import GiftCircle

class GiftCircleTests(unittest.TestCase):
    def setUp(self):
        f = open("test_unit.txt","w") 
        f.write("""Javier Novoa Cataño,jstitch@gmail.com
Javier Naranjamecanica,naranjamecanica00@hotmail.com
""")
        f.close()
        f = open("test_unit_2.txt","w")
        f.write("""Novoa,jstitch@gmail.com
Naranjamecanica,naranjamecanica00@hotmail.com
""")
        f.close()
        f = open("test_unit_3.txt","w")
        f.write("""Javier Novoa Cataño,javisfelagund@yahoo.com.mx
Naranjamecanica,naranjamecanica00@hotmail.com
Novoa,jstitch@gmail.com
""")
        f.close()
    
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

    def test_parse_data(self):
        gift_circle = GiftCircle("test_unit.txt")
        parsed = gift_circle.parse_data()

        self.assertListEqual(parsed, [{'name'    : "Javier Novoa Cataño",
                                       'contact' : "jstitch@gmail.com"},
                                      {'name'    : "Javier Naranjamecanica",
                                       'contact' : "naranjamecanica00@hotmail.com"},
                                     ])
        self.assertListEqual(parsed, gift_circle.parsed)

        gift_circle = GiftCircle("test_unit_2.txt")
        parsed = gift_circle.parse_data()

        self.assertListEqual(parsed, [{'name'    : "Novoa",
                                       'contact' : "jstitch@gmail.com"},
                                      {'name'    : "Naranjamecanica",
                                       'contact' : "naranjamecanica00@hotmail.com"},
                                     ])
        self.assertListEqual(parsed, gift_circle.parsed)

    def test_shuffle_data(self):
        gift_circle = GiftCircle("test_unit_3.txt")
        parsed = gift_circle.parse_data()
        shuffled = gift_circle.shuffle_data()
        names_shuffled = [ s['name'] for s in shuffled ]
        names_shuffled.sort()
        self.assertEqual(names_shuffled, [ p['name'] for p in parsed ])
        elem = random.choice(names_shuffled)
        self.assertTrue(elem in names_shuffled)
        with self.assertRaises(ValueError):
            random.sample(names_shuffled, 4)
        for elem in random.sample(names_shuffled, 3):
            self.assertTrue(elem in names_shuffled)

    def test_cannotshuffle_without_parse(self):
        gift_circle = GiftCircle("test_unit_3.txt")
        with self.assertRaisesRegexp(AttributeError, "'GiftCircle' object has no attribute 'parsed'") as ex:
            shuffled = gift_circle.shuffle_data()


if __name__ == '__main__':
    test_classes_to_run = [
                           GiftCircleTests,
                          ]
    tl = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        print("%s testcases:" % test_class.__name__)
        suite = tl.loadTestsFromTestCase(test_class)
        testcases = tl.getTestCaseNames(test_class)
        for t in testcases:
            print(" ", t)
        print("")
        suites_list.append(suite)
    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner(verbosity=2)
    results = runner.run(big_suite)
