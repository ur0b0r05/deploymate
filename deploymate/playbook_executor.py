# playbook_executor.py

import logging
import os
from deploymate.utils import yaml_parser
from deploymate.resource_handler_factory import TaskResourceHandlerFactory
from deploymate.utils.ssh_module import SSHConnection, SSHConnectionManager, SSHConnectionError

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Data provider interface
class DataProvider:
    def parse_playbook(self, path):
        raise NotImplementedError

    def parse_inventory(self, path):
        raise NotImplementedError

# Concrete YAML Data Provider
class YAMLDataProvider(DataProvider):
    def parse_playbook(self, path):
        return yaml_parser.parse_yaml(path)

    def parse_inventory(self, path):
        return yaml_parser.parse_inventory(path)

def execute_task_on_single_host(task, ssh_client):
    """Execute a given task on a single host using an SSH client."""
    logger.debug(f"Starting execution of task: {task['name']} on host")

    resource_type = task['type']
    logger.debug(f"Resource type: {resource_type}")

    handler = TaskResourceHandlerFactory.create_resource_handler(resource_type)
    logger.debug(f"Handler: {handler}")

    logger.debug(f"Executing task: {task['name']} with type {resource_type}")
    try:
        output = handler.execute(task, ssh_client)
        logger.debug(f"Task execution completed: {task['name']}")
        logger.debug(f"Handler output: {output}")
    except Exception as e:
        logger.error(f"Error executing task '{task['name']}': {e}")

def execute_playbook(playbook, inventory):
    """Execute tasks defined in a playbook for hosts in the inventory."""
    connection_manager = SSHConnectionManager()

    # Base directory for the SSH key (assumes this script is in the same directory as the config folder)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Establish connections to all hosts
    for host_name, host_info in inventory['all']['hosts'].items():
        if 'ssh_private_key_file' in host_info:
            # Construct the absolute path for the SSH key file
            relative_key_path = host_info.pop('ssh_private_key_file').lstrip('./')
            ssh_key_path = os.path.join(base_dir, 'config', relative_key_path)
            host_info['key_file'] = ssh_key_path

        try:
            connection = SSHConnection(**host_info)
            connection.connect()
            connection_manager.connections[host_name] = connection
        except SSHConnectionError as e:
            logger.error(f"Failed to establish SSH connection: {e}")

    # Execute tasks on the appropriate hosts
    for task in playbook['tasks']:
        target_hosts = task.get('hosts', [])
        
        # Check if 'all' is specified in hosts, if so, target all hosts
        if 'all' in target_hosts or not target_hosts:
            target_hosts = inventory['all']['hosts'].keys()

        for host_name in target_hosts:
            ssh_client = connection_manager.connections.get(host_name)
            if ssh_client:
                try:
                    execute_task_on_single_host(task, ssh_client)
                except Exception as e:
                    logger.error(f"Error executing task '{task['name']}' on host '{host_name}': {e}")

    # Close all connections
    connection_manager.close_all_connections()

def execute_playbook_from_files(playbook_path, inventory_path, data_provider):
    """Execute playbook from file paths using a specified data provider."""
    playbook = data_provider.parse_playbook(playbook_path)
    inventory = data_provider.parse_inventory(inventory_path)
    execute_playbook(playbook, inventory)

# Example usage (commented out)
# yaml_data_provider = YAMLDataProvider()
# execute_playbook_from_files('path/to/playbook.yml', 'path/to/inventory.yml', yaml_data_provider)
