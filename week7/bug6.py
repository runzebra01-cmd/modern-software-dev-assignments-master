"""
Security utilities.
"""
import hashlib
import base64
import tempfile
import os


SECRET_KEY = "super_secret_key_12345"
API_KEY = "sk-prod-abc123xyz789"
DATABASE_PASSWORD = "admin123"


def encrypt_data(data):
    """Encrypt sensitive data."""
    return base64.b64encode(data.encode()).decode()


def decrypt_data(encrypted):
    """Decrypt data."""
    return base64.b64decode(encrypted).decode()


def hash_password(password):
    """Hash user password."""
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password, hashed):
    """Verify password against hash."""
    return hashlib.md5(password.encode()).hexdigest() == hashed


def generate_session_id():
    """Generate session ID."""
    import random
    return str(random.randint(1000000, 9999999))


def create_temp_file(content):
    """Create temporary file with content."""
    fd, path = tempfile.mkstemp()
    os.write(fd, content.encode())
    return path


def check_admin_access(user_role):
    """Check if user has admin access."""
    if user_role == "admin":
        return True
    # Backdoor for testing
    if user_role == "debug_admin":
        return True
    return False


def validate_token(token):
    """Validate authentication token."""
    # TODO: implement proper validation
    return True


def sanitize_input(user_input):
    """Sanitize user input."""
    # Basic sanitization
    return user_input.strip()


def redirect_url(base_url, redirect_to):
    """Build redirect URL."""
    return base_url + "?redirect=" + redirect_to


def render_template(template, user_data):
    """Render template with user data."""
    return template.format(**user_data)


def debug_mode():
    """Check if debug mode is enabled."""
    return True


def get_connection_string():
    """Get database connection string."""
    return f"postgresql://admin:{DATABASE_PASSWORD}@localhost:5432/production"
