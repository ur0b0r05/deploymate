import logging
from deploymate.ssh_module import SSHConnection, SSHConnectionManager, SSHConnectionError

class CommandHandler:
    """Handler for executing shell commands on a remote server."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute(self, task: dict, ssh_client) -> None:
        """Execute a shell command on a remote server.

        Args:
            task (dict): Task details containing the command to execute.
            ssh_client (SSHClient): SSH client connected to the remote server.
        """
        shell_command = task.get('command')
        if not shell_command:
            self.logger.error("No command specified in the task.")
            return

        try:
            self.logger.info(f"Executing command: {shell_command}")
            stdout, stderr = ssh_client.execute_command(shell_command)
            if stdout.strip():
                self.logger.info(f"Command output: {stdout}")
            if stderr.strip():
                self.logger.info(f"Command error output: {stderr}")
        except SSHConnectionError as e:
            self.logger.error(f"Failed to execute command '{shell_command}': {e}")
# Example usage:
# command_task = {'command': 'echo "Hello, DeployMate!"'}
# handler = CommandHandler()
# handler.execute(command_task, ssh_client)
