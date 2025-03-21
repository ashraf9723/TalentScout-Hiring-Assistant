"""
This module contains utility functions for the TalentScout hiring assistant.
"""
import re

def is_valid_email(email):
    """Check if an email is valid."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def is_valid_phone(phone):
    """Check if a phone number is valid."""
    # Basic validation - checks for 10+ digits
    pattern = r'^\+?[\d\s\(\)\-\.]{10,}$'
    return bool(re.match(pattern, phone))

def sanitize_input(text):
    """Sanitize user input to prevent injection attacks."""
    # Basic sanitization - remove HTML tags
    sanitized = re.sub(r'<[^>]*>', '', text)
    return sanitized

def format_candidate_info(info_dict):
    """Format candidate information for display."""
    formatted = ""
    for key, value in info_dict.items():
        if value:
            # Convert snake_case to Title Case
            display_key = key.replace("_", " ").title()
            formatted += f"**{display_key}**: {value}\n"
    return formatted