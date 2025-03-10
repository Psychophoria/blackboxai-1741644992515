"""
PDF Generation and Export Handler for Storm911
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class PDFHandler:
    def __init__(self):
        """Initialize PDF Handler"""
        self.exports_dir = "EXPORTS"
        self.ensure_exports_directory()
        self.styles = getSampleStyleSheet()
        
        # Create custom styles
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=10
        ))
    
    def ensure_exports_directory(self):
        """Ensure exports directory exists"""
        if not os.path.exists(self.exports_dir):
            os.makedirs(self.exports_dir)
    
    def generate_call_report(self, data):
        """Generate PDF report for a call"""
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"call_report_{timestamp}.pdf"
        filepath = os.path.join(self.exports_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build content
        story = []
        
        # Title
        story.append(Paragraph("Storm911 Call Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Date and Time
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 20))
        
        # Customer Information
        story.append(Paragraph("Customer Information", self.styles['SectionHeader']))
        customer_data = [
            ["Name:", data.get('customer_name', '')],
            ["Address:", data.get('address', '')],
            ["City:", data.get('city', '')],
            ["State:", data.get('state', '')],
            ["Zip Code:", data.get('zip', '')],
            ["Phone:", data.get('phone', '')],
            ["Cell:", data.get('cell', '')],
            ["Email:", data.get('email', '')]
        ]
        customer_table = Table(customer_data, colWidths=[100, 400])
        customer_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(customer_table)
        
        # Roofing Information
        story.append(Paragraph("Roofing Information", self.styles['SectionHeader']))
        roofing_data = [
            ["Stories:", data.get('stories', '')],
            ["Roof Age:", data.get('roof_age', '')],
            ["Roof Type:", data.get('roof_type', '')]
        ]
        roofing_table = Table(roofing_data, colWidths=[100, 400])
        roofing_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(roofing_table)
        
        # Insurance Information
        story.append(Paragraph("Insurance Information", self.styles['SectionHeader']))
        insurance_data = [
            ["Has Insurance:", data.get('has_insurance', '')],
            ["Insurance Company:", data.get('insurance_company', '')],
            ["Is Homeowner:", data.get('is_homeowner', '')],
            ["Has Contractor:", data.get('has_contractor', '')]
        ]
        insurance_table = Table(insurance_data, colWidths=[100, 400])
        insurance_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(insurance_table)
        
        # Appointment Information
        story.append(Paragraph("Appointment Information", self.styles['SectionHeader']))
        appointment_data = [
            ["Date:", data.get('appointment_date', '')],
            ["Time:", data.get('appointment_time', '')]
        ]
        appointment_table = Table(appointment_data, colWidths=[100, 400])
        appointment_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(appointment_table)
        
        # Notes
        if data.get('notes'):
            story.append(Paragraph("Notes", self.styles['SectionHeader']))
            story.append(Paragraph(data.get('notes', ''), self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        return filepath
    
    def generate_appointment_confirmation(self, data):
        """Generate appointment confirmation PDF"""
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"appointment_confirmation_{timestamp}.pdf"
        filepath = os.path.join(self.exports_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build content
        story = []
        
        # Title
        story.append(Paragraph("Roof Inspection Appointment Confirmation", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # Confirmation message
        story.append(Paragraph(
            f"Dear {data.get('customer_name', '')},",
            self.styles['Normal']
        ))
        story.append(Spacer(1, 12))
        
        confirmation_text = f"""
        This letter confirms your upcoming FREE roof inspection appointment with Storm911.
        
        Appointment Details:
        Date: {data.get('appointment_date', '')}
        Time: {data.get('appointment_time', '')}
        Address: {data.get('address', '')}, {data.get('city', '')}, {data.get('state', '')} {data.get('zip', '')}
        
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
        """
        
        story.append(Paragraph(confirmation_text, self.styles['Normal']))
        
        # Build PDF
        doc.build(story)
        return filepath
