import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_email(to_addr, subject, body, file_path, file_name):
    from_addr = EMAIL_ADDRESS
    password = EMAIL_PASSWORD

    msg = MIMEMultipart()

    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject

    body = MIMEText(body, 'html')
    msg.attach(body)

    try:
        with open(file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
    except FileNotFoundError:
        print(f"No attachment found at {file_path}")
        return

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {file_name}",
    )

    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_addr, password)
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()
        print(f"Email sent to {to_addr}")
    except Exception as e:
        print(f"Failed to send email to {to_addr} due to {e}")
