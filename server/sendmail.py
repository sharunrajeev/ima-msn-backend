import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
load_dotenv()
# Set up email parameters
sender_email = os.environ.get("MAIL_ID")
sender_password = os.environ.get("MAIL_PASS")

def send_mail(email_to,user_password,username):
# Create a message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email_to
    message['Subject'] = 'Cognosco login credentials'

    # Add the username and password to the message
    body = f'Dear {username}\nYour username is {email_to} and \nyour password is {user_password}.'
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, email_to, text)
def send_mail_reset(email_to,user_password):
# Create a message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email_to
    message['Subject'] = 'Cognosco Registration Password Reset'

    # Add the username and password to the message
    body = f'Dear User\nYour new password is {user_password}.'
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, email_to, text)

def send_mail_link(email_to,username):
# Create a message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email_to
    message['Subject'] = 'Cognosco login credentials'

    # Add the username and password to the message
    body = f'Dear {username}\nYour Payment has been verified\nJoin the whatsapp group through the link given below.\nhttps://chat.whatsapp.com/HacGrs1p4h56I84MMt3bkS'
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, email_to, text)

def send_mail_reject(email_to,username):
# Create a message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email_to
    message['Subject'] = 'Cognosco Application Rejected'

    # Add the username and password to the message
    body = f'Dear {username}\nYour Application for Cognosco 2023 has been rejected as we were not able to verify your payment. If interested kindly register again and upload your details '
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, email_to, text)