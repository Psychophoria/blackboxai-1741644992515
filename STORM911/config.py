"""
Configuration Settings for Storm911
Contains all application constants and settings
"""

import os
from pathlib import Path

# Application Information
APP_NAME = "Storm911"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Storm911 Development Team"

# Directory Paths
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
EXPORTS_DIR = os.path.join(BASE_DIR, 'EXPORTS')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Asset Paths
LOGO_PATH = os.path.join(ASSETS_DIR, 'images', 'logos', 'storm911.png')
ICONS_DIR = os.path.join(ASSETS_DIR, 'images', 'icons')
TEMPLATES_DIR = os.path.join(ASSETS_DIR, 'templates')
FONTS_DIR = os.path.join(ASSETS_DIR, 'fonts')

# Window Settings
WINDOW_SIZE = "1600x900"
MIN_WINDOW_SIZE = "1200x800"
DEFAULT_PADDING = 10

# Theme Settings
DEFAULT_THEME = "dark"
DEFAULT_FONT_SIZE = "normal"
DEFAULT_FONT_FAMILY = "Arial"

# API Settings
API_BASE_URL = "https://api.readymode.com/v1"
API_TIMEOUT = 30  # seconds
API_RETRY_ATTEMPTS = 3
API_CACHE_DURATION = 300  # seconds

# Email Settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USE_TLS = True
DEFAULT_SENDER = "noreply@storm911.com"
EMAIL_TEMPLATE_DIR = os.path.join(TEMPLATES_DIR, 'email')

# PDF Settings
PDF_TEMPLATE_DIR = os.path.join(TEMPLATES_DIR, 'pdf')
PDF_FONT_DIR = FONTS_DIR
DEFAULT_PDF_FORMAT = "Letter"
PDF_MARGIN = 72  # points (1 inch)

# Logging Settings
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_LOG_SIZE = 10485760  # 10MB
LOG_BACKUP_COUNT = 5

# Security Settings
SESSION_TIMEOUT = 3600  # 1 hour
MAX_LOGIN_ATTEMPTS = 3
PASSWORD_MIN_LENGTH = 8
REQUIRE_2FA = False

# Cache Settings
CACHE_DIR = os.path.join(DATA_DIR, 'cache')
MAX_CACHE_SIZE = 104857600  # 100MB
CACHE_CLEANUP_INTERVAL = 86400  # 24 hours

# Performance Settings
MAX_RECENT_CALLS = 50
AUTO_SAVE_INTERVAL = 300  # 5 minutes
CLEANUP_INTERVAL = 86400  # 24 hours

# Feature Flags
ENABLE_API_CACHE = True
ENABLE_EMAIL = True
ENABLE_PDF_EXPORT = True
ENABLE_AUTO_SAVE = True
ENABLE_ANALYTICS = True

# Development Settings
DEBUG = False
TESTING = False
PROFILE = False

try:
    from local_settings import *
except ImportError:
    pass

# Ensure required directories exist
for directory in [ASSETS_DIR, EXPORTS_DIR, LOGS_DIR, DATA_DIR, CACHE_DIR]:
    os.makedirs(directory, exist_ok=True)
