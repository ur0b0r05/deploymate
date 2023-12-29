from scp import SCPClient, SCPException
import logging
import os

class SCPTransferError(Exception):
    """Custom exception for SCP transfer errors."""
    pass

class SCPTransfer:
    """Class for handling SCP transfers using an existing SSH connection."""

    def __init__(self, ssh_client):
        self.ssh_client = ssh_client
        self.logger = logging.getLogger(__name__)

    def upload_file(self, local_path, remote_path):
        if not os.path.exists(local_path) or not os.path.isfile(local_path):
            raise SCPTransferError(f"Local file does not exist: {local_path}")

        try:
            with SCPClient(self.ssh_client.get_transport()) as scp:
                scp.put(local_path, remote_path)
                self.logger.info(f"File uploaded to {remote_path}")
        except SCPException as e:
            self.logger.error(f"Failed to upload file via SCP: {e}")
            raise SCPTransferError(f"Failed to upload file to {remote_path}")

# Example usage:
# scp_transfer = SCPTransfer(ssh_client)
# scp_transfer.upload_file('path/to/local/file.txt', '/remote/path/file.txt')
