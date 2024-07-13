```plaintext
Flask==2.1.2
celery==5.2.3
pika==1.2.0  # RabbitMQ client library
```

Dependencies such as `smtplib` and `email` are part of Python's standard library and don't need to be included in `requirements.txt`.

### Installing RabbitMQ

Since RabbitMQ is an external service, it cannot be installed via `pip` and should be installed separately. Here are installation instructions for different operating systems:

- **On Ubuntu/Debian**:

  ```bash
  sudo apt-get update
  sudo apt-get install rabbitmq-server
  sudo systemctl start rabbitmq-server
  ```

- **On CentOS/RHEL**:

  ```bash
  sudo yum install rabbitmq-server
  sudo systemctl start rabbitmq-server
  ```

- **On Windows**:

  Download the installer from the [RabbitMQ website](https://www.rabbitmq.com/install-windows.html) and follow the installation instructions.

### Installing ngrok

Download ngrok from [ngrok's download page](https://ngrok.com/download) and unzip it. You will run ngrok from the command line to expose your Flask application.

### Complete Setup Guide

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/messaging-system.git
   cd messaging-system
   ```

2. **Install Python Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install RabbitMQ** (provide OS-specific instructions or a link to RabbitMQ's installation guide).

4. **Download and Setup ngrok** (provide a link to ngrok's download page and basic usage instructions).

5. **Configure SMTP Settings** in `config.py` (guide users to create this file with necessary SMTP details).

6. **Start RabbitMQ** (provide the command based on the user's OS).

7. **Start the Celery Worker**:

   ```bash
   celery -A app.celery worker --loglevel=info
   ```

8. **Run the Flask Application**:

   ```bash
   python app.py
   ```

9. **Use ngrok to Expose the Application**:

   ```bash
   ./ngrok http 8080
   ```
