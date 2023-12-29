import logging
from deploymate.ssh_module import SSHConnection, SSHConnectionManager

logging.basicConfig(level=logging.DEBUG)  # Set logging level to DEBUG
logger = logging.getLogger(__name__)

class DirectoryHandler:
    """Handler for managing directories on a remote server."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute(self, task, ssh_client):
        """Execute directory-related tasks on a remote server."""
        logger.debug(f"Executing directory task: {task}")

        action = task.get('action')
        logger.debug(f"Extracted action: {action}")
        assert action in ['create', 'delete'], "Invalid action specified"

        directory_path = task.get('directory_path')
        logger.debug(f"Extracted directory path: {directory_path}")
        assert directory_path, "No directory path specified"

        command = self.construct_command(action, directory_path)
        logger.debug(f"Constructing command for action '{action}' on '{directory_path}': {command}")

        logger.debug(f"Executing command '{command}' on SSH client: {ssh_client}")
        try:
            output = ssh_client.execute_command(command)
            logger.info(f"Executed '{command}'. Output: {output}")
        except SSHConnectionError as e:
            logger.error(f"SSH error during '{action}' on '{directory_path}': {e}")

    def construct_command(self, action, directory_path):
        """Constructs the command based on the action and directory path."""
        logger.debug(f"Constructing command for action '{action}' and path '{directory_path}'")
        # Add input sanitization here if directory_path is from an untrusted source
        if action == 'create':
            return f"sudo mkdir -p {directory_path}"
        elif action == 'delete':
            return f"rm -r {directory_path}"
