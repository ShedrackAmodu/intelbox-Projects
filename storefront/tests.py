from django.test import TestCase

# Create your tests here.
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
smtp_server = 'smtp.office365.com'
smtp_port = 587
email_address = 'onlinestorea731@hotmail.com'  # Replace with your Outlook email address
email_password = 'ppinebujilbgfkhe'  # Replace with your Outlook email password

# Email content
recipient_email = 'kolawoleisrael2500@gmail.com'  # Replace with the recipient's email address
subject = 'Test Email'
body = 'This is a test email to verify the email configuration.'

# Create the email message
msg = MIMEMultipart()
msg['From'] = email_address
msg['To'] = recipient_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

# Send the email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_address, email_password)
    text = msg.as_string()
    server.sendmail(email_address, recipient_email, text)
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
