import paramiko
import logging

def test_ssh_connection(host, username, key_file=None, password=None, port=22):
    # Set up logging to display potential debug information
    logging.basicConfig(level=logging.DEBUG)

    # Create an instance of the SSHClient
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the host
        if key_file:
            client.connect(hostname=host, port=port, username=username, key_filename=key_file)
        else:
            client.connect(hostname=host, port=port, username=username, password=password)

        # Execute a simple command (e.g., 'ls') and print the output
        stdin, stdout, stderr = client.exec_command('ls')
        print("Command Output:", stdout.read().decode())
        print("Command Error:", stderr.read().decode())

    except paramiko.SSHException as e:
        print(f"SSH connection failed: {e}")
    finally:
        # Close the client to free resources
        client.close()

# Replace these values with your SSH server details
HOST = ""
USERNAME = "your_username"
KEY_FILE = "Users/mav/home/deploymate_project/deploymate/config/pair-ansible-challenge.pem"  # Use None if using password
PASSWORD = None  # Use your password here if not using an SSH key
PORT = 22  # Default SSH port is 22

if __name__ == "__main__":
    test_ssh_connection(HOST, USERNAME, key_file=KEY_FILE, password=PASSWORD, port=PORT)
