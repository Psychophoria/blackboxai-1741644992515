"""
Email Handler for Storm911
"""

import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email_validator import validate_email, EmailNotValidError

class EmailHandler:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        """Initialize Email Handler"""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = os.getenv("STORM911_EMAIL")
        self.sender_password = os.getenv("STORM911_EMAIL_PASSWORD")
        
        if not self.sender_email or not self.sender_password:
            logging.warning("Email credentials not found in environment variables")
    
    def validate_email_address(self, email):
        """Validate email address format"""
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
    
    def send_appointment_confirmation(self, recipient_email, appointment_data, pdf_path=None):
        """Send appointment confirmation email"""
        if not self.validate_email_address(recipient_email):
            raise ValueError("Invalid recipient email address")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Storm911 - Roof Inspection Appointment Confirmation"
        
        # Email body
        body = f"""
        Dear {appointment_data.get('customer_name', '')},

        Thank you for scheduling your FREE roof inspection with Storm911.

        Your appointment is confirmed for:
        Date: {appointment_data.get('appointment_date', '')}
        Time: {appointment_data.get('appointment_time', '')}
        Address: {appointment_data.get('address', '')}, {appointment_data.get('city', '')}, {appointment_data.get('state', '')} {appointment_data.get('zip', '')}

        What to Expect:
        - Our professional inspector will arrive at the scheduled time
        - The inspection will take approximately 30 minutes
        - We will thoroughly examine your roof for any storm damage
        - You will receive a detailed report of our findings

        Important Notes:
        - No payment is required for this inspection
        - We work with all insurance companies
        - You will receive professional documentation of any damage found

        If you need to reschedule or have any questions, please contact us at:
        Phone: 1-800-STORM911
        Email: appointments@storm911.com

        Thank you for choosing Storm911 for your roof inspection needs.

        Best regards,
        The Storm911 Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF if provided
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
                pdf_attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(pdf_path)
                )
                msg.attach(pdf_attachment)
        
        try:
            # Create secure SSL/TLS connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            
            # Login and send email
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            logging.info(f"Appointment confirmation email sent to {recipient_email}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send appointment confirmation email: {str(e)}")
            raise
    
    def send_call_report(self, recipient_email, report_data, pdf_path=None):
        """Send call report email"""
        if not self.validate_email_address(recipient_email):
            raise ValueError("Invalid recipient email address")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Storm911 - Call Report"
        
        # Email body
        body = f"""
        Call Report Summary

        Customer Information:
        Name: {report_data.get('customer_name', '')}
        Phone: {report_data.get('phone', '')}
        Address: {report_data.get('address', '')}
        
        Roofing Information:
        Stories: {report_data.get('stories', '')}
        Roof Age: {report_data.get('roof_age', '')}
        Roof Type: {report_data.get('roof_type', '')}
        
        Insurance Information:
        Has Insurance: {report_data.get('has_insurance', '')}
        Insurance Company: {report_data.get('insurance_company', '')}
        
        Appointment Information:
        Date: {report_data.get('appointment_date', '')}
        Time: {report_data.get('appointment_time', '')}

        Please find the detailed report attached.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach PDF if provided
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
                pdf_attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(pdf_path)
                )
                msg.attach(pdf_attachment)
        
        try:
            # Create secure SSL/TLS connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            
            # Login and send email
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            logging.info(f"Call report email sent to {recipient_email}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send call report email: {str(e)}")
            raise
    
    def send_test_email(self, recipient_email):
        """Send test email to verify configuration"""
        if not self.validate_email_address(recipient_email):
            raise ValueError("Invalid recipient email address")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Storm911 - Email Test"
        
        body = """
        This is a test email from Storm911.
        
        If you received this email, the email configuration is working correctly.
        
        Best regards,
        The Storm911 Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            # Create secure SSL/TLS connection
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            
            # Login and send email
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            logging.info(f"Test email sent to {recipient_email}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to send test email: {str(e)}")
            raise
