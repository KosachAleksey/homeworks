import logging

#from datetime import datetime

logging.basicConfig(filename='notification.log', level=logging.INFO, format='%(asctime)s  - %(message)s')

def send_sms(message):
    print(f"SMS sent : {message}")
    logging.info(f"SMS sent : {message}")

def send_email(message):
    print(f"Email sent : {message}")
    logging.info(f"Email sent : {message}")

def send_notification(notification_type, callback, message):
    try:
        if notification_type not in ["sms", "email"]:
            raise ValueError("Invalid notification type")
        callback(message)
    except ValueError as err:
        print(f"Error sending notification: {err}")
        logging.error(f"Error sending notification: {err}")

send_notification("sms", send_sms, "Hello as SMS")
send_notification("email", send_email, "Hello as Email")
send_notification("push", send_sms, "This will trigger an error")
            