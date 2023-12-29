# service_handler.py

import logging
from deploymate.ssh_module import SSHConnection, SSHConnectionManager

class ServiceHandlerError(Exception):
    """Custom exception for service handling errors."""
    pass

class ServiceHandler:
    """Handler for managing system services on a remote server."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute(self, task, ssh_client):
        """Execute service-related tasks on a remote server.

        Args:
            task (dict): Task details containing the action and service name.
            ssh_client (SSHClient): SSH client connected to the remote server.

        Raises:
            ServiceHandlerError: If there is an error in handling the service.
        """
        action = task.get('action')
        service_name = task.get('service_name')

        if not service_name:
            raise ServiceHandlerError("No service name specified in the task.")

        try:
            if action == 'start':
                self.start_service(ssh_client, service_name)
            elif action == 'stop':
                self.stop_service(ssh_client, service_name)
            elif action == 'restart':
                self.restart_service(ssh_client, service_name)
            else:
                raise ServiceHandlerError(f"Invalid or unsupported action '{action}' specified.")
        except SSHConnectionError as e:
            self.logger.error(f"SSH error during service '{action}' for '{service_name}': {e}")
            raise ServiceHandlerError(e)

    def start_service(self, ssh_client, service_name):
        """Start a system service."""
        command = f"sudo systemctl start {service_name}"
        ssh_client.execute_command(command)
        self.logger.info(f"Service started: {service_name}")

    def stop_service(self, ssh_client, service_name):
        """Stop a system service."""
        command = f"sudo systemctl stop {service_name}"
        ssh_client.execute_command(command)
        self.logger.info(f"Service stopped: {service_name}")

    def restart_service(self, ssh_client, service_name):
        """Restart a system service."""
        command = f"sudo systemctl restart {service_name}"
        ssh_client.execute_command(command)
        self.logger.info(f"Service restarted: {service_name}")

# Example usage:
# service_task = {'action': 'restart', 'service_name': 'nginx'}
# ssh_client = SSHClient(host='192.168.1.10', user='user', key_file='/path/to/key.pem')
# handler = ServiceHandler()
# handler.execute(service_task, ssh_client)
