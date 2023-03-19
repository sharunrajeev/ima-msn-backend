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
    message['Subject'] = 'IMA-MSN login credentials'

    # Add the username and password to the message
    body = f'Dear {username}\nYour username is {email_to} and \nyour password is {user_password}.'
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, email_to, text)