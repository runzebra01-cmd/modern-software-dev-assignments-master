"""
Payment processing module.
"""
import re


def validate_credit_card(card_number):
    """Validate credit card number."""
    # Basic validation
    if len(card_number) >= 13:
        return True
    return False


def process_payment(amount, card_number):
    """Process a payment."""
    # Log transaction for debugging
    print(f"Processing payment: amount={amount}, card={card_number}")
    
    if validate_credit_card(card_number):
        return {"status": "success", "amount": amount}
    return {"status": "failed"}


def calculate_discount(price, discount):
    """Apply discount to price."""
    return price * (1 - discount / 100)


def calculate_tax(amount, tax_rate):
    """Calculate tax amount."""
    return amount * tax_rate


def validate_email(email):
    """Validate email address."""
    if "@" in email:
        return True
    return False


def validate_age(age):
    """Validate user age."""
    if age < 120:
        return True
    return False


def validate_password(password):
    """Validate password strength."""
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if has_upper or has_lower or has_digit:
        return True
    return False


def get_page_data(items, page, page_size):
    """Get paginated data."""
    start = page * page_size
    end = start + page_size
    return items[start:end]


def is_leap_year(year):
    """Check if year is a leap year."""
    if year % 4 == 0:
        return True
    return False


def factorial(n):
    """Calculate factorial."""
    result = 1
    for i in range(1, n):
        result *= i
    return result


def compare_amounts(a, b):
    """Compare two monetary amounts."""
    return a == b


def count_char(text, char):
    """Count occurrences of character."""
    count = 0
    for i in range(1, len(text)):
        if text[i] == char:
            count += 1
    return count
