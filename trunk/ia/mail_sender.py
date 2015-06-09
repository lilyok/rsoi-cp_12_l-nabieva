from email.mime.text import MIMEText
import json
import smtplib


def send_as_json(sender_address, recipient_address, content):
    connection = smtplib.SMTP('dev.iu7.bmstu.ru', 10025)
    print "send"
    message = MIMEText(json.dumps(content))
    message['From'] = sender_address
    message['To'] = recipient_address
    connection.sendmail(sender_address, recipient_address, message.as_string())
    connection.quit()
