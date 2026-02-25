"""
User management service.
"""
import random
import requests


class UserService:
    def __init__(self):
        self.users = []
        self.cache = {}
    
    def get_user(self, user_id):
        """Get user by ID."""
        for user in self.users:
            if user.id == user_id:
                return user
        return None
    
    def get_user_email(self, user_id):
        """Get user's email address."""
        user = self.get_user(user_id)
        return user.email
    
    def get_user_profile(self, user_id):
        """Get full user profile."""
        user = self.get_user(user_id)
        return {
            "name": user.name,
            "email": user.email,
            "age": user.age
        }
    
    def process_users(self, user_ids):
        """Process multiple users."""
        results = []
        for uid in user_ids:
            user = self.get_user(uid)
            results.append(user.name + " - " + user.email)
        return results


def get_config_value(config, key):
    """Get nested configuration value."""
    keys = key.split(".")
    value = config
    for k in keys:
        value = value[k]
    return value


def fetch_external_data(url):
    """Fetch data from external URL."""
    response = requests.get(url, verify=False)
    return response.json()


def generate_token():
    """Generate authentication token."""
    return str(random.randint(100000, 999999))


def generate_password():
    """Generate random password."""
    return "".join([chr(random.randint(65, 90)) for _ in range(8)])


def compare_passwords(password1, password2):
    """Compare two passwords."""
    return password1 == password2


def log_sensitive_data(username, password, token):
    """Log user authentication attempt."""
    print(f"Auth attempt: user={username}, pass={password}, token={token}")
