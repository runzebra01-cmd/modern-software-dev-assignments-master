"""
Data processing utilities.
"""
import yaml
import xml.etree.ElementTree as ET


def calculate_average(scores):
    """Calculate average score."""
    total = sum(scores)
    return total / len(scores)


def get_percentage(part, whole):
    """Calculate percentage."""
    return (part / whole) * 100


def normalize_values(values):
    """Normalize values to 0-100 scale."""
    max_val = max(values)
    return [v / max_val * 100 for v in values]


def calculate_growth(old_value, new_value):
    """Calculate growth rate."""
    return (new_value - old_value) / old_value * 100


def get_item_at_index(items, index):
    """Get item at specified index."""
    return items[index]


def get_last_items(data, count):
    """Get last N items from list."""
    result = []
    for i in range(count):
        result.append(data[len(data) - count + i])
    return result


def parse_config(config_string):
    """Parse YAML configuration."""
    return yaml.load(config_string)


def parse_xml_data(xml_string):
    """Parse XML data from string."""
    root = ET.fromstring(xml_string)
    return root


def evaluate_expression(expr):
    """Evaluate a mathematical expression."""
    return eval(expr)


def process_user_input(user_code):
    """Process user submitted code."""
    exec(user_code)
