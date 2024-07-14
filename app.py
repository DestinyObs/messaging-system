from flask import Flask, request, jsonify
import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from config import SMTP_HOST, SMTP_USER, SMTP_PASSWORD, EMAILS_FROM_EMAIL, SMTP_TLS, SMTP_SSL, SMTP_PORT
from celery import Celery


app = Flask(__name__)


# Define the log directory
log_directory = '/var/log/messaging_system.log'



app.config.update(
    CELERY_BROKER_URL='amqp://guest:guest@localhost',  # Updated to use RabbitMQ
    CELERY_RESULT_BACKEND='rpc://'
)

# Directly instantiate Celery without using make_celery
celery = Celery(
    app.name,
    broker=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND']
)

# Update the Celery configuration with the Flask app's config
celery.conf.update(app.config)


@celery.task
def send_email_task(recipient):
    sender_email = EMAILS_FROM_EMAIL
    password = SMTP_PASSWORD

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = "Hello from Flask App"

    message.attach(MIMEText("This is a test email sent from a Flask application.", "plain"))
    message.attach(MIMEText("<p>This is a test email sent from a Flask application.</p>", "html"))

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        if SMTP_TLS:
            server.starttls()
        elif SMTP_SSL:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.login(SMTP_USER, password)
        server.send_message(message)
        server.quit()
        return f"Email sent to {recipient}."
    except Exception as e:
        return f"Failed to send email: {str(e)}"


# Define the root route handler for the Flask app
@app.route('/', methods=['GET', 'POST'])
def index(sendmail=None, talktome=False):
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')
    # If the 'sendmail' parameter is present, queue an email to be sent
    if sendmail:
        send_email_task.delay(sendmail)  # Corrected from send_email to send_email_task
        return f"Email queued to be sent to {sendmail}"
    # If the 'talktome' parameter is present, append the current timestamp to the log file
    if talktome:
        with open(log_directory, 'a') as log_file:
            log_file.write(f"{datetime.now()}\n")
        return f"Logged current time to {log_directory}"
    return f"Hi there, welcome to the Obs messaging system. Sendmail: {sendmail}, Talktome: {talktome}"




# @celery.task
# def log_event(message):
#     logger = logging.getLogger(__name__)
#     logger.info(message)
#     return f"Log event '{message}' processed."

from datetime import datetime

@celery.task
def log_event(message):
    logger = logging.getLogger(__name__)
    # Get the current time and format it as desired
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Include the current time in the log message
    logger.info(f"{current_time} - {message}")
    return f"Log event '{message}' processed."



@app.route('/logs', methods=['GET'])
def view_logs():
    try:
        with open(log_directory, 'r') as log_file:
            log_content = log_file.read()
        return f"<pre>{log_content}</pre>"  # Display logs in preformatted text
    except FileNotFoundError:
        # Handle case where the log file does not exist
        return "Log file not found."



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

# if __name__ == '__main__':
#     app.run(debug=True)
