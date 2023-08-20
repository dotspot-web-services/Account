

import os
import smtplib
from email.message import EmailMessage
from email import message_from_bytes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from imaplib import IMAP4_SSL

from .serializer import Contact
from setting.dbcon import DbSet as _DB
from .templates import SetMail


class SendMsg(SetMail):

    contact = None
    __host = "smtp.questarenz.com"
    __mail=None
    __mailpwd=None
    __port = 465 #587
    toname=None
    subject=None
    text=None
    attatchment=None

    def __init__(self, mail, mailpwd, contact, subject=None, toname=None, text=None, attatchment=None):
        super().__init__(contact, subject, toname, text, attatchment)
        _db = _DB()

        if mail or mailpwd is None:
            assert mail and mailpwd is None
            self.__mail = _db._oda.quest_mailer
            self.__mailpwd = _db._oda.quest_pass
            self.__host = "smtp"
        else:
            self.__mail = mail
            self.__mailpwd = mailpwd
        assert contact is not None
        self.contact = Contact(cont=contact)

    def format_msg(self):
        ""

    def send_mail(self, mail):

        if (emails := isinstance(mail, list)):
            email = ", ".join(emails)
        else:
            email = emails

        msg = EmailMessage()
        msg['From'] = self.__quest
        msg['To'] = email
        if self.subjt and self.text is None:
            subjet, txt = self.format_msg()
        msg['Subject'] = subjet
        msg.set_content = txt

        if self.attatchd:
            data, subtyp, file_name = self.file()
            msg.add_attachment(data, subtype=subtyp, filename=file_name)
        msg.add_alternative("""the html""", subtyp="html")
        with smtplib.SMTP_SSL(self.__host, self.__port) as server:
            server.login(self.__mail, self.__mailpwd)
            server.send_message(msg)  

    def send_sms(self, phone):
        server = smtplib.SMTP(self.__host, self.__port)
        # Starting the server
        server.starttls()
        # Now we need to login
        server.login(self.__mail, self.__mailpwd)

        def sender(sms_gateway):
            try:
                msg.attach(MIMEText(body, 'plain'))
                sms = msg.as_string()
                server.sendmail(self.__quest,sms_gateway,sms)
            except ValueError:
                raise"Phone number is needed"
            # lastly quit the server
        code = os.urandom(5)
        # The server we use to send emails in our case it will be gmail but every email provider has a different smtp 
        # and port is also provided by the email provider.

        # This will start our email server
        

        # Now we use the MIME module to structure our message.
        msg = MIMEMultipart()
        msg['From'] = self.__mail

        if not isinstance(phone, set):
            sms_gateway=f"{phone}@{self.__mail}"
            msg['To'] = sms_gateway
            sender(sms_gateway=sms_gateway)
        elif phone:
            for gateway in phone:
                sms_gateway=f"{gateway}@tmomail.net"
                msg['To'] = sms_gateway
                sender(sms_gateway=sms_gateway)
        
        # Make sure you add a new line in the subject
        msg['Subject'] = "Confirmation code\n"
        # Make sure you also add new lines to your body
        body = f"{code} is your confirmation code\n"
        # and then attach that body furthermore you can also send html content.
        
        server.quit()

    def messaged(self):

        _, mail = self.domain()
        status = True

        try:
            match mail:
                case True:
                    self.send_mail(mail=self.contact)
                case False:
                    self.send_sms(phone=self.contact)
            if isinstance(mail, tuple):
                self.send_mail(mail=mail[0])
                self.send_sms(phone=mail[1])
        except:
            status = False
        return status

    def get_inbox(self):

        mail = IMAP4_SSL(self.__host)
        mail.login(self.__mail, self.__mailpwd)
        mail.select("inbox")
        _, search_data = mail.search(None, 'UNSEEN')
        my_message = []
        for num in search_data[0].split():
            email_data = {}
            _, data = mail.fetch(num, '(RFC822)')
            # print(data[0])
            _, b = data[0]
            email_message = message_from_bytes(b)
            for header in ['subject', 'to', 'from', 'date']:
                print("{}: {}".format(header, email_message[header]))
                email_data[header] = email_message[header]
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()
                elif part.get_content_type() == "text/html":
                    html_body = part.get_payload(decode=True)
                    email_data['html_body'] = html_body.decode()
            my_message.append(email_data)
        return my_message

    def __call__(self, *args: tuple, **kwds: dict) -> int:

        if isinstance(self.contact, list):
            assert self.subjt and self.text is not None
        else:
            assert self.contact is dict
        return self.messaged()
        