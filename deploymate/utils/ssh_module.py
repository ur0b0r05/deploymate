import paramiko
import logging

class SSHConnectionError(Exception):
    """Custom exception for SSH connection errors."""
    pass

class SSHConnection:
    """Represents an SSH connection to a single host."""
    def __init__(self, host, user, password=None, key_file=None, port=22):
        self.host = host
        self.user = user
        self.password = password
        self.key_file = key_file
        self.port = port
        self.client = None

    def connect(self):
        """Establish an SSH connection."""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if self.key_file:
                self.client.connect(self.host, port=self.port, username=self.user, key_filename=self.key_file)
            else:
                self.client.connect(self.host, port=self.port, username=self.user, password=self.password)
            logging.info(f"SSH connection established with {self.host}")
        except paramiko.SSHException as e:
            raise SSHConnectionError(f"Failed to establish SSH connection with {self.host}: {e}")

    def execute_command(self, command):
        """Execute a command on the SSH server and return stdout, stderr, and exit code."""
        if not self.client:
            raise SSHConnectionError("SSH client not connected")

        stdin, stdout, stderr = self.client.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        stdout_data = stdout.read().decode('utf-8').strip()
        stderr_data = stderr.read().decode('utf-8').strip()
        return stdout_data, stderr_data, exit_code

    def get_transport(self):
        """Return the transport object of the SSH connection."""
        if self.client:
            return self.client.get_transport()
        else:
            raise SSHConnectionError("SSH client not connected or transport not available")

    def disconnect(self):
        """Close the SSH connection."""
        if self.client:
            self.client.close()
            logging.info(f"SSH connection closed with {self.host}")

class SSHConnectionManager:
    """Manages multiple SSH connections."""
    def __init__(self):
        self.connections = {}

    def establish_connections(self, hosts):
        """Establish SSH connections to multiple hosts."""
        for host_name, host_info in hosts.items():
            try:
                connection = SSHConnection(**host_info)
                connection.connect()
                self.connections[host_name] = connection
                logging.info(f"Connected to {host_name}")
            except SSHConnectionError as e:
                logging.error(f"{e}")

    def execute_command_on_all(self, command):
        """Execute a command on all connected hosts."""
        results = {}
        for host_name, connection in self.connections.items():
            try:
                results[host_name] = connection.execute_command(command)
            except SSHConnectionError as e:
                logging.error(f"Error on {host_name}: {e}")
                results[host_name] = None
        return results

    def close_all_connections(self):
        """Close all established SSH connections."""
        for host_name, connection in self.connections.items():
            connection.disconnect()
            logging.info(f"Disconnected from {host_name}")

# Example usage:
# manager = SSHConnectionManager()
# manager.establish_connections(hosts_info)
# output = manager.execute_command_on_all('ls')
# manager.close_all_connections()
