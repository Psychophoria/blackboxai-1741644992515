"""
Event Logger for Storm911
Handles application event logging and tracking
"""

import os
import logging
import json
from datetime import datetime
from typing import Dict, Optional, Any
from pathlib import Path

class EventLogger:
    def __init__(self, app_dir: str = None):
        """Initialize Event Logger"""
        self.app_dir = app_dir or os.path.dirname(os.path.abspath(__file__))
        self.logs_dir = os.path.join(self.app_dir, 'logs')
        
        # Ensure logs directory exists
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Set up logging configuration
        self._setup_logging()
        
        # Initialize event categories
        self.categories = {
            'user': self._log_user_event,
            'system': self._log_system_event,
            'api': self._log_api_event,
            'error': self._log_error_event,
            'security': self._log_security_event,
            'call': self._log_call_event
        }
    
    def _setup_logging(self) -> None:
        """Set up logging configuration"""
        # Main application log
        main_handler = logging.FileHandler(
            os.path.join(self.logs_dir, 'storm911.log')
        )
        main_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        
        # Error log
        error_handler = logging.FileHandler(
            os.path.join(self.logs_dir, 'errors.log')
        )
        error_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s\n%(exc_info)s')
        )
        error_handler.setLevel(logging.ERROR)
        
        # API log
        api_handler = logging.FileHandler(
            os.path.join(self.logs_dir, 'api.log')
        )
        api_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(message)s')
        )
        
        # Security log
        security_handler = logging.FileHandler(
            os.path.join(self.logs_dir, 'security.log')
        )
        security_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        )
        
        # Call log
        call_handler = logging.FileHandler(
            os.path.join(self.logs_dir, 'calls.log')
        )
        call_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(message)s')
        )
        
        # Configure loggers
        logging.getLogger('main').addHandler(main_handler)
        logging.getLogger('error').addHandler(error_handler)
        logging.getLogger('api').addHandler(api_handler)
        logging.getLogger('security').addHandler(security_handler)
        logging.getLogger('call').addHandler(call_handler)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()
    
    def _sanitize_data(self, data: Dict) -> Dict:
        """Remove sensitive information from log data"""
        sensitive_fields = ['password', 'api_key', 'token', 'ssn', 'credit_card']
        sanitized = data.copy()
        
        for field in sensitive_fields:
            if field in sanitized:
                sanitized[field] = '********'
        
        return sanitized
    
    def _log_user_event(self, event_type: str, details: Dict) -> None:
        """Log user event"""
        logger = logging.getLogger('main')
        sanitized_details = self._sanitize_data(details)
        logger.info(f"USER EVENT - {event_type}: {json.dumps(sanitized_details)}")
    
    def _log_system_event(self, event_type: str, details: Dict) -> None:
        """Log system event"""
        logger = logging.getLogger('main')
        logger.info(f"SYSTEM EVENT - {event_type}: {json.dumps(details)}")
    
    def _log_api_event(self, event_type: str, details: Dict) -> None:
        """Log API event"""
        logger = logging.getLogger('api')
        sanitized_details = self._sanitize_data(details)
        logger.info(f"API EVENT - {event_type}: {json.dumps(sanitized_details)}")
    
    def _log_error_event(self, event_type: str, details: Dict) -> None:
        """Log error event"""
        logger = logging.getLogger('error')
        logger.error(f"ERROR EVENT - {event_type}: {json.dumps(details)}")
    
    def _log_security_event(self, event_type: str, details: Dict) -> None:
        """Log security event"""
        logger = logging.getLogger('security')
        sanitized_details = self._sanitize_data(details)
        logger.info(f"SECURITY EVENT - {event_type}: {json.dumps(sanitized_details)}")
    
    def _log_call_event(self, event_type: str, details: Dict) -> None:
        """Log call event"""
        logger = logging.getLogger('call')
        sanitized_details = self._sanitize_data(details)
        logger.info(f"CALL EVENT - {event_type}: {json.dumps(sanitized_details)}")
    
    def log_event(self, category: str, event_type: str, details: Dict) -> None:
        """Log an event"""
        if category in self.categories:
            try:
                # Add timestamp to details
                details['timestamp'] = self._get_timestamp()
                
                # Log the event
                self.categories[category](event_type, details)
                
            except Exception as e:
                # Log error in main log
                logging.getLogger('main').error(
                    f"Error logging {category} event: {str(e)}"
                )
        else:
            logging.getLogger('main').error(f"Invalid event category: {category}")
    
    def get_recent_events(
        self,
        category: str = None,
        limit: int = 100
    ) -> list:
        """Get recent events from log"""
        events = []
        
        try:
            # Determine which log file to read
            if category == 'error':
                log_file = os.path.join(self.logs_dir, 'errors.log')
            elif category == 'api':
                log_file = os.path.join(self.logs_dir, 'api.log')
            elif category == 'security':
                log_file = os.path.join(self.logs_dir, 'security.log')
            elif category == 'call':
                log_file = os.path.join(self.logs_dir, 'calls.log')
            else:
                log_file = os.path.join(self.logs_dir, 'storm911.log')
            
            # Read events from log file
            with open(log_file, 'r') as f:
                lines = f.readlines()[-limit:]
                events = [line.strip() for line in lines]
            
            return events
            
        except Exception as e:
            logging.getLogger('main').error(
                f"Error reading events from log: {str(e)}"
            )
            return []
    
    def clear_logs(self, category: str = None) -> bool:
        """Clear log files"""
        try:
            if category:
                # Clear specific log file
                log_file = os.path.join(self.logs_dir, f'{category}.log')
                if os.path.exists(log_file):
                    with open(log_file, 'w') as f:
                        f.write('')
            else:
                # Clear all log files
                for file in os.listdir(self.logs_dir):
                    if file.endswith('.log'):
                        with open(os.path.join(self.logs_dir, file), 'w') as f:
                            f.write('')
            
            return True
            
        except Exception as e:
            logging.getLogger('main').error(f"Error clearing logs: {str(e)}")
            return False
    
    def archive_logs(self, days: int = 30) -> bool:
        """Archive logs older than specified days"""
        try:
            archive_dir = os.path.join(self.logs_dir, 'archive')
            os.makedirs(archive_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_file = os.path.join(
                archive_dir,
                f'logs_archive_{timestamp}.zip'
            )
            
            # Create archive
            import zipfile
            with zipfile.ZipFile(archive_file, 'w') as zipf:
                for file in os.listdir(self.logs_dir):
                    if file.endswith('.log'):
                        file_path = os.path.join(self.logs_dir, file)
                        zipf.write(file_path, file)
            
            # Clear current logs
            self.clear_logs()
            
            return True
            
        except Exception as e:
            logging.getLogger('main').error(f"Error archiving logs: {str(e)}")
            return False
