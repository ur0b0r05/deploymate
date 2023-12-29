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

    def execute(self, task, ssh_client):
        action = task.get('action')
        file_path = task.get('file_path')

        if not file_path:
            raise FileHandlerError("No file path specified in the task.")

        try:
            if action in ['create', 'overwrite', 'upload']:
                directory_path = os.path.dirname(file_path)
                self.directory_handler.execute({'action': 'create', 'directory_path': directory_path}, ssh_client)

                if action == 'create':
                    self.create_file(ssh_client, file_path, task.get('content', ''))
                elif action == 'overwrite':
                    self.overwrite_file(ssh_client, file_path, task.get('content', ''))
                elif action == 'upload':
                    local_path = task.get('local_path')
                    self.upload_and_move_file(ssh_client, local_path, file_path)

            elif action == 'delete':
                self.delete_file(ssh_client, file_path)

            else:
                raise FileHandlerError(f"Invalid or unsupported action '{action}' specified.")

        except SSHConnectionError as e:
            self.logger.error(f"Error during file '{action}' on '{file_path}': {e}")
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
        intermediate_path = "/home/ubuntu/" + os.path.basename(local_path)
        scp_transfer = SCPTransfer(ssh_client)
        scp_transfer.upload_file(local_path, intermediate_path)
        self.move_file(ssh_client, intermediate_path, remote_final_path)

    def move_file(self, ssh_client, original_path, target_path):
        move_command = f"sudo mv {original_path} {target_path}"
        stdout, stderr, exit_code = ssh_client.execute_command(move_command)
        if exit_code != 0:
            self.logger.error(f"Failed to move file. STDOUT: {stdout}, STDERR: {stderr}")
            raise Exception("Failed to move file")
        else:
            self.logger.info(f"File moved to {target_path}")

# Example usage:
# file_task = {
#     'local_path': '/local/path/file.txt',
#     'remote_temp_path': '/upload/ubuntu/temp_file.txt',
#     'remote_final_path': '/remote/path/file.txt'
# }
# ssh_client = SSHConnection(host='example.com', user='user', key_file='/path/to/key.pem')
# handler = FileHandler()
# handler.upload_and_move_file(ssh_client, file_task['local_path'], file_task['remote_temp_path'], file_task['remote_final_path'])
