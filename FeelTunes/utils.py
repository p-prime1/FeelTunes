from flask_mail import Message
from flask import current_app

def send_email(to, subject, body):
    # Sends an email using the Flask-Mail extension.
    
    mail = current_app.extensions['mail']
    msg = Message(subject=subject, recipients=[to], body=body)
    mail.send(msg)
