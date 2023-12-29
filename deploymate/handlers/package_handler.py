import logging
from deploymate.ssh_module import SSHConnection, SSHConnectionError

class PackageHandlerError(Exception):
    """Custom exception for package handling errors."""
    pass

class PackageHandler:
    """Handler for managing software packages on a remote server."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute(self, task, ssh_client):
        """Execute package-related tasks on a remote server.

        Args:
            task (dict): Task details containing the action and package details.
            ssh_client (SSHClient): SSH client connected to the remote server.

        Raises:
            PackageHandlerError: If there is an error in handling the package.
        """
        action = task.get('action')
        package_name = task.get('package_name')

        if not package_name:
            raise PackageHandlerError("No package name specified in the task.")

        try:
            if action == 'install':
                self.install_package(ssh_client, package_name)
            elif action == 'update':
                self.update_package(ssh_client, package_name)
            elif action == 'remove':
                self.remove_package(ssh_client, package_name)
            else:
                raise PackageHandlerError(f"Invalid or unsupported action '{action}' specified.")
        except SSHConnectionError as e:
            self.logger.error(f"SSH error during package '{action}' for '{package_name}': {e}")
            raise PackageHandlerError(e)

    def install_package(self, ssh_client, package_name):
        """Install a software package."""
        command = f"sudo apt-get install -y {package_name}"
        stdout, stderr, exit_code = ssh_client.execute_command(command)
        self.logger.info(f"STDOUT: {stdout}")
        self.logger.info(f"STDERR: {stderr}")
        self.logger.info(f"Package installed: {package_name}")

    def update_package(self, ssh_client, package_name):
        """Update a software package."""
        command = f"sudo apt-get update && sudo apt-get install --only-upgrade -y {package_name}"
        stdout, stderr, exit_code = ssh_client.execute_command(command)
        self.logger.info(f"STDOUT: {stdout}")
        self.logger.info(f"STDERR: {stderr}")
        self.logger.info(f"Package updated: {package_name}")

    def remove_package(self, ssh_client, package_name):
        """Purge a software package along with its configuration files and perform autoremove."""
        purge_command = f"sudo apt-get purge -y {package_name}"
        autoremove_command = "sudo apt-get autoremove -y"

        # Execute purge command
        stdout, stderr, exit_code = ssh_client.execute_command(purge_command)
        if exit_code != 0:
            self.logger.error(f"Failed to purge package {package_name}. Exit Code: {exit_code}")
            self.logger.error(f"STDOUT: {stdout}")
            self.logger.error(f"STDERR: {stderr}")
            raise PackageHandlerError(f"Failed to purge package {package_name}. Error: {stderr}")
        self.logger.info(f"Package purged: {package_name}")

        # Execute autoremove command
        stdout, stderr, exit_code = ssh_client.execute_command(autoremove_command)
        if exit_code != 0:
            self.logger.error("Failed to execute autoremove. Exit Code: {exit_code}")
            self.logger.error(f"STDOUT: {stdout}")
            self.logger.error(f"STDERR: {stderr}")
        else:
            self.logger.info("Autoremove executed successfully.")

# Example usage:
# package_task = {'action': 'install', 'package_name': 'nginx'}
# ssh_client = SSHClient(host='192.168.1.10', user='user', key_file='/path/to/key.pem')
# handler = PackageHandler()
# handler.execute(package_task, ssh_client)
