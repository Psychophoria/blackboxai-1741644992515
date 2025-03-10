"""
State Manager for Storm911
Handles application state management and persistence
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

class StateManager:
    def __init__(self):
        """Initialize State Manager"""
        self.data_dir = "data"
        self.state_file = os.path.join(self.data_dir, "app_state.json")
        
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize state
        self.state = {
            "current_call": None,
            "recent_calls": [],
            "last_search": None,
            "last_export": None,
            "ui_state": {
                "current_page": 0,
                "panels": {
                    "caller_info": True,
                    "transcript": True,
                    "objections": True
                }
            },
            "session": {
                "start_time": datetime.now().isoformat(),
                "call_count": 0,
                "export_count": 0,
                "email_count": 0
            }
        }
        
        # Load saved state
        self.load_state()
    
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
        """Save current application state"""
        try:
            # Update session info
            self.state["session"]["last_save"] = datetime.now().isoformat()
            
            # Save to file
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
            
            logging.info("Application state saved successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error saving application state: {str(e)}")
            return False
    
    def get_current_call(self) -> Optional[Dict]:
        """Get current call data"""
        return self.state.get("current_call")
    
    def set_current_call(self, call_data: Dict) -> None:
        """Set current call data"""
        try:
            self.state["current_call"] = call_data
            self.state["session"]["call_count"] += 1
            
            # Add to recent calls
            if call_data:
                self.add_recent_call(call_data)
            
            self.save_state()
            
        except Exception as e:
            logging.error(f"Error setting current call: {str(e)}")
    
    def clear_current_call(self) -> None:
        """Clear current call data"""
        self.state["current_call"] = None
        self.save_state()
    
    def add_recent_call(self, call_data: Dict) -> None:
        """Add call to recent calls list"""
        try:
            # Add timestamp
            call_data["timestamp"] = datetime.now().isoformat()
            
            # Add to list
            self.state["recent_calls"].insert(0, call_data)
            
            # Keep only last 50 calls
            self.state["recent_calls"] = self.state["recent_calls"][:50]
            
            self.save_state()
            
        except Exception as e:
            logging.error(f"Error adding recent call: {str(e)}")
    
    def get_recent_calls(self) -> list:
        """Get list of recent calls"""
        return self.state.get("recent_calls", [])
    
    def set_last_search(self, search_data: Dict) -> None:
        """Set last search data"""
        self.state["last_search"] = search_data
        self.save_state()
    
    def get_last_search(self) -> Optional[Dict]:
        """Get last search data"""
        return self.state.get("last_search")
    
    def set_ui_state(self, key: str, value: Any) -> None:
        """Set UI state value"""
        try:
            self.state["ui_state"][key] = value
            self.save_state()
        except Exception as e:
            logging.error(f"Error setting UI state: {str(e)}")
    
    def get_ui_state(self, key: str, default: Any = None) -> Any:
        """Get UI state value"""
        return self.state["ui_state"].get(key, default)
    
    def increment_counter(self, counter_type: str) -> None:
        """Increment session counter"""
        try:
            if counter_type in ["call_count", "export_count", "email_count"]:
                self.state["session"][counter_type] += 1
                self.save_state()
        except Exception as e:
            logging.error(f"Error incrementing counter: {str(e)}")
    
    def get_session_stats(self) -> Dict:
        """Get current session statistics"""
        return self.state["session"]
    
    def reset_session(self) -> None:
        """Reset session statistics"""
        try:
            self.state["session"] = {
                "start_time": datetime.now().isoformat(),
                "call_count": 0,
                "export_count": 0,
                "email_count": 0
            }
            self.save_state()
        except Exception as e:
            logging.error(f"Error resetting session: {str(e)}")
    
    def clear_state(self) -> None:
        """Clear all application state"""
        try:
            self.state = {
                "current_call": None,
                "recent_calls": [],
                "last_search": None,
                "last_export": None,
                "ui_state": {
                    "current_page": 0,
                    "panels": {
                        "caller_info": True,
                        "transcript": True,
                        "objections": True
                    }
                },
                "session": {
                    "start_time": datetime.now().isoformat(),
                    "call_count": 0,
                    "export_count": 0,
                    "email_count": 0
                }
            }
            self.save_state()
        except Exception as e:
            logging.error(f"Error clearing state: {str(e)}")
