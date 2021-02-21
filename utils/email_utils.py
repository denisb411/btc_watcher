from argparse import ArgumentParser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from utils.logging_utils import create_default_logger

logger = create_default_logger(__file__)

class EmailSender():

    def __init__(self, 
                 email_login, 
                 email_password):
        self.email_login = email_login
        self.email_password = email_password
        self.__check_login()

    def __check_login(self):
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.ehlo()
        session.starttls()
        session.quit()

    def __login_and_send_message(self, 
                                 message, 
                                 receiver_email_address):

        ## Need to set gmail to `less secure` state:
        ## https://support.google.com/accounts/answer/6010255#zippy=%2Cse-a-op%C3%A7%C3%A3o-acesso-a-app-menos-seguro-estiver-ativada-para-sua-conta%2Cse-a-op%C3%A7%C3%A3o-acesso-a-app-menos-seguro-estiver-desativada-para-sua-conta 
        
        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.ehlo()
        session.starttls() #enable security
        session.login(self.email_login, self.email_password) 
        session.sendmail(self.email_login, receiver_email_address, message)
        session.quit()

        logger.info("Email sent successfully")

    def send(self,
             receiver_email_address,
             subject,
             content):
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = self.email_login
        message['To'] = receiver_email_address
        message['Subject'] = subject
        message.attach(MIMEText(content, 'plain'))

        self.__login_and_send_message(message.as_string(), receiver_email_address)
        
    def send_to_myself(self, 
                       subject, 
                       content):
        self.send(self.email_login, subject, content)

if __name__ == "__main__":

    argParser = ArgumentParser()
    argParser.add_argument('--email-login', dest="email_login", type=str, default='')
    argParser.add_argument('--email-password', dest="email_password", type=str, default='')
    argParser.add_argument('--receiver-email-address', dest="receiver_email_address", type=str, default=None)
    argParser.add_argument('--subject', dest="subject", type=str, default='EmailSender test')
    argParser.add_argument('--content', dest="content", type=str, default='EmailSender test')
    args = argParser.parse_args()

    email_sender = EmailSender(args.email_login, args.email_password)

    if args.receiver_email_address is None:
        email_sender.send_to_myself(args.subject, args.content)

    else:
        email_sender.send(args.receiver_email_address, args.email_login, args.email_password)