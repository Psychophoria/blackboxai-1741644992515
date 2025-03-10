"""
Event Logger for Storm911
Handles application event logging and tracking
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

class EventLogger:
    def __init__(self):
        """Initialize Event Logger"""
        self.logs_dir = "logs"
        self.events_file = os.path.join(self.logs_dir, "events.log")
        self.error_file = os.path.join(self.logs_dir, "error.log")
        self.security_file = os.path.join(self.logs_dir, "security.log")
        
        # Ensure logs directory exists
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Configure logging
        self._setup_logging()
        
        # Initialize event counters
        self.event_counts = {
            "user": 0,
            "system": 0,
            "error": 0,
            "security": 0
        }
    
    def _setup_logging(self) -> None:
        """Set up logging configuration"""
        try:
            # Main logger
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            # Events logger
            events_handler = logging.FileHandler(self.events_file)
            events_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(message)s')
            )
            self.events_logger = logging.getLogger('events')
            self.events_logger.addHandler(events_handler)
            self.events_logger.setLevel(logging.INFO)
            
            # Error logger
            error_handler = logging.FileHandler(self.error_file)
            error_handler.setFormatter(
                logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            )
            self.error_logger = logging.getLogger('error')
            self.error_logger.addHandler(error_handler)
            self.error_logger.setLevel(logging.ERROR)
            
            # Security logger
            security_handler = logging.FileHandler(self.security_file)
            security_handler.setFormatter(
                logging.Formatter('%(asctime)s - SECURITY - %(message)s')
            )
            self.security_logger = logging.getLogger('security')
            self.security_logger.addHandler(security_handler)
            self.security_logger.setLevel(logging.INFO)
            
        except Exception as e:
            print(f"Error setting up logging: {str(e)}")
    
    def log_event(
        self,
        category: str,
        event_type: str,
        data: Optional[Dict] = None
    ) -> None:
        """Log an application event"""
        try:
            # Create event data
            event = {
                "timestamp": datetime.now().isoformat(),
                "category": category,
                "type": event_type,
                "data": data or {}
            }
            
            # Log based on category
            if category == "error":
                self.error_logger.error(json.dumps(event))
                self.event_counts["error"] += 1
            elif category == "security":
                self.security_logger.info(json.dumps(event))
                self.event_counts["security"] += 1
            elif category == "user":
                self.events_logger.info(json.dumps(event))
                self.event_counts["user"] += 1
            else:  # system events
                self.events_logger.info(json.dumps(event))
                self.event_counts["system"] += 1
            
        except Exception as e:
            print(f"Error logging event: {str(e)}")
    
    def log_error(
        self,
        error: Exception,
        context: Optional[Dict] = None
    ) -> None:
        """Log an error with context"""
        try:
            error_data = {
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context or {}
            }
            self.log_event("error", "exception", error_data)
            
        except Exception as e:
            print(f"Error logging error: {str(e)}")
    
    def log_security_event(
        self,
        event_type: str,
        details: Dict
    ) -> None:
        """Log a security-related event"""
        try:
            self.log_event("security", event_type, details)
            
        except Exception as e:
            print(f"Error logging security event: {str(e)}")
    
    def get_event_counts(self) -> Dict[str, int]:
        """Get current event counts"""
        return self.event_counts.copy()
    
    def clear_logs(self) -> bool:
        """Clear all log files"""
        try:
            # Clear each log file
            open(self.events_file, 'w').close()
            open(self.error_file, 'w').close()
            open(self.security_file, 'w').close()
            
            # Reset counters
            self.event_counts = {
                "user": 0,
                "system": 0,
                "error": 0,
                "security": 0
            }
            
            return True
            
        except Exception as e:
            print(f"Error clearing logs: {str(e)}")
            return False
    
    def get_recent_events(
        self,
        category: Optional[str] = None,
        limit: int = 100
    ) -> list:
        """Get recent events from log"""
        events = []
        try:
            # Read appropriate log file
            if category == "error":
                log_file = self.error_file
            elif category == "security":
                log_file = self.security_file
            else:
                log_file = self.events_file
            
            # Read events
            with open(log_file, 'r') as f:
                lines = f.readlines()[-limit:]
                for line in lines:
                    try:
                        # Extract JSON part
                        json_str = line.split(" - ")[-1]
                        event = json.loads(json_str)
                        if not category or event.get("category") == category:
                            events.append(event)
                    except:
                        continue
            
        except Exception as e:
            print(f"Error getting recent events: {str(e)}")
        
        return events
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of recent errors"""
        try:
            errors = self.get_recent_events("error")
            
            # Count errors by type
            error_types = {}
            for error in errors:
                error_type = error.get("data", {}).get("error_type", "unknown")
                error_types[error_type] = error_types.get(error_type, 0) + 1
            
            return {
                "total_errors": len(errors),
                "error_types": error_types,
                "most_recent": errors[-1] if errors else None
            }
            
        except Exception as e:
            print(f"Error getting error summary: {str(e)}")
            return {
                "total_errors": 0,
                "error_types": {},
                "most_recent": None
            }
    
    def archive_old_logs(self, days: int = 30) -> bool:
        """Archive logs older than specified days"""
        try:
            # Create archive directory
            archive_dir = os.path.join(self.logs_dir, "archive")
            os.makedirs(archive_dir, exist_ok=True)
            
            # Get current timestamp
            now = datetime.now()
            
            # Archive each log file if old enough
            for log_file in [self.events_file, self.error_file, self.security_file]:
                if os.path.exists(log_file):
                    # Check file age
                    mtime = datetime.fromtimestamp(os.path.getmtime(log_file))
                    age = (now - mtime).days
                    
                    if age >= days:
                        # Create archive filename
                        base_name = os.path.basename(log_file)
                        archive_name = f"{base_name}.{mtime.strftime('%Y%m%d')}"
                        archive_path = os.path.join(archive_dir, archive_name)
                        
                        # Move file to archive
                        os.rename(log_file, archive_path)
                        
                        # Create new empty log file
                        open(log_file, 'w').close()
            
            return True
            
        except Exception as e:
            print(f"Error archiving logs: {str(e)}")
            return False
