import smtplib

from email.message import EmailMessage
import read_env


def send_email(to, message, subject=""):
    ## setup data
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = read_env.get_value('EMAIL')
    msg['To'] = [to]
    
    ## connect to the server 
    server = smtplib.SMTP("smtp.office365.com", 587)    
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    ## login 
    server.login(read_env.get_value('EMAIL'), read_env.get_value('PASSWORD'))    
    # send message 
    server.send_message(msg)
    # close connection 
    server.quit()