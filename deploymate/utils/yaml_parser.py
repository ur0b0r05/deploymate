# yaml_parser.py

import yaml
import logging
import os

class YAMLParseError(Exception):
    """Custom exception for errors during YAML parsing."""
    pass

def file_exists(file_path: str) -> bool:
    """Check if a file exists.
    Args:
        file_path (str): Path to the file.
    Returns:
        bool: True if file exists, False otherwise.
    """
    return os.path.exists(file_path)

def parse_yaml(file_path: str) -> dict:
    """Parse a YAML file and return the data.
    Args:
        file_path (str): Path to the YAML file.
    Returns:
        dict: Parsed data.
    Raises:
        YAMLParseError: If there is an issue parsing the file.
    """
    if not file_exists(file_path):
        raise YAMLParseError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        logging.error(f"YAML parsing error in file {file_path}: {e}")
        raise YAMLParseError(f"Error parsing YAML file {file_path}: {e}")
    except Exception as e:
        logging.error(f"Unexpected error when parsing {file_path}: {e}")
        raise YAMLParseError(f"Unexpected error when parsing {file_path}")

def parse_inventory(inventory_path: str) -> dict:
    """Parse an inventory YAML file and return the data.
    Args:
        inventory_path (str): Path to the inventory YAML file.
    Returns:
        dict: Parsed data.
    Raises:
        YAMLParseError: If there is an issue parsing the file.
    """
    return parse_yaml(inventory_path)

# Example usage:
# try:
#     playbook_data = parse_yaml('path/to/playbook.yml')
#     inventory_data = parse_inventory('path/to/inventory.yml')
# except YAMLParseError as e:
#     logging.error(e)
#     # Handle the error appropriately
