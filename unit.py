#!/usr/bin/pyrg
# coding: utf-8

import unittest

import gift_circle

class GiftCircle(unittest.TestCase):
    @classmethod
    def setupClass(self):
        f = open("test_unit.txt","w")
        f.write("""Persona1,correo@example.com,0987654321
Persona2,1234567890,estecorreo@example.com
Persona3,uncorreo@example.com""")
        f.close()
        f = open("test_unit_2.txt","w")
        f.write("""Persona1,Oso de peluche,correo@example.com,0987654321
Persona2,Bebe;DVD,1234567890,estecorreo@example.com
Persona3,Mouse;Servidor;Pantalla,uncorreo@example.com""")
        f.close()

    def test_01_load(self):
        data = gift_circle.load_data("test_unit.txt")
        self.assertListEqual(["Persona1,correo@example.com,0987654321",
			                  "Persona2,1234567890,estecorreo@example.com",
			                  "Persona3,uncorreo@example.com"],
			data)
        data = gift_circle.load_data("test_unit_2.txt")
        self.assertListEqual(["Persona1,Oso de peluche,correo@example.com,0987654321",
			                  "Persona2,Bebe;DVD,1234567890,estecorreo@example.com",
			                  "Persona3,Mouse;Servidor;Pantalla,uncorreo@example.com"],
            data)

    def test_02_parse(self):
        data = gift_circle.load_data("test_unit.txt")
        parsed_data = gift_circle.parse_data(data)
        self.assertListEqual([{'name':"Persona1",'gifts':[],'contact':[{'dest':"correo@example.com",'type':"Email"},
			                                                                      {'dest':"0987654321",'type':"SMS"}]},
                              {'name':"Persona2",'gifts':[],'contact':[{'dest':"1234567890",'type':"SMS"},
			                                                           {'dest':"estecorreo@example.com",'type':"Email"}]},
                              {'name':"Persona3",'gifts':[],'contact':[{'dest':"uncorreo@example.com",'type':"Email"}]},
			                 ],
			parsed_data)
        data = gift_circle.load_data("test_unit_2.txt")
        parsed_data = gift_circle.parse_data(data)
        self.assertListEqual([{'name':"Persona1",'gifts':["Oso de peluche"],'contact':[{'dest':"correo@example.com",'type':"Email"},
			                                                                                      {'dest':"0987654321",'type':"SMS"}]},
                              {'name':"Persona2",'gifts':["Bebe","DVD"],'contact':[{'dest':"1234567890",'type':"SMS"},
			                                                                       {'dest':"estecorreo@example.com",'type':"Email"}]},
                              {'name':"Persona3",'gifts':["Mouse","Servidor","Pantalla"],'contact':[{'dest':"uncorreo@example.com",'type':"Email"}]},
			                 ],
			parsed_data)

    def test_03_validate(self):
        data = [{'name':"Persona1",'contact':[{'dest':"uncorreo@example.com",'type':"Email"},
			                                                           {'dest':"0987654321",'type':"SMS"}]},
                              {'name':"Persona2",'contact':[{'dest':"1234567890",'type':"SMS"},
			                                                {'dest':"estecorreo@example.com",'type':"Email"}]},
                              {'name':"Persona3",'contact':[{'dest':"uncorreo@example.com",'type':"Email"}]},
			                 ]
        self.assertEqual(False, gift_circle.shuffle_data(data, validate=True))
        data2 = [{'name':"Persona1",'gifts':["Oso de peluche"],'contact':[{'dest':"uncorreo@example.com",'type':"Email"},
                                                                                     {'dest':"0987654321",'type':"SMS"}]},
                 {'name':"Persona2",'gifts':["Bebe","DVD"],'contact':[{'dest':"1234567890",'type':"SMS"},
                                                                      {'dest':"estecorreo@example.com",'type':"Email"}]},
                 {'name':"Persona3",'gifts':["Mouse","Servidor","Pantalla"],'contact':[{'dest':"uncorreo@example.com",'type':"Email"}]},
			    ]
        self.assertEqual(False, gift_circle.shuffle_data(data2, validate=True))

if __name__ == '__main__':
    tl = unittest.TestLoader()
    suite = unittest.TestLoader().loadTestsFromTestCase(GiftCircle)
    testcases = tl.getTestCaseNames(GiftCircle)
    print("Testcases:")
    for t in testcases:
        print(" ", t)
    print("")

    unittest.TextTestRunner(verbosity=2).run(suite)
