# coding: utf-8

import config

class Sender(object):

    def __init__(self, desde, a, msg):
        self.desde = {}
        self.a = {}
        self.desde['addr'] = desde[0]
        self.desde['nombre'] = desde[1]
        self.a['addr'] = a[0]
        self.a['nombre'] = a[1]
        self.msg = msg

    def send(self):
        pass

class Email(Sender):

    import smtplib

    def __init__(self, a, subject, msg, server='localhost', port=25):
        self.subject = subject
        self.server = server
        self.port = port
        Sender.__init__(self, desde=(config.Email['FromAddr'],config.Email['FromName']), a=a, msg=msg)

    def send(self):
        from email.mime.text import MIMEText
        try:
            self.msg = MIMEText(self.msg)
            self.msg['Subject'] = self.subject
            self.msg['From'] = self.desde['addr']
            self.msg['To'] = self.a['addr']
            s = self.smtplib.SMTP(host=self.server,port=self.port)
            s.sendmail(self.msg['From'], [self.a['addr']], self.msg.as_string())
            s.quit()
        except Exception as ex:
            raise Exception("Error sending email to %s (%s)" % (self.a['addr'], repr(ex)))

class SMS(Sender):
    import twilio.rest
    from twilio import TwilioRestException

    def __init__(self, a, msg, intlcode="+52"):
        self.intlcode=intlcode
        Sender.__init__(self, desde=(config.SMS['FromNumber'],"FromName"), a=a, msg=msg)

    def send(self):
        account_sid=config.SMS['AccountSID']
        auth_token=config.SMS['AuthToken']
        client = self.twilio.rest.TwilioRestClient(account_sid, auth_token)
        try:
            self.message = client.sms.messages.create(body=self.msg, to=self.intlcode+self.a['addr'], from_=self.desde['addr'])
        except self.TwilioRestException as trex:
            raise Exception("Error sending SMS to %s\n(%s)" % (self.a['nombre'], str(trex)))
