# Deploymate - Ansible-Like Configuration Management Tool

Deploymate is a simple configuration management tool similar to Ansible. It reads a playbook (in YAML format) and executes actions based on it against remote targets running Ubuntu 18.04 via SSH. This documentation will guide you on how to set up and use Deploymate.

### Prerequisites
Before you begin, ensure you have the following prerequisites:

- Python 3.x: Deploymate is written in Python 3.
- SSH Key Pair: You should have an SSH private key file (e.g., pair-ansible-challenge.pem) to authenticate with remote servers.
- Inventory File: Create an inventory file (e.g., inventory_test.yaml) that lists your target servers and their SSH configurations.
- Deploymate Project Directory: Ensure that your playbook, inventory file, and SSH private key file are located at /deploymate/config. Your directory structure should look like this:
    ```
    /deploymate/
        /config/
            playbook_test.yaml
            inventory_test.yaml
            pair-ansible-challenge.pem
    ```
### Running Deploymate

To execute the Deploymate project, one should follow these steps:

1. **Install Dependencies:**

   Before running Deploymate, it is necessary to ensure that all required dependencies are installed. These dependencies are listed in the project's `requirements.txt` file. One should open the terminal, navigate to the directory containing the `requirements.txt` file, and run the following command:

   pip install -r requirements.txt

   This command will install the following Python packages:
   - paramiko==3.4.0 for SSH connections.
   - PyYAML==6.0.1 for YAML parsing.
   - scp==0.14.5 for SCP file transfers.

2. **Navigate to the Project Root Directory:**

   The user should open their terminal and navigate to the root directory of the project.

3. **Execute Deploymate:**

   To execute Deploymate, the following command should be run:

   python3 -m deploymate.main deploymate/config/playbook_test.yaml deploymate/config/inventory_test.yaml


### Playbook Structure
The playbook_test.yaml file is your playbook, which contains a series of tasks to execute. Each task in the playbook has a name, type, action, and other properties. The tasks can perform actions like package management, file operations, service control, and more.

### Inventory Configuration
The inventory_test.yaml file serves as your inventory, listing the remote servers to target. It should have the following structure:

```
all:
  hosts:
    testserver1:
      host: 3.83.238.253
      user: ubuntu
      ssh_private_key_file: ./pair-ansible-challenge.pem

    testserver2:
      host: 52.7.160.19
      user: ubuntu
      ssh_private_key_file: ./pair-ansible-challenge.pem
```
Replace the host IP addresses and usernames with your own server details.

### Uploading Files
If your playbook includes tasks to upload files, make sure the files to be uploaded are located in the config/files_to_upload directory. The playbook should specify the correct file paths.

### Idempotent Execution
Deploymate aims to be idempotent, meaning you can run the playbook multiple times without causing errors. Ensure that the tasks within your playbook are designed to be idempotent.

### Additional Information
For any additional details, please refer to the comments in the playbook_test.yaml file for specific task descriptions and configurations.


# Instructions for Playbook Task Types in Deploymate Playbook

When working with the Deploymate playbook (`playbook_test.yaml`), follow these instructions for each task type to perform specific actions on remote servers:

## Instructions for Package Task
- **Task Type:** package
- **To Install a Package:**
  - Use the `install` action to install a specified software package on remote servers.
- **To Remove a Package:**
  - Use the `remove` action to remove a specified software package from remote servers.
- **Purpose:** This task manages software packages, allowing for installation and removal as required.

## Instructions for File Task
- **Task Type:** file
- **To Create a File:**
  - Use the `create` action to make a new file with specified content on remote servers.
- **To Upload a File:**
  - Use the `upload` action to send files from your local machine to remote servers.
- **To Delete a File:**
  - Use the `delete` action to remove specific files on remote servers.
- **Purpose:** This task handles file management, including creation, uploading, and deletion of files.

## Instructions for Service Task
- **Task Type:** service
- **To Start a Service:**
  - Use the `start` action to begin a specified service on remote servers.
- **To Stop a Service:**
  - Use the `stop` action to cease a specified service on remote servers.
- **To Restart a Service:**
  - Use the `restart` action to reboot a specified service on remote servers.
- **Purpose:** This task is used for controlling services, including starting, stopping, and restarting as necessary.

## Instructions for Update Task
- **Task Type:** update
- **To Update Packages:**
  - Use the `update` action to refresh the package lists on remote servers.
- **To Upgrade Packages:**
  - Use the `upgrade` action to enhance installed packages on remote servers.
- **Purpose:** This task focuses on package management, ensuring up-to-date and secure software.

## Instructions for Directory Task
- **Task Type:** directory
- **To Create a Directory:**
  - Use the `create` action to establish a new directory on remote servers.
- **To Delete a Directory:**
  - Use the `delete` action to remove specific directories on remote servers.
- **Purpose:** This task manages directories, aiding in file and resource organization.

## Instructions for Command Task
- **Task Type:** command
- **To Execute a Command:**
  - Use the custom command execution action for running specific commands on target servers.
- **Purpose:** This task allows for flexibility in executing tailored commands as per specific requirements.



