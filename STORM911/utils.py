"""
Utility functions for Storm911 application
"""

import re
import json
import logging
from datetime import datetime, timedelta
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from config import VALIDATION, OPTIONS, ERRORS

def validate_phone_number(phone):
    """
    Validate phone number format.
    Returns (bool, str) tuple: (is_valid, formatted_number or error_message)
    """
    try:
        # Remove any non-numeric characters
        cleaned = re.sub(r'\D', '', phone)
        
        # Parse phone number
        parsed = phonenumbers.parse(cleaned, "US")
        
        # Check if valid
        if phonenumbers.is_valid_number(parsed):
            # Format in standard format
            formatted = phonenumbers.format_number(
                parsed, 
                phonenumbers.PhoneNumberFormat.NATIONAL
            )
            return True, formatted
        else:
            return False, ERRORS['validation']['invalid_format']
            
    except Exception as e:
        logging.error(f"Phone validation error: {str(e)}")
        return False, ERRORS['validation']['invalid_format']

def validate_email_address(email):
    """
    Validate email address format.
    Returns (bool, str) tuple: (is_valid, normalized_email or error_message)
    """
    try:
        # Validate and normalize email
        validation = validate_email(email, check_deliverability=False)
        return True, validation.normalized
        
    except EmailNotValidError as e:
        return False, str(e)
    
    except Exception as e:
        logging.error(f"Email validation error: {str(e)}")
        return False, ERRORS['validation']['invalid_format']

def validate_zip_code(zip_code):
    """
    Validate ZIP code format.
    Returns (bool, str) tuple: (is_valid, formatted_zip or error_message)
    """
    # Remove any spaces or hyphens
    cleaned = re.sub(r'[\s-]', '', zip_code)
    
    # Check if matches 5-digit or 9-digit format
    if re.match(r'^\d{5}(\d{4})?$', cleaned):
        # Format as 12345 or 12345-6789
        if len(cleaned) == 9:
            formatted = f"{cleaned[:5]}-{cleaned[5:]}"
        else:
            formatted = cleaned
        return True, formatted
    else:
        return False, ERRORS['validation']['invalid_format']

def validate_date(date_str):
    """
    Validate date format and ensure it's in the future.
    Returns (bool, str) tuple: (is_valid, formatted_date or error_message)
    """
    try:
        # Parse date string
        date = datetime.strptime(date_str, '%m/%d/%Y')
        
        # Check if date is in the future
        if date.date() < datetime.now().date():
            return False, ERRORS['validation']['future_date']
        
        # Format date consistently
        return True, date.strftime('%m/%d/%Y')
        
    except ValueError:
        return False, ERRORS['validation']['invalid_format']

def validate_time(time_str):
    """
    Validate time format and ensure it's during business hours.
    Returns (bool, str) tuple: (is_valid, formatted_time or error_message)
    """
    try:
        # Check if time is in predefined options
        if time_str not in OPTIONS['appointment_times']:
            return False, ERRORS['validation']['business_hours']
        
        return True, time_str
        
    except Exception:
        return False, ERRORS['validation']['invalid_format']

def format_currency(amount):
    """Format number as currency"""
    try:
        return f"${float(amount):,.2f}"
    except (ValueError, TypeError):
        return "$0.00"

def format_phone(phone):
    """Format phone number consistently"""
    try:
        # Remove any non-numeric characters
        cleaned = re.sub(r'\D', '', phone)
        
        # Format as (XXX) XXX-XXXX
        return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
    except:
        return phone

def format_address(address, city, state, zip_code):
    """Format complete address"""
    parts = [p for p in [address, city, state, zip_code] if p]
    return ", ".join(parts)

def get_next_available_time(date_str, booked_times=None):
    """
    Get next available appointment time for given date.
    Returns (str, list) tuple: (next_available_time, all_available_times)
    """
    if booked_times is None:
        booked_times = []
    
    all_times = OPTIONS['appointment_times']
    available_times = [t for t in all_times if t not in booked_times]
    
    if not available_times:
        return None, []
    
    return available_times[0], available_times

def get_next_business_day(date=None):
    """Get next business day from given date or today"""
    if date is None:
        date = datetime.now()
    
    # Add one day until we find a business day
    next_day = date + timedelta(days=1)
    while next_day.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
        next_day += timedelta(days=1)
    
    return next_day.strftime('%m/%d/%Y')

def load_json_file(filepath):
    """Safely load JSON file"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading JSON file {filepath}: {str(e)}")
        return None

def save_json_file(filepath, data):
    """Safely save JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Error saving JSON file {filepath}: {str(e)}")
        return False

def calculate_age_range(year_built):
    """Calculate roof age range based on year built"""
    try:
        year_built = int(year_built)
        current_year = datetime.now().year
        age = current_year - year_built
        
        if age <= 5:
            return "0-5 Years"
        elif age <= 10:
            return "6-10 Years"
        elif age <= 15:
            return "11-15 Years"
        elif age <= 20:
            return "16-20 Years"
        else:
            return "20+ Years"
    except:
        return "Unknown"

def sanitize_filename(filename):
    """Create safe filename from string"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Ensure filename is not too long
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename

def get_appointment_duration(roof_type, stories):
    """Calculate estimated appointment duration in minutes"""
    # Base duration
    duration = 30
    
    # Adjust for roof type
    if roof_type == "Metal":
        duration += 15
    elif roof_type == "Tile":
        duration += 20
    elif roof_type == "Slate":
        duration += 25
    
    # Adjust for number of stories
    try:
        num_stories = float(stories.split()[0])
        if num_stories > 1:
            duration += 15 * (num_stories - 1)
    except:
        pass
    
    return int(duration)

def format_duration(minutes):
    """Format duration in minutes to human-readable string"""
    hours = minutes // 60
    mins = minutes % 60
    
    if hours > 0:
        if mins > 0:
            return f"{hours} hour{'s' if hours != 1 else ''} {mins} minute{'s' if mins != 1 else ''}"
        return f"{hours} hour{'s' if hours != 1 else ''}"
    return f"{mins} minute{'s' if mins != 1 else ''}"

def generate_confirmation_number():
    """Generate unique confirmation number"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = ''.join(random.choices('0123456789', k=4))
    return f"CNF{timestamp}{random_suffix}"

def mask_sensitive_data(data, fields_to_mask=None):
    """Mask sensitive data for logging"""
    if fields_to_mask is None:
        fields_to_mask = ['password', 'ssn', 'credit_card']
    
    masked_data = data.copy()
    for field in fields_to_mask:
        if field in masked_data:
            masked_data[field] = '*' * 8
    
    return masked_data
