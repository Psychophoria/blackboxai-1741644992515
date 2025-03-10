"""
Settings Manager for Storm911
Handles application settings, preferences, and configuration
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path

class SettingsManager:
    def __init__(self, app_dir: str = None):
        """Initialize Settings Manager"""
        self.app_dir = app_dir or os.path.dirname(os.path.abspath(__file__))
        self.settings_file = os.path.join(self.app_dir, 'data', 'settings.json')
        
        # Ensure settings directory exists
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        
        # Default settings
        self.default_settings = {
            "appearance": {
                "theme": "dark",
                "font_size": "normal",
                "font_family": "Arial",
                "window_size": "1600x900",
                "show_toolbar": True,
                "show_statusbar": True
            },
            "behavior": {
                "auto_save": True,
                "confirm_exit": True,
                "confirm_dispositions": True,
                "show_tooltips": True,
                "enable_hotkeys": True
            },
            "notifications": {
                "enable_sound": True,
                "enable_popup": True,
                "sound_volume": 50,
                "notification_duration": 5
            },
            "api": {
                "timeout": 30,
                "retry_attempts": 3,
                "cache_duration": 300
            },
            "export": {
                "pdf_directory": "EXPORTS",
                "auto_email": True,
                "include_timestamp": True,
                "default_format": "pdf"
            },
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "use_tls": True,
                "sender_name": "Storm911",
                "signature": True
            },
            "logging": {
                "level": "INFO",
                "max_file_size": 10485760,  # 10MB
                "backup_count": 5,
                "log_api_calls": True
            },
            "security": {
                "session_timeout": 3600,  # 1 hour
                "max_login_attempts": 3,
                "password_expiry": 90,  # days
                "require_2fa": False
            },
            "performance": {
                "cache_size": 100,
                "max_recent_calls": 50,
                "cleanup_interval": 86400,  # 24 hours
                "max_export_size": 52428800  # 50MB
            }
        }
        
        # Load or create settings
        self.settings = self.load_settings()
    
    def load_settings(self) -> Dict:
        """Load settings from file or create with defaults"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    # Update with any new default settings
                    return self._update_settings_with_defaults(settings)
            return self.default_settings.copy()
            
        except Exception as e:
            logging.error(f"Error loading settings: {str(e)}")
            return self.default_settings.copy()
    
    def save_settings(self) -> bool:
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
            
        except Exception as e:
            logging.error(f"Error saving settings: {str(e)}")
            return False
    
    def get_setting(self, category: str, key: str) -> Any:
        """Get specific setting value"""
        try:
            return self.settings[category][key]
        except KeyError:
            # Return default if exists
            return self.default_settings.get(category, {}).get(key)
    
    def set_setting(self, category: str, key: str, value: Any) -> bool:
        """Set specific setting value"""
        try:
            if category not in self.settings:
                self.settings[category] = {}
            self.settings[category][key] = value
            return self.save_settings()
            
        except Exception as e:
            logging.error(f"Error setting {category}.{key}: {str(e)}")
            return False
    
    def reset_category(self, category: str) -> bool:
        """Reset category to default settings"""
        try:
            if category in self.default_settings:
                self.settings[category] = self.default_settings[category].copy()
                return self.save_settings()
            return False
            
        except Exception as e:
            logging.error(f"Error resetting category {category}: {str(e)}")
            return False
    
    def reset_all(self) -> bool:
        """Reset all settings to defaults"""
        try:
            self.settings = self.default_settings.copy()
            return self.save_settings()
            
        except Exception as e:
            logging.error(f"Error resetting all settings: {str(e)}")
            return False
    
    def _update_settings_with_defaults(self, settings: Dict) -> Dict:
        """Update existing settings with any new default settings"""
        updated = settings.copy()
        
        for category, values in self.default_settings.items():
            if category not in updated:
                updated[category] = values
            else:
                for key, value in values.items():
                    if key not in updated[category]:
                        updated[category][key] = value
        
        return updated
    
    def export_settings(self, filepath: str) -> bool:
        """Export settings to file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.settings, f, indent=2)
            return True
            
        except Exception as e:
            logging.error(f"Error exporting settings: {str(e)}")
            return False
    
    def import_settings(self, filepath: str) -> bool:
        """Import settings from file"""
        try:
            with open(filepath, 'r') as f:
                imported = json.load(f)
                # Validate and update with defaults
                self.settings = self._update_settings_with_defaults(imported)
                return self.save_settings()
                
        except Exception as e:
            logging.error(f"Error importing settings: {str(e)}")
            return False
    
    def get_all_settings(self) -> Dict:
        """Get all current settings"""
        return self.settings.copy()
    
    def validate_settings(self) -> Dict[str, list]:
        """Validate current settings and return any issues"""
        issues = {}
        
        try:
            # Validate window size
            window_size = self.settings["appearance"]["window_size"]
            if not isinstance(window_size, str) or "x" not in window_size:
                if "appearance" not in issues:
                    issues["appearance"] = []
                issues["appearance"].append("Invalid window size format")
            
            # Validate numeric values
            if self.settings["notifications"]["sound_volume"] not in range(101):
                if "notifications" not in issues:
                    issues["notifications"] = []
                issues["notifications"].append("Sound volume must be 0-100")
            
            # Validate timeouts and intervals
            if self.settings["security"]["session_timeout"] < 300:
                if "security" not in issues:
                    issues["security"] = []
                issues["security"].append("Session timeout too short")
            
            # Validate email settings
            if self.settings["email"]["smtp_port"] not in [25, 465, 587]:
                if "email" not in issues:
                    issues["email"] = []
                issues["email"].append("Invalid SMTP port")
            
        except Exception as e:
            logging.error(f"Error validating settings: {str(e)}")
            issues["general"] = ["Error validating settings"]
        
        return issues
    
    def apply_settings(self) -> bool:
        """Apply current settings to application"""
        try:
            # Validate settings first
            issues = self.validate_settings()
            if issues:
                logging.error(f"Settings validation failed: {issues}")
                return False
            
            # Apply logging settings
            log_level = self.settings["logging"]["level"]
            logging.getLogger().setLevel(log_level)
            
            # Save settings
            return self.save_settings()
            
        except Exception as e:
            logging.error(f"Error applying settings: {str(e)}")
            return False
