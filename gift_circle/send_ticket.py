# coding: utf-8

try:
    from . import config
except ImportError:
    import config

class Sender(object):
    def __init__(self,fromaddr,fromname,toaddr,toname,message):
        self.fromaddr = fromaddr
        self.fromname = fromname
        self.toaddr = toaddr
        self.toname = toname
        self.message = message

    def send(self):
        pass

class Email(Sender):
    def send(self):
        import smtplib
        from email.mime.text import MIMEText
        try:
            msg = MIMEText(self.message)
            msg['Subject'] = "Gift Circle"
            msg['From'] = config.email['email_from_addr']
            msg['To'] = self.toaddr
            s = smtplib.SMTP(config.email['email_server'])
            s.sendmail(config.email['email_from_addr'], [self.toaddr], msg.as_string())
            s.quit()
        except smtplib.SMTPException:
            raise Exception("Error sending email to %s" % (self.toaddr))

class SMS(Sender):
    def send(self):
        from twilio.base.exceptions import TwilioRestException
        from twilio.rest import Client
        account_sid=config.twilio["account_sid"]
        auth_token=config.twilio["auth_token"]
        from_number=config.twilio["from_number"]
        code=config.twilio["code"]
        client = Client(account_sid, auth_token)
        try:
            message = client.messages.create(body=self.message, to=code+self.toaddr, from_=from_number)
            print(message.sid)
        except TwilioRestException as trex:
            raise Exception("Error sending SMS to %s (%s)" % (self.toname, repr(trex)))
