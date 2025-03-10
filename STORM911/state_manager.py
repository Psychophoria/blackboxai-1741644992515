"""
State Manager for Storm911
Handles application state management and data persistence
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Optional, Any
from pathlib import Path

class StateManager:
    def __init__(self, app_dir: str = None):
        """Initialize State Manager"""
        self.app_dir = app_dir or os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.app_dir, 'data')
        self.state_file = os.path.join(self.data_dir, 'app_state.json')
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize state
        self.state = {
            'current_call': None,
            'api_credentials': None,
            'last_search': None,
            'recent_calls': [],
            'settings': self._get_default_settings()
        }
        
        # Load existing state
        self.load_state()
    
    def _get_default_settings(self) -> Dict:
        """Get default application settings"""
        return {
            'theme': 'dark',
            'font_size': 'normal',
            'auto_save': True,
            'confirm_dispositions': True,
            'max_recent_calls': 50,
            'pdf_export_dir': os.path.join(self.app_dir, 'EXPORTS'),
            'log_level': 'INFO',
            'api_timeout': 30,
            'last_updated': datetime.now().isoformat()
        }
    
    def load_state(self) -> None:
        """Load application state from file"""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    saved_state = json.load(f)
                    self.state.update(saved_state)
                logging.info("Application state loaded successfully")
        except Exception as e:
            logging.error(f"Error loading application state: {str(e)}")
    
    def save_state(self) -> bool:
        """Save current application state to file"""
        try:
            # Update last modified timestamp
            self.state['last_updated'] = datetime.now().isoformat()
            
            # Save state to file
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            
            logging.info("Application state saved successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error saving application state: {str(e)}")
            return False
    
    def get_current_call(self) -> Optional[Dict]:
        """Get current call data"""
        return self.state.get('current_call')
    
    def set_current_call(self, call_data: Dict) -> None:
        """Set current call data"""
        self.state['current_call'] = call_data
        self.save_state()
    
    def clear_current_call(self) -> None:
        """Clear current call data"""
        if self.state['current_call']:
            # Add to recent calls before clearing
            self.add_recent_call(self.state['current_call'])
            self.state['current_call'] = None
            self.save_state()
    
    def get_api_credentials(self) -> Optional[Dict]:
        """Get stored API credentials"""
        return self.state.get('api_credentials')
    
    def set_api_credentials(self, credentials: Dict) -> None:
        """Set API credentials"""
        self.state['api_credentials'] = credentials
        self.save_state()
    
    def clear_api_credentials(self) -> None:
        """Clear stored API credentials"""
        self.state['api_credentials'] = None
        self.save_state()
    
    def get_last_search(self) -> Optional[Dict]:
        """Get last search data"""
        return self.state.get('last_search')
    
    def set_last_search(self, search_data: Dict) -> None:
        """Set last search data"""
        self.state['last_search'] = search_data
        self.save_state()
    
    def get_recent_calls(self, limit: int = None) -> list:
        """Get list of recent calls"""
        calls = self.state.get('recent_calls', [])
        if limit:
            return calls[:limit]
        return calls
    
    def add_recent_call(self, call_data: Dict) -> None:
        """Add call to recent calls list"""
        # Add timestamp if not present
        if 'timestamp' not in call_data:
            call_data['timestamp'] = datetime.now().isoformat()
        
        # Add to beginning of list
        self.state['recent_calls'].insert(0, call_data)
        
        # Trim list if needed
        max_calls = self.get_setting('max_recent_calls')
        if len(self.state['recent_calls']) > max_calls:
            self.state['recent_calls'] = self.state['recent_calls'][:max_calls]
        
        self.save_state()
    
    def clear_recent_calls(self) -> None:
        """Clear recent calls list"""
        self.state['recent_calls'] = []
        self.save_state()
    
    def get_setting(self, key: str) -> Any:
        """Get specific setting value"""
        return self.state['settings'].get(key)
    
    def set_setting(self, key: str, value: Any) -> None:
        """Set specific setting value"""
        self.state['settings'][key] = value
        self.save_state()
    
    def reset_settings(self) -> None:
        """Reset settings to defaults"""
        self.state['settings'] = self._get_default_settings()
        self.save_state()
    
    def export_state(self, filepath: str) -> bool:
        """Export current state to file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.state, f, indent=2)
            return True
        except Exception as e:
            logging.error(f"Error exporting state: {str(e)}")
            return False
    
    def import_state(self, filepath: str) -> bool:
        """Import state from file"""
        try:
            with open(filepath, 'r') as f:
                imported_state = json.load(f)
                self.state.update(imported_state)
            self.save_state()
            return True
        except Exception as e:
            logging.error(f"Error importing state: {str(e)}")
            return False
    
    def get_call_history(self, phone: str) -> list:
        """Get call history for specific phone number"""
        return [
            call for call in self.state['recent_calls']
            if call.get('phone') == phone
        ]
    
    def get_statistics(self) -> Dict:
        """Get usage statistics"""
        total_calls = len(self.state['recent_calls'])
        
        # Count dispositions
        dispositions = {}
        for call in self.state['recent_calls']:
            disposition = call.get('disposition')
            if disposition:
                dispositions[disposition] = dispositions.get(disposition, 0) + 1
        
        # Calculate appointment rate
        appointments = dispositions.get('appointment_scheduled', 0)
        appointment_rate = (appointments / total_calls) if total_calls > 0 else 0
        
        return {
            'total_calls': total_calls,
            'dispositions': dispositions,
            'appointment_rate': appointment_rate,
            'last_updated': self.state['last_updated']
        }
    
    def cleanup_old_data(self, days: int = 30) -> None:
        """Remove data older than specified days"""
        try:
            cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            # Filter recent calls
            self.state['recent_calls'] = [
                call for call in self.state['recent_calls']
                if datetime.fromisoformat(call['timestamp']).timestamp() > cutoff
            ]
            
            self.save_state()
            logging.info(f"Cleaned up data older than {days} days")
            
        except Exception as e:
            logging.error(f"Error cleaning up old data: {str(e)}")
