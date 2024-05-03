from django.test import TestCase

# Create your tests here.
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPAuthenticationError

def send_simple_message(mailfrom, mailpw, mailto, mailsubject, mailcontent):
    global message
    strSmtp = "smtp.gmail.com:587"  # SMTP server
    strAccount = mailfrom  # Sender's email
    strPassword = mailpw  # Sender's password
    msg = MIMEText(mailcontent)
    msg["Subject"] = mailsubject  # Email subject
    mailto1 = mailto  # Recipient's email
    try:
        server = SMTP(strSmtp)  # Establish SMTP connection
        server.ehlo()  # Greet the SMTP server
        server.starttls()  # Start TLS encryption
        server.login(strAccount, strPassword)  # Login
        server.sendmail(strAccount, mailto1, msg.as_string())  # Send email
        message = "郵件已成功寄出！"  # Success message
    except SMTPAuthenticationError:
        message = "無法登入！"  # Authentication error message
    except Exception as e:
        message = f"郵件發送產生錯誤： {str(e)}"  # Generic error message
    finally:
        server.quit()  # Close the connection

# Test the function
send_simple_message("jason568911@gmail.com", "pqrl tbjh enxp qjtb", "jason568911@gmail.com", "Test Subject", "Test Content")
print(message)
