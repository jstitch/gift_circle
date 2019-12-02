#!/usr/bin/pyrg
# coding: utf-8

import unittest

import gift_circle

class GiftCircle(unittest.TestCase):
    @classmethod
    def setupClass(self):
        f = open("test_unit.txt","w")
        f.write("""Javier Novoa Cataño,jstitch@gmail.com,5515905010
Lorenita,5536538102,lorena806@gmail.com
Javier Naranjamecanica,naranjamecanica00@hotmail.com""")
        f.close()
        f = open("test_unit_2.txt","w")
        f.write("""Javier Novoa Cataño,Oso de peluche,jstitch@gmail.com,5515905010
Lorenita,Bebe;DVD,5536538102,lorena806@gmail.com
Javier Naranjamecanica,Mouse;Servidor;Pantalla,naranjamecanica00@hotmail.com""")
        f.close()

    def test_01_load(self):
        data = gift_circle.load_data("test_unit.txt")
        self.assertListEqual(["Javier Novoa Cataño,jstitch@gmail.com,5515905010",
			                  "Lorenita,5536538102,lorena806@gmail.com",
			                  "Javier Naranjamecanica,naranjamecanica00@hotmail.com"],
			data)
        data = gift_circle.load_data("test_unit_2.txt")
        self.assertListEqual(["Javier Novoa Cataño,Oso de peluche,jstitch@gmail.com,5515905010",
			                  "Lorenita,Bebe;DVD,5536538102,lorena806@gmail.com",
			                  "Javier Naranjamecanica,Mouse;Servidor;Pantalla,naranjamecanica00@hotmail.com"],
            data)

    def test_02_parse(self):
        data = gift_circle.load_data("test_unit.txt")
        parsed_data = gift_circle.parse_data(data)
        self.assertListEqual([{'name':"Javier Novoa Cataño",'gifts':[],'contact':[{'dest':"jstitch@gmail.com",'type':"Email"},
			                                                                      {'dest':"5515905010",'type':"SMS"}]},
                              {'name':"Lorenita",'gifts':[],'contact':[{'dest':"5536538102",'type':"SMS"},
			                                                           {'dest':"lorena806@gmail.com",'type':"Email"}]},
                              {'name':"Javier Naranjamecanica",'gifts':[],'contact':[{'dest':"naranjamecanica00@hotmail.com",'type':"Email"}]},
			                 ],
			parsed_data)
        data = gift_circle.load_data("test_unit_2.txt")
        parsed_data = gift_circle.parse_data(data)
        self.assertListEqual([{'name':"Javier Novoa Cataño",'gifts':["Oso de peluche"],'contact':[{'dest':"jstitch@gmail.com",'type':"Email"},
			                                                                                      {'dest':"5515905010",'type':"SMS"}]},
                              {'name':"Lorenita",'gifts':["Bebe","DVD"],'contact':[{'dest':"5536538102",'type':"SMS"},
			                                                                       {'dest':"lorena806@gmail.com",'type':"Email"}]},
                              {'name':"Javier Naranjamecanica",'gifts':["Mouse","Servidor","Pantalla"],'contact':[{'dest':"naranjamecanica00@hotmail.com",'type':"Email"}]},
			                 ],
			parsed_data)

    def test_03_validate(self):
        data = [{'name':"Javier Novoa Cataño",'contact':[{'dest':"naranjamecanica00@hotmail.com",'type':"Email"},
			                                                           {'dest':"5515905010",'type':"SMS"}]},
                              {'name':"Lorenita",'contact':[{'dest':"5536538102",'type':"SMS"},
			                                                {'dest':"lorena806@gmail.com",'type':"Email"}]},
                              {'name':"Javier Naranjamecanica",'contact':[{'dest':"naranjamecanica00@hotmail.com",'type':"Email"}]},
			                 ]
        self.assertEqual(False, gift_circle.shuffle_data(data, validate=True))
        data2 = [{'name':"Javier Novoa Cataño",'gifts':["Oso de peluche"],'contact':[{'dest':"naranjamecanica00@hotmail.com",'type':"Email"},
                                                                                     {'dest':"5515905010",'type':"SMS"}]},
                 {'name':"Lorenita",'gifts':["Bebe","DVD"],'contact':[{'dest':"5536538102",'type':"SMS"},
                                                                      {'dest':"lorena806@gmail.com",'type':"Email"}]},
                 {'name':"Javier Naranjamecanica",'gifts':["Mouse","Servidor","Pantalla"],'contact':[{'dest':"naranjamecanica00@hotmail.com",'type':"Email"}]},
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
