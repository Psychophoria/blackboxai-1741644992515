"""
API Handler for Storm911 - Manages interactions with ReadyMode API
"""

import logging
import requests
from datetime import datetime
from typing import Dict, Optional, Tuple, Any

from config import API_BASE_URL, API_ENDPOINTS, ERRORS

class APIHandler:
    def __init__(self, api_user: str = None, api_pass: str = None):
        """Initialize API Handler"""
        self.api_user = api_user
        self.api_pass = api_pass
        self.base_url = API_BASE_URL
        self.session = requests.Session()
    
    def set_credentials(self, api_user: str, api_pass: str) -> None:
        """Set API credentials"""
        self.api_user = api_user
        self.api_pass = api_pass
    
    def _get_auth_params(self) -> Dict[str, str]:
        """Get authentication parameters"""
        return {
            'API_user': self.api_user,
            'API_pass': self.api_pass
        }
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None, 
        data: Optional[Dict] = None
    ) -> Tuple[bool, Any]:
        """
        Make API request with error handling
        Returns (success, data/error_message) tuple
        """
        if not self.api_user or not self.api_pass:
            return False, ERRORS['api']['authentication']
        
        # Combine authentication params with any additional params
        request_params = self._get_auth_params()
        if params:
            request_params.update(params)
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=request_params,
                json=data,
                timeout=30
            )
            
            # Log request (excluding sensitive data)
            logging.debug(f"API Request: {method} {url}")
            logging.debug(f"Status Code: {response.status_code}")
            
            if response.ok:
                return True, response.json()
            elif response.status_code == 401:
                return False, ERRORS['api']['authentication']
            elif response.status_code == 404:
                return False, ERRORS['api']['not_found']
            else:
                return False, ERRORS['api']['server']
                
        except requests.exceptions.ConnectionError:
            return False, ERRORS['api']['connection']
        except requests.exceptions.Timeout:
            return False, "Request timed out. Please try again."
        except Exception as e:
            logging.error(f"API request error: {str(e)}")
            return False, str(e)
    
    def search_lead(self, phone: str) -> Tuple[bool, Any]:
        """Search for lead by phone number"""
        endpoint = API_ENDPOINTS['search_lead'].format(phone=phone)
        return self._make_request('GET', endpoint)
    
    def create_lead(self, lead_data: Dict) -> Tuple[bool, Any]:
        """Create new lead"""
        endpoint = API_ENDPOINTS['create_lead']
        
        # Add timestamp
        lead_data['created_at'] = datetime.now().isoformat()
        
        return self._make_request('POST', endpoint, data=lead_data)
    
    def update_lead(self, lead_id: str, lead_data: Dict) -> Tuple[bool, Any]:
        """Update existing lead"""
        endpoint = API_ENDPOINTS['update_lead'].format(id=lead_id)
        
        # Add timestamp
        lead_data['updated_at'] = datetime.now().isoformat()
        
        return self._make_request('PUT', endpoint, data=lead_data)
    
    def validate_credentials(self) -> Tuple[bool, str]:
        """
        Validate API credentials
        Returns (is_valid, message) tuple
        """
        # Try a simple API call to validate credentials
        success, result = self.search_lead('0000000000')
        
        if success:
            return True, "API credentials validated successfully"
        elif result == ERRORS['api']['authentication']:
            return False, "Invalid API credentials"
        else:
            return False, "Could not validate API credentials"
    
    def format_lead_data(self, data: Dict) -> Dict:
        """Format lead data for API submission"""
        formatted = {
            'firstName': data.get('first_name', ''),
            'lastName': data.get('last_name', ''),
            'address': data.get('address', ''),
            'city': data.get('city', ''),
            'state': data.get('state', ''),
            'zip': data.get('zip', ''),
            'phone': data.get('phone', ''),
            'phone2': data.get('cell', ''),
            'email': data.get('email', ''),
            'notes': data.get('notes', ''),
            'appointmentDate': data.get('appointment_date', ''),
            'appointmentTime': data.get('appointment_time', ''),
            'roofStories': data.get('stories', ''),
            'roofAge': data.get('roof_age', ''),
            'roofType': data.get('roof_type', ''),
            'hasInsurance': data.get('has_insurance', ''),
            'insuranceCompany': data.get('insurance_company', ''),
            'isHomeowner': data.get('is_homeowner', ''),
            'hasContractor': data.get('has_contractor', '')
        }
        
        # Remove empty values
        return {k: v for k, v in formatted.items() if v}
    
    def parse_lead_data(self, api_data: Dict) -> Dict:
        """Parse API lead data into application format"""
        return {
            'first_name': api_data.get('firstName', ''),
            'last_name': api_data.get('lastName', ''),
            'address': api_data.get('address', ''),
            'city': api_data.get('city', ''),
            'state': api_data.get('state', ''),
            'zip': api_data.get('zip', ''),
            'phone': api_data.get('phone', ''),
            'cell': api_data.get('phone2', ''),
            'email': api_data.get('email', ''),
            'notes': api_data.get('notes', ''),
            'appointment_date': api_data.get('appointmentDate', ''),
            'appointment_time': api_data.get('appointmentTime', ''),
            'stories': api_data.get('roofStories', ''),
            'roof_age': api_data.get('roofAge', ''),
            'roof_type': api_data.get('roofType', ''),
            'has_insurance': api_data.get('hasInsurance', ''),
            'insurance_company': api_data.get('insuranceCompany', ''),
            'is_homeowner': api_data.get('isHomeowner', ''),
            'has_contractor': api_data.get('hasContractor', '')
        }
    
    def close(self):
        """Close API session"""
        self.session.close()
