from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

class EmailService:
    @staticmethod
    def send_status_update(recipients: List[str], service_name: str, status: str):
        msg = MIMEMultipart()
        msg['Subject'] = f'Status Update: {service_name}'
        msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
        
        body = f"""
        Service Status Update
        
        Service: {service_name}
        New Status: {status}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(current_app.config['MAIL_SERVER']) as server:
            server.starttls()
            server.login(
                current_app.config['MAIL_USERNAME'],
                current_app.config['MAIL_PASSWORD']
            )
            server.send_message(msg, to_addrs=recipients)
