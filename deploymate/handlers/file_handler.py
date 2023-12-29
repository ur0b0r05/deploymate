import logging
import os
from deploymate.utils.ssh_module import SSHConnection, SSHConnectionError
from deploymate.handlers.directory_handler import DirectoryHandler
from deploymate.utils.scp_transfer import SCPTransfer

class FileHandlerError(Exception):
    """Custom exception for file handling errors."""
    pass

class FileHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.directory_handler = DirectoryHandler()
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Project base directory
        self.files_to_upload_dir = os.path.join(self.base_dir, 'config', 'files_to_upload')

    def execute(self, task, ssh_client):
        action = task.get('action')
        file_paths = task.get('files', [])
        remote_path = task.get('remote_path')

        if not remote_path:
            raise FileHandlerError("No remote path specified in the task.")

        try:
            if action in ['create', 'overwrite']:
                content = task.get('content', '')
                for file_name in file_paths:
                    full_file_path = os.path.join(remote_path, file_name)
                    if action == 'create':
                        self.create_file(ssh_client, full_file_path, content)
                    elif action == 'overwrite':
                        self.overwrite_file(ssh_client, full_file_path, content)
            elif action == 'delete':
                for file_name in file_paths:
                    full_file_path = os.path.join(remote_path, file_name)
                    self.delete_file(ssh_client, full_file_path)
            elif action == 'upload':
                # Ensure the remote directory exists
                self.directory_handler.execute({'action': 'create', 'directory_path': remote_path}, ssh_client)

                for file_name in file_paths:
                    local_file_path = os.path.join(self.files_to_upload_dir, file_name)
                    remote_file_path = os.path.join(remote_path, file_name)
                    self.upload_and_move_file(ssh_client, local_file_path, remote_file_path)
            else:
                raise FileHandlerError(f"Invalid or unsupported action '{action}' specified.")
        except Exception as e:
            self.logger.error(f"Error during file '{action}' on '{remote_path}': {e}")
            raise FileHandlerError(e)

    def create_file(self, ssh_client, file_path, content):
        command = f"echo '{content}' | sudo tee {file_path} > /dev/null"
        ssh_client.execute_command(command)
        self.logger.info(f"File created at {file_path}")

    def overwrite_file(self, ssh_client, file_path, content):
        command = f"echo '{content}' | sudo tee {file_path} > /dev/null"
        ssh_client.execute_command(command)
        self.logger.info(f"File overwritten at {file_path}")

    def delete_file(self, ssh_client, file_path):
        command = f"sudo rm -f {file_path}"
        ssh_client.execute_command(command)
        self.logger.info(f"File deleted at {file_path}")

    def upload_and_move_file(self, ssh_client, local_path, remote_final_path):
        """Uploads a file to a temporary path and then moves it to the final path."""
        if not os.path.isfile(local_path):
            raise FileHandlerError(f"File does not exist: {local_path}")

        # Temporary upload path in the home directory of the 'ubuntu' user
        intermediate_path = "/home/ubuntu/" + os.path.basename(local_path)

        # Upload the file to the temporary path
        scp_transfer = SCPTransfer(ssh_client)
        scp_transfer.upload_file(local_path, intermediate_path)

        # Move the file to the final path using sudo
        move_command = f"sudo mv {intermediate_path} {remote_final_path}"
        stdout, stderr, exit_code = ssh_client.execute_command(move_command)
        if exit_code != 0:
            self.logger.error(f"Failed to move file. STDOUT: {stdout}, STDERR: {stderr}")
            raise FileHandlerError("Failed to move file")
        else:
            self.logger.info(f"File moved to {remote_final_path}")

# Example usage (commented out)
# file_task = {
#     'action': 'upload',
#     'files': ['file1.txt', 'file2.txt'],
#     'remote_path': '/remote/path'
# }
# ssh_client = SSHConnection(host='example.com', user='user', key_file='/path/to/key.pem')
# handler = FileHandler()
# handler.execute(file_task, ssh_client)
