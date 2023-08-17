import re

from django.core.exceptions import ValidationError


def nepali_date_validator(value):
    """function to check if nepali date is in YYYY-MM-DD format"""
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if not pattern.match(value):
        raise ValidationError('Invalid Nepali date format. Use YYYY-MM-DD format.')
    