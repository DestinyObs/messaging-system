# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return 'Hello, World!'

# if __name__ == '__main__':
#     app.run(port=8080, debug=True)



# from flask import Flask, request
# from datetime import datetime
# import os
# import logging
# import pika
# from celery import Celery

# app = Flask(__name__)
# rabbitmq_url = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@localhost')
# celery_app = Celery('tasks', broker=rabbitmq_url)

# @app.route('/')
# def home():
#     return 'Hello, World!'

# @celery_app.task
# def send_email(email):
#     # Simulate sending an email
#     print(f"Simulating sending email to {email}")
#     return True

# @app.route('/sendmail')
# def send_mail_endpoint():
#     email = request.args.get('sendmail')
#     if email:
#         result = send_email.delay(email)
#         return f"Email task queued for {email}, task ID: {result.id}"
#     else:
#         return "No email address provided", 400


# @app.route('/talktome')
# def talk_to_me():
#     # Define the log file path
#     log_path = './log/messaging_system.log'

#     # Check if the log directory exists, if not, create it
#     log_dir = os.path.dirname(log_path)
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)

#     # Append the log entry
#     with open(log_path, 'a') as log_file:
#         log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Requested\n")

#     return "Logged successfully"

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)


# import logging
# from flask import Flask, request
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from datetime import datetime
# import os
# from config import SMTP_HOST, SMTP_USER, SMTP_PASSWORD, EMAILS_FROM_EMAIL, SMTP_TLS, SMTP_SSL, SMTP_PORT
# from celery import make_celery


# app = Flask(__name__)

# app.config.update(
#     CELERY_BROKER_URL='redis://localhost:6379',
#     CELERY_RESULT_BACKEND='redis://localhost:6379'
# )

# celery = make_celery(app)


# @app.route('/')
# def index():
#     return "Welcome to the Messaging System!"



# # Configure logging
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s',
#                     handlers=[logging.FileHandler('./log/messaging_system.log'),
#                               logging.StreamHandler()])



# # @app.route('/sendmail', methods=['GET'])
# # def send_mail():
# #     recipient = request.args.get('recipient')
# #     if not recipient:
# #         return "Please provide a recipient email address.", 400

# #     # Use the SMTP settings from your configuration
# #     sender_email = EMAILS_FROM_EMAIL
# #     receiver_email = recipient
# #     password = SMTP_PASSWORD

# #     # Create a multipart message and set headers
# #     message = MIMEMultipart()
# #     message["From"] = sender_email
# #     message["To"] = receiver_email
# #     message["Subject"] = "Hello from Flask App"

# #     # Add plain-text and HTML version of your message
# #     message.attach(MIMEText("This is a test email sent from a Flask application.", "plain"))
# #     message.attach(MIMEText("<p>This is a test email sent from a Flask application.</p>", "html"))

# #     try:
# #         server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
# #         server.starttls() if SMTP_TLS else server.startssl()
# #         server.login(SMTP_USER, password)
# #         server.send_message(message)  # Use send_message for multipart messages
# #         server.quit()
# #         return f"Email sent to {receiver_email}.", 200
# #     except Exception as e:
# #         return f"Failed to send email: {str(e)}", 500



# @celery.task
# def send_email_task(recipient):
#     # Use the same logging configuration as your Flask app
#     logger = logging.getLogger(__name__)

#     sender_email = EMAILS_FROM_EMAIL
#     password = SMTP_PASSWORD

#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = recipient
#     message["Subject"] = "Hello from Flask App"

#     message.attach(MIMEText("This is a test email sent from a Flask application.", "plain"))
#     message.attach(MIMEText("<p>This is a test email sent from a Flask application.</p>", "html"))

#     try:
#         server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
#         server.starttls() if SMTP_TLS else server.startssl()
#         server.login(SMTP_USER, password)
#         server.send_message(message)
#         server.quit()
#         logger.info(f"Email sent to {recipient}.")
#         return f"Email sent to {recipient}."
#     except Exception as e:
#         logger.error(f"Failed to send email: {str(e)}")
#         return f"Failed to send email: {str(e)}"


        

# @app.route('/sendmail', methods=['GET'])
# def send_mail():
#     recipient = request.args.get('recipient')
#     if not recipient:
#         return "Please provide a recipient email address.", 400

#     result = send_email_task.delay(recipient)
#     return f"Email task queued for {recipient}.", 202


# @celery.task
# def log_event(message):
#     logger = logging.getLogger(__name__)
#     logger.info(message)
#     return f"Log event '{message}' processed."


# # @app.route('/talktome', methods=['GET'])
# # def talk_to_me():
# #     # Log the event
# #     logging.info("Talk to Me endpoint accessed.")
# #     return "Logged successfully."


# @app.route('/talktome', methods=['GET'])
# def talk_to_me():
#     # Enqueue the logging task
#     result = log_event.delay("Talk to Me endpoint accessed.")
    
#     # Optionally, you can wait for the task to finish and get its result
#     # This is not necessary for most use cases, as the primary goal is to offload the task
#     # result = AsyncResult(result.task_id).get(timeout=10)
    
#     return "Logged successfully."



# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8080, debug=True)


from flask import Flask, request
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from config import SMTP_HOST, SMTP_USER, SMTP_PASSWORD, EMAILS_FROM_EMAIL, SMTP_TLS, SMTP_SSL, SMTP_PORT
from celery import Celery

app = Flask(__name__)

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

@app.route('/')
def index():
    return "Welcome to the Messaging System!"

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('./log/messaging_system.log'),
                              logging.StreamHandler()])

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

@app.route('/sendmail', methods=['GET'])
def send_mail():
    recipient = request.args.get('recipient')
    if not recipient:
        return "Please provide a recipient email address.", 400

    result = send_email_task.delay(recipient)
    return f"Email task queued for {recipient}.", 202

@celery.task
def log_event(message):
    logger = logging.getLogger(__name__)
    logger.info(message)
    return f"Log event '{message}' processed."

@app.route('/talktome', methods=['GET'])
def talk_to_me():
    result = log_event.delay("Talk to Me endpoint accessed.")
    return "Logged successfully."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
