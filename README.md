Here's a suggested README for your GitHub repository, `messaging-system`:

---

# Messaging System

This project implements a messaging system using Flask, Celery, RabbitMQ, and Nginx. The system provides endpoints for sending emails and logging events, and it uses Celery to queue tasks and RabbitMQ as the message broker.

## Features

- **Email Sending**: Queue email tasks using Celery and send them via SMTP.
- **Logging**: Log events with the current timestamp to a specified log file.
- **Nginx Reverse Proxy**: Serve the Flask application behind an Nginx reverse proxy.
- **Exposed Endpoint**: Use Ngrok to expose the local application for external access.

## Requirements

- Python 3.10
- Flask
- Celery
- RabbitMQ
- Nginx
- Ngrok
- SMTP server for sending emails

## Setup Instructions

### Clone the Repository

```bash
git clone https://github.com/DestinyObs/messaging-system.git
cd messaging-system
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure SMTP Settings

Create a `config.py` file in the project root and add your SMTP settings:

```python
SMTP_HOST = "your_smtp_host"
SMTP_USER = "your_smtp_user"
SMTP_PASSWORD = "your_smtp_password"
EMAILS_FROM_EMAIL = "your_email@example.com"
SMTP_TLS = True
SMTP_SSL = False
SMTP_PORT = 587
```

### Start RabbitMQ

Ensure RabbitMQ is installed and running on your local machine. Start the RabbitMQ server:

```bash
rabbitmq-server
```

### Start the Celery Worker

Run the following command to start the Celery worker:

```bash
celery -A app.celery worker --loglevel=info
```

### Start the Flask Application

Run the Flask application:

```bash
python app.py
```

### Configure Nginx

Set up Nginx to reverse proxy requests to your Flask application. An example Nginx configuration might look like this:

```nginx
server {
    listen 80;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Restart Nginx to apply the configuration.

### Expose Endpoint Using Ngrok

Use Ngrok to expose your local application to the internet:

```bash
ngrok http 8080
```

Copy the generated URL and use it to access your application externally.

## Usage

### Send Email

To queue an email sending task, make a GET request to the `/sendmail` endpoint with the recipient's email address as a parameter:

```
GET /sendmail?recipient=recipient@example.com
```

### Log Event

To log an event, make a GET request to the `/talktome` endpoint:

```
GET /talktome
```

## Logging

Logs are written to `./log/messaging_system.log` by default. Ensure the log directory exists and is writable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.

## Contact

For any questions or issues, please contact [Destiny Obueh](mailto:destinyobueh14@gmail.com).
