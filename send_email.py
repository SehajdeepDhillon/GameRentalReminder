import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables (secret sender email and password)
current_dir = Path(__file__).resolve().parent
envars = current_dir / ".env"
load_dotenv(envars)

# send_mail uses gmail servers to send an email
def send_email(subject, name, to):
    msg = EmailMessage()
    msg['subject'] = subject
    msg['to'] = to

    msg.set_content(
    f"Hi {name},\n\n"
    "This is a reminder from the MathSoc board game library that your game is now overdue. "
    "Please return it as soon as possible.\n\n"
    "Thanks,\n"
    "Board Game Director"
    )


    # email and password are in a .env file to safety hide them
    user = os.getenv("EMAIL")
    msg['from'] = formataddr(("MathSoc", f"{user}"))
    password = os.getenv("PASSWORD")

    # use SMTP gmail server for sending the email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()

if __name__ == "__main__":
    send_email(
        subject = "Outstanding Rental",
        name = "MathSoc",
        to = "dhillo68@uwindsor.ca",
    )