# main.py

import argparse
import logging
import os
from .playbook_executor import execute_playbook_from_files, YAMLDataProvider

def validate_file(file_path):
    """Check if a file exists and is readable."""
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

def parse_arguments():
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(description="DeployMate: Simple Configuration Management Tool")
    parser.add_argument('playbook', help='Path to the playbook YAML file')
    parser.add_argument('inventory', help='Path to the inventory YAML file')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Manually set logging level to DEBUG:
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().setLevel(log_level)

    # Check actual logging level:
    logging.debug("Actual logging level: %s", logging.getLevelName(logging.getLogger().level))

    # Isolate logging test:
    logging.debug("This is a DEBUG message")

    try:
        validate_file(args.playbook)
        validate_file(args.inventory)
        logging.info("Starting playbook execution...")

        # Using YAMLDataProvider for parsing
        yaml_data_provider = YAMLDataProvider()
        execute_playbook_from_files(args.playbook, args.inventory, yaml_data_provider)

        logging.info("Playbook execution completed successfully.")
    except Exception as e:  # Consider more specific exceptions here
        logging.error("Error: %s", e)

if __name__ == "__main__":
    main()
