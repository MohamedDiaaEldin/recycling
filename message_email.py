import smtplib

from email.message import EmailMessage



def send_email(to, message, subject=""):
    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = subject
    msg['From'] = "bikya.service@gmail.com"
    msg['To'] = to
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("bikya.service@gmail.com", "Mohamed12..")
    server.send_message(msg)
    server.quit()