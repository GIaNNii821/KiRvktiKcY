# 代码生成时间: 2025-09-19 21:03:34
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# message_notification_system.py
# A simple message notification system using the Bottle framework.

# Import required modules
from bottle import route, run, request, HTTPError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

# Define constants
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'username'
SMTP_PASSWORD = 'password'
FROM_EMAIL = 'from@example.com'

# Function to send an email
def send_email(to_email, subject, message):
    try:
        # Create MIME multipart message
        msg = MIMEMultipart()
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email
        msg['Subject'] = Header(subject, 'utf-8')
        
        # Add the message to the MIME message
        msg.attach(MIMEText(message, 'plain', 'utf-8'))
        
        # Send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, [to_email], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Route to handle POST requests for sending notifications
@route('/notify', method='POST')
def notify():
    try:
        # Get data from request
        data = request.json
        to_email = data.get('email')
        subject = data.get('subject')
        message = data.get('message')

        # Check if all required fields are present
        if not all([to_email, subject, message]):
            raise ValueError('Missing required fields in the request body')
        
        # Send the notification email
        if send_email(to_email, subject, message):
            return {'status': 'success', 'message': 'Notification sent successfully'}
        else:
            return {'status': 'error', 'message': 'Failed to send notification'}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception as e:
        return {'status': 'error', 'message': 'An unexpected error occurred'}

# Run the Bottle application
run(host='localhost', port=8080, debug=True)
