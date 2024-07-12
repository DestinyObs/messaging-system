from celery import Celery
from datetime import datetime
import smtplib
from flask import Flask, request, render_template

# Configure Celery with RabbitMQ broker
app = Celery('tasks', broker='amqp://localhost')

# Function to send email (using Sendinblue details)
@app.task
def send_email(recipient):
    # Replace with your Sendinblue credentials (not your Gmail credentials)
    sender = 'info@example.com'  # Replace with your desired sender email
    password = 'wIzNjV9dZF5T6qsh'  # Replace with your Sendinblue API key

    message = f'This is a test email sent to {recipient}.'

    with smtplib.SMTP(host='smtp-relay.sendinblue.com', port=587) as server:
        server.starttls()  # Use TLS encryption
        server.login(sender, password)
        server.sendmail(sender, recipient, message)
    print(f"Email sent to {recipient}")

# Function to log message
def log_message():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("/var/log/messaging_system.log", "a") as f:
        f.write(f"{now}\n")
    print(f"Logged message to /var/log/messaging_system.log")

# Flask app
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sendmail", methods=["POST"])
def send_mail():
    recipient = request.form.get("recipient")
    if recipient:
        send_email.delay(recipient)
        return "Email queued for sending."
    return "Invalid recipient email."

@app.route("/logmessage")
def log_message_route():
    log_message()
    return "Message logged."

if __name__ == "__main__":
    app.run(debug=True)
