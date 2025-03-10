"""
Configuration settings for Storm911 application
"""

import os
from pathlib import Path

# Application Information
APP_NAME = "Storm911"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Storm911"

# Directory Structure
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
EXPORTS_DIR = BASE_DIR / "EXPORTS"
LOGS_DIR = BASE_DIR / "logs"

# Ensure required directories exist
for directory in [ASSETS_DIR, EXPORTS_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# Window Settings
WINDOW_SIZE = "1600x900"
WINDOW_MIN_SIZE = (1200, 700)
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"

# Color Theme
COLORS = {
    "primary": "#007bff",
    "secondary": "#6c757d",
    "success": "#28a745",
    "danger": "#dc3545",
    "warning": "#ffc107",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40"
}

# Font Settings
FONTS = {
    "title": ("Arial", 24, "bold"),
    "subtitle": ("Arial", 18, "bold"),
    "heading": ("Arial", 16, "bold"),
    "subheading": ("Arial", 14, "bold"),
    "normal": ("Arial", 12),
    "small": ("Arial", 10)
}

# API Settings
API_BASE_URL = "https://roofingappointments.readymode.com/TPI"
API_ENDPOINTS = {
    "search_lead": "/search/Lead/{phone}",
    "update_lead": "/update/Lead/{id}",
    "create_lead": "/create/Lead"
}

# Email Settings
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": os.getenv("STORM911_EMAIL", ""),
    "sender_password": os.getenv("STORM911_EMAIL_PASSWORD", ""),
    "reply_to": "support@storm911.com",
    "support_email": "support@storm911.com"
}

# PDF Settings
PDF_CONFIG = {
    "page_size": "letter",
    "margins": {
        "top": 72,
        "bottom": 72,
        "left": 72,
        "right": 72
    },
    "font_size": {
        "title": 24,
        "heading": 16,
        "subheading": 14,
        "normal": 12,
        "small": 10
    }
}

# Logging Configuration
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "storm911.log",
            "formatter": "standard",
            "level": "INFO",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "INFO",
        }
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True
        }
    }
}

# Form Field Validation
VALIDATION = {
    "phone": {
        "pattern": r"^\+?1?\d{9,15}$",
        "message": "Please enter a valid phone number"
    },
    "email": {
        "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "message": "Please enter a valid email address"
    },
    "zip": {
        "pattern": r"^\d{5}(-\d{4})?$",
        "message": "Please enter a valid ZIP code"
    }
}

# Default Values
DEFAULTS = {
    "state": "Select State",
    "stories": "Select Stories",
    "roof_age": "Select Roof Age",
    "roof_type": "Select Roof Type"
}

# Dropdown Options
OPTIONS = {
    "states": [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    ],
    "stories": [
        "1 Story",
        "1.5 Stories",
        "2 Stories",
        "2.5 Stories",
        "3+ Stories"
    ],
    "roof_age": [
        "0-5 Years",
        "6-10 Years",
        "11-15 Years",
        "16-20 Years",
        "20+ Years",
        "Unknown"
    ],
    "roof_type": [
        "Asphalt Shingles",
        "Metal",
        "Tile",
        "Wood Shake",
        "Slate",
        "Other"
    ],
    "appointment_times": [
        "9:00 AM",
        "10:00 AM",
        "11:00 AM",
        "12:00 PM",
        "1:00 PM",
        "2:00 PM",
        "3:00 PM",
        "4:00 PM",
        "5:00 PM",
        "6:00 PM",
        "7:00 PM"
    ]
}

# Error Messages
ERRORS = {
    "api": {
        "connection": "Could not connect to the API. Please check your internet connection.",
        "authentication": "Invalid API credentials. Please check your username and password.",
        "not_found": "No data found for the provided phone number.",
        "server": "Server error occurred. Please try again later."
    },
    "validation": {
        "required": "This field is required.",
        "invalid_format": "Invalid format.",
        "future_date": "Date must be in the future.",
        "business_hours": "Time must be during business hours (9 AM - 7 PM)."
    },
    "email": {
        "send_failed": "Failed to send email. Please try again later.",
        "invalid_recipient": "Invalid recipient email address.",
        "attachment_failed": "Failed to attach file to email."
    },
    "pdf": {
        "generation_failed": "Failed to generate PDF. Please try again.",
        "file_access": "Could not access the PDF file.",
        "invalid_data": "Invalid data for PDF generation."
    }
}

# Success Messages
SUCCESS = {
    "appointment": "Appointment scheduled successfully!",
    "email_sent": "Email sent successfully!",
    "pdf_generated": "PDF generated successfully!",
    "data_saved": "Data saved successfully!"
}
