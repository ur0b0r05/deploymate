# update_handler.py

import logging
from ..ssh_module import SSHConnection, SSHConnectionManager

class UpdateHandlerError(Exception):
    """Custom exception for update handling errors."""
    pass

class UpdateHandler:
    """Handler for managing system updates on a remote server."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute(self, task, ssh_client):
        """Execute update-related tasks on a remote server.

        Args:
            task (dict): Task details containing the action.
            ssh_client (SSHClient): SSH client connected to the remote server.

        Raises:
            UpdateHandlerError: If there is an error in handling the update.
        """
        action = task.get('action')

        try:
            if action == 'update':
                self.update_packages(ssh_client)
            elif action == 'upgrade':
                self.upgrade_packages(ssh_client)
            else:
                raise UpdateHandlerError(f"Invalid or unsupported action '{action}' specified.")
        except SSHConnectionError as e:
            self.logger.error(f"SSH error during update '{action}': {e}")
            raise UpdateHandlerError(e)

    def update_packages(self, ssh_client):
        """Update package lists."""
        command = "sudo apt-get update"
        ssh_client.execute_command(command)
        self.logger.info("Package lists updated.")

    def upgrade_packages(self, ssh_client):
        """Upgrade all installed packages."""
        command = "sudo apt-get upgrade -y"
        ssh_client.execute_command(command)
        self.logger.info("Installed packages upgraded.")

# Example usage:
# update_task = {'action': 'upgrade'}
# ssh_client = SSHClient(host='192.168.1.10', user='user', key_file='/path/to/key.pem')
# handler = UpdateHandler()
# handler.execute(update_task, ssh_client)
