"""
Call Disposition Handler for Storm911
Manages end-of-call processes, data collection, and export
"""

import os
import logging
from datetime import datetime
from typing import Dict, Optional, Tuple, List

from config import EXPORTS_DIR
from pdf_handler import PDFHandler
from email_handler import EmailHandler
from api_handler import APIHandler
from utils import (
    generate_confirmation_number,
    format_duration,
    format_address,
    sanitize_filename
)

class DispositionHandler:
    def __init__(
        self,
        pdf_handler: PDFHandler,
        email_handler: EmailHandler,
        api_handler: APIHandler
    ):
        """Initialize Disposition Handler"""
        self.pdf_handler = pdf_handler
        self.email_handler = email_handler
        self.api_handler = api_handler
        
        # Ensure exports directory exists
        os.makedirs(EXPORTS_DIR, exist_ok=True)
    
    def process_call_disposition(
        self,
        disposition_type: str,
        call_data: Dict,
        notes: str = ""
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Process call disposition
        Returns (success, message, pdf_path) tuple
        """
        try:
            # Generate confirmation number
            confirmation = generate_confirmation_number()
            
            # Add disposition details
            disposition_data = self._prepare_disposition_data(
                disposition_type,
                call_data,
                confirmation,
                notes
            )
            
            # Generate PDF report
            pdf_path = self.pdf_handler.generate_call_report(disposition_data)
            
            # Update API if appointment scheduled
            if disposition_type == "appointment_scheduled":
                success, message = self._handle_appointment_scheduled(
                    disposition_data,
                    pdf_path
                )
                if not success:
                    return False, message, None
            
            # Update API with disposition
            success, message = self.api_handler.update_lead(
                call_data['lead_id'],
                {'disposition': disposition_type, 'notes': notes}
            )
            
            if not success:
                return False, message, None
            
            return True, "Call disposition processed successfully", pdf_path
            
        except Exception as e:
            logging.error(f"Error processing call disposition: {str(e)}")
            return False, f"Error processing disposition: {str(e)}", None
    
    def _prepare_disposition_data(
        self,
        disposition_type: str,
        call_data: Dict,
        confirmation: str,
        notes: str
    ) -> Dict:
        """Prepare data for disposition processing"""
        # Get current timestamp
        timestamp = datetime.now()
        
        # Format address
        address = format_address(
            call_data.get('address', ''),
            call_data.get('city', ''),
            call_data.get('state', ''),
            call_data.get('zip', '')
        )
        
        # Calculate appointment duration if applicable
        duration = None
        if disposition_type == "appointment_scheduled":
            duration = format_duration(
                self._calculate_appointment_duration(call_data)
            )
        
        return {
            # Basic Information
            'disposition_type': disposition_type,
            'confirmation_number': confirmation,
            'disposition_date': timestamp.strftime('%Y-%m-%d'),
            'disposition_time': timestamp.strftime('%H:%M:%S'),
            
            # Customer Information
            'customer_name': call_data.get('customer_name', ''),
            'address': address,
            'phone': call_data.get('phone', ''),
            'email': call_data.get('email', ''),
            
            # Roof Information
            'stories': call_data.get('stories', ''),
            'roof_age': call_data.get('roof_age', ''),
            'roof_type': call_data.get('roof_type', ''),
            
            # Insurance Information
            'has_insurance': call_data.get('has_insurance', ''),
            'insurance_company': call_data.get('insurance_company', ''),
            'is_homeowner': call_data.get('is_homeowner', ''),
            'has_contractor': call_data.get('has_contractor', ''),
            
            # Appointment Information
            'appointment_date': call_data.get('appointment_date', ''),
            'appointment_time': call_data.get('appointment_time', ''),
            'appointment_duration': duration,
            
            # Additional Information
            'notes': notes,
            'lead_id': call_data.get('lead_id', '')
        }
    
    def _handle_appointment_scheduled(
        self,
        disposition_data: Dict,
        pdf_path: str
    ) -> Tuple[bool, str]:
        """Handle appointment scheduled disposition"""
        try:
            # Generate appointment confirmation PDF
            confirmation_pdf = self.pdf_handler.generate_appointment_confirmation(
                disposition_data
            )
            
            # Send confirmation email
            if disposition_data.get('email'):
                self.email_handler.send_appointment_confirmation(
                    disposition_data['email'],
                    disposition_data,
                    confirmation_pdf
                )
            
            # Send internal report email
            self.email_handler.send_call_report(
                "appointments@storm911.com",
                disposition_data,
                pdf_path
            )
            
            return True, "Appointment scheduled and confirmations sent"
            
        except Exception as e:
            logging.error(f"Error handling appointment scheduled: {str(e)}")
            return False, f"Error handling appointment: {str(e)}"
    
    def _calculate_appointment_duration(self, call_data: Dict) -> int:
        """Calculate appointment duration in minutes"""
        # Base duration
        duration = 30
        
        # Adjust for roof type
        roof_type = call_data.get('roof_type', '').lower()
        if 'metal' in roof_type:
            duration += 15
        elif 'tile' in roof_type:
            duration += 20
        elif 'slate' in roof_type:
            duration += 25
        
        # Adjust for number of stories
        stories = call_data.get('stories', '').lower()
        if '2' in stories:
            duration += 15
        elif '3' in stories or 'three' in stories:
            duration += 30
        
        return duration
    
    def get_disposition_options(self) -> List[Dict]:
        """Get list of available disposition options"""
        return [
            {
                'id': 'appointment_scheduled',
                'label': 'Appointment Scheduled',
                'requires_notes': True,
                'requires_confirmation': True
            },
            {
                'id': 'not_interested',
                'label': 'Not Interested',
                'requires_notes': True,
                'requires_confirmation': False
            },
            {
                'id': 'call_back',
                'label': 'Call Back Later',
                'requires_notes': True,
                'requires_confirmation': False
            },
            {
                'id': 'wrong_number',
                'label': 'Wrong Number',
                'requires_notes': False,
                'requires_confirmation': False
            },
            {
                'id': 'no_answer',
                'label': 'No Answer',
                'requires_notes': False,
                'requires_confirmation': False
            },
            {
                'id': 'busy',
                'label': 'Busy',
                'requires_notes': False,
                'requires_confirmation': False
            },
            {
                'id': 'disconnected',
                'label': 'Disconnected',
                'requires_notes': False,
                'requires_confirmation': False
            },
            {
                'id': 'do_not_call',
                'label': 'Do Not Call',
                'requires_notes': True,
                'requires_confirmation': False
            },
            {
                'id': 'other',
                'label': 'Other',
                'requires_notes': True,
                'requires_confirmation': False
            }
        ]
    
    def validate_disposition_data(
        self,
        disposition_type: str,
        call_data: Dict,
        notes: str = ""
    ) -> Tuple[bool, str]:
        """Validate disposition data"""
        # Get disposition options
        options = self.get_disposition_options()
        disposition = next(
            (opt for opt in options if opt['id'] == disposition_type),
            None
        )
        
        if not disposition:
            return False, "Invalid disposition type"
        
        # Check required notes
        if disposition['requires_notes'] and not notes:
            return False, "Notes are required for this disposition"
        
        # Check required fields for appointment scheduling
        if disposition_type == "appointment_scheduled":
            required_fields = [
                'customer_name',
                'address',
                'city',
                'state',
                'zip',
                'phone',
                'appointment_date',
                'appointment_time'
            ]
            
            missing = [f for f in required_fields if not call_data.get(f)]
            if missing:
                return False, f"Missing required fields: {', '.join(missing)}"
        
        return True, "Disposition data valid"
