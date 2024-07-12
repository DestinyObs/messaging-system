# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(port=8080, debug=True)



from flask import Flask, request
from datetime import datetime
import os
import logging
import pika
from celery import Celery

app = Flask(__name__)
rabbitmq_url = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@localhost')
celery_app = Celery('tasks', broker=rabbitmq_url)

@app.route('/')
def home():
    return 'Hello, World!'

@celery_app.task
def send_email(email):
    # Simulate sending an email
    print(f"Simulating sending email to {email}")
    return True

@app.route('/sendmail')
def send_mail_endpoint():
    email = request.args.get('sendmail')
    if email:
        result = send_email.delay(email)
        return f"Email task queued for {email}, task ID: {result.id}"
    else:
        return "No email address provided", 400


@app.route('/talktome')
def talk_to_me():
    # Define the log file path
    log_path = './log/messaging_system.log'
    
    # Check if the log directory exists, if not, create it
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Append the log entry
    with open(log_path, 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Requested\n")
    
    return "Logged successfully"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
