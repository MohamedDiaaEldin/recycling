import smtplib

from email.message import EmailMessage
import read_env


def send_email(to, message, subject=""):
    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = subject
    msg['From'] = "bikya.service@gmail.com"
    msg['To'] = to
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(read_env.get_value('EMAIL'), read_env.get_value('PASSWORD'))
    server.send_message(msg)
    server.quit()