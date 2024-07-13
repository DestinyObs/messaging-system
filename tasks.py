# tasks.py
from celery import shared_task

@shared_task
def send_email(recipient):
    print(f"Sending email to {recipient}")
    # Placeholder for actual email sending logic
    return f"Email task simulated for {recipient}"
