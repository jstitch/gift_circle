#!/usr/bin/python
# coding: utf-8

import unittest, mock
import random

from giftcircle import GiftCircle
from senders import Sender, Email, SMS, config

class GiftCircleTests(unittest.TestCase):
    def setUp(self):
        f = open("test_unit.txt","w")
        f.write("""Nombre1,correo1@example.com
Nombre2,correo2@example.com
""")
        f.close()
        f = open("test_unit_2.txt","w")
        f.write("""Nombre1,correo1@example.com
Nombre2,correo2@example.com
""")
        f.close()
        f = open("test_unit_3.txt","w")
        f.write("""Nombre1,correo1@example.com
Nombre2,correo2@example.com
Nombre3,correo3@example.com,correo4@example.com
""")
        f.close()
        f = open("test_unit_5.txt","w")
        f.write("""Nombre1,malcontacto""")
        f.close()

    def test_load_data(self):
        gift_circle = GiftCircle("test_unit.txt")
        self.assertEqual(str(gift_circle),
"""Nombre1,correo1@example.com
Nombre2,correo2@example.com
""")

        gift_circle = GiftCircle("test_unit_2.txt")
        self.assertEqual(str(gift_circle),
"""Nombre1,correo1@example.com
Nombre2,correo2@example.com
""")

        self.assertListEqual(gift_circle.data,
                             ["Nombre1,correo1@example.com",
                              "Nombre2,correo2@example.com"])

    def test_parse_data(self):
        gift_circle = GiftCircle("test_unit.txt")
        parsed = gift_circle.parse_data()
        self.assertListEqual(parsed, [{'name'    : "Nombre1",
                                       'contacts': [{'addr':"correo1@example.com",'type':Email}],
                                      },
                                      {'name'    : "Nombre2",
                                       'contacts': [{'addr':"correo2@example.com",'type':Email}],
                                      },
                                     ])
        self.assertListEqual(parsed, gift_circle.parsed)

        gift_circle = GiftCircle("test_unit_2.txt")
        parsed = gift_circle.parse_data()
        self.assertListEqual(parsed, [{'name'    : "Nombre1",
                                       'contacts': [{'addr':"correo1@example.com",'type':Email}],
                                      },
                                      {'name'    : "Nombre2",
                                       'contacts': [{'addr':"correo2@example.com",'type':Email}],
                                      },
                                     ])
        self.assertListEqual(parsed, gift_circle.parsed)

        gift_circle = GiftCircle("test_unit_3.txt")
        parsed = gift_circle.parse_data()
        self.assertListEqual(parsed, [{'name'    : "Nombre1",
                                       'contacts': [{'addr':"correo1@example.com",'type':Email}],
                                      },
                                      {'name'    : "Nombre2",
                                       'contacts': [{'addr':"correo2@example.com",'type':Email}],
                                      },
                                      {'name'    : "Nombre3",
                                       'contacts': [{'addr':"correo3@example.com",'type':Email},
                                                    {'addr':"correo4@example.com",'type':Email}],
                                      },
                                     ])
        self.assertListEqual(parsed, gift_circle.parsed)

        gift_circle = GiftCircle("test_unit_5.txt")
        with self.assertRaisesRegex(Exception, "'GiftCircle' bad contact") as ex:
            gift_circle.parse_data()

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
        with self.assertRaisesRegex(AttributeError, "'GiftCircle' object has no attribute 'parsed'") as ex:
            shuffled = gift_circle.shuffle_data()

    @mock.patch('giftcircle.senders.Email.smtplib.SMTP')
    def test_send_circle(self, mock_smtplib):
        gift_circle = GiftCircle("test_unit_3.txt")
        gift_circle.parse_data()
        gift_circle.shuffle_data()
        smtpserver = mock_smtplib.return_value
        smtpserver.sendmail.return_value={}
        gift_circle.send_circle()
        self.assertTrue(smtpserver.sendmail.called)

    def test_cannotsend_without_shuffle(self):
        gift_circle = GiftCircle("test_unit_3.txt")
        gift_circle.parse_data()
        with self.assertRaisesRegex(AttributeError, "'GiftCircle' object has no attribute 'shuffled'") as ex:
            gift_circle.send_circle("This is a test message")


class SendersTests(unittest.TestCase):
    def test_sender(self):
        sender = Sender(desde=('DesdeAddr','DesdeNombre'),
                        a=('AAddr','ANombre'),
                        msg="Mensaje")
        self.assertEqual(sender.desde['addr'], "DesdeAddr")
        self.assertEqual(sender.desde['nombre'], "DesdeNombre")
        self.assertEqual(sender.a['addr'], "AAddr")
        self.assertEqual(sender.a['nombre'], "ANombre")
        self.assertEqual(sender.msg, "Mensaje")
        self.assertIsNone(sender.send())

    @mock.patch('senders.Email.smtplib.SMTP')
    def test_email(self, mock_smtplib):
        sender = Email(a=('jstitch@jonsnow', 'Javier Novoa C.'),
                       subject="Asunto",
                       msg="Este es un mensaje de Prueba\nPROBANDO PROBANDO 1,2,3")
        self.assertEqual(sender.subject, "Asunto")
        self.assertEqual(sender.desde['addr'],config.Email['FromAddr'])
        self.assertEqual(sender.desde['nombre'],config.Email['FromName'])
        self.assertEqual(sender.server,'localhost')
        self.assertEqual(sender.port,25)

        smtpserver = mock_smtplib.return_value
        smtpserver.sendmail.return_value={}
        sender.send()
        self.assertTrue(smtpserver.sendmail.called)
        smtpserver.sendmail.assert_called_once_with(sender.desde['addr'], [sender.a['addr']], sender.msg.as_string())

        smtpserver.side_effect=Exception("Error sending email to %s (%s)" % ("jstitch@jonsnow", ""))
        with self.assertRaisesRegex(Exception, "Error sending email to %s ([\w]*)" % ("jstitch@jonsnow",)) as ex:
            sender.send()

    @mock.patch('senders.SMS.twilio.rest.TwilioRestClient')
    def test_twilio(self, mock_twilio):
        sender = SMS(a=('5512345678','Javier Novoa C.'),
                     msg="Este es un mensaje de prueba. PROBANDO PROBANDO 1,2,3")
        self.assertEqual(sender.intlcode,"+52")
        self.assertEqual(sender.desde['addr'],config.SMS['FromNumber'])
        self.assertEqual(sender.desde['nombre'],'FromName')

        import random
        class message(object):
            sid = "SM"+"".join(random.choice("abcdef0123456789") for i in range(32))
        twilio = mock_twilio.return_value
        twilio.sms.messages.create.return_value=message()
        sender.send()
        self.assertTrue(twilio.sms.messages.create.called)
        twilio.sms.messages.create.assert_called_once_with(body=sender.msg, to=sender.intlcode+sender.a['addr'], from_=sender.desde['addr'])
        self.assertEqual(str(type(sender.message.sid)),"<class 'str'>")
        self.assertRegex(sender.message.sid, r"^SM[\w]{32}$")

        twilio.sms.messages.create.side_effect=SMS.TwilioRestException("404","Not Found")
        with self.assertRaisesRegex(Exception, "Error sending SMS to %s" % (sender.a['nombre'],)) as ex:
            sender.send()


class SMSTests(unittest.TestCase):
    def setUp(self):
        f = open("test_unit_4.txt","w")
        f.write("""Nombre1,correo1@example.com
Nombre2,5512345678
Nombre3,correo3@example.com,5587654321
""")
        f.close()
        f = open("test_unit_5.txt","w")
        f.write("""Nombre1,malcontacto""")
        f.close()
        f = open("test_unit_6.txt","w")
        f.write("""Nombre1,5512345678
Nombre2,5587654321
""")
        f.close()

    def test_setEmail(self):
        gf = GiftCircle('test_unit_4.txt')
        pd = gf.parse_data()
        self.assertEqual(pd[0]['contacts'][0]['type'], Email)

    def test_setSMS(self):
        gf = GiftCircle('test_unit_4.txt')
        pd = gf.parse_data()
        self.assertEqual(pd[1]['contacts'][0]['type'], SMS)

    def test_setEmailAndSMS(self):
        gf = GiftCircle('test_unit_4.txt')
        pd = gf.parse_data()
        self.assertEqual(pd[2]['contacts'][0]['type'], Email)
        self.assertEqual(pd[2]['contacts'][1]['type'], SMS)

    def test_malContacto(self):
        gf = GiftCircle('test_unit_5.txt')
        with self.assertRaisesRegex(Exception, "'GiftCircle' bad contact") as ex:
            pd = gf.parse_data()

    @mock.patch('senders.SMS.twilio.rest.TwilioRestClient')
    def test_send_circle(self, mock_twilio):
        gift_circle = GiftCircle("test_unit_6.txt")
        gift_circle.parse_data()
        gift_circle.shuffle_data()

        import random
        class message(object):
            sid = "SM"+"".join(random.choice("abcdef0123456789") for i in range(32))
        twilio = mock_twilio.return_value
        twilio.sms.messages.create.return_value=message()
        gift_circle.send_circle()
        self.assertTrue(twilio.sms.messages.create.called)


if __name__ == '__main__':
    test_classes_to_run = [
                           GiftCircleTests,
                           SendersTests,
                           SMSTests,
                          ]
    tl = unittest.TestLoader()
    suites_list = []
    for test_class in test_classes_to_run:
        print("%s testcases:" % test_class.__name__)
        suite = tl.loadTestsFromTestCase(test_class)
        testcases = tl.getTestCaseNames(test_class)
        for t in testcases:
            print(t)
        print("")
        suites_list.append(suite)
    big_suite = unittest.TestSuite(suites_list)
    runner = unittest.TextTestRunner(verbosity=2)
    results = runner.run(big_suite)
