# resource_handler_factory.py

# Importing the specific handler classes
from deploymate.handlers.package_handler import PackageHandler

from deploymate.handlers.file_handler import FileHandler
from deploymate.handlers.service_handler import ServiceHandler
from deploymate.handlers.update_handler import UpdateHandler
from deploymate.handlers.directory_handler import DirectoryHandler
from deploymate.handlers.command_handler import CommandHandler

class UnknownResourceTypeError(Exception):
    """Exception raised for unknown resource types."""
    def __init__(self, resource_type):
        self.message = f"Unknown resource type: {resource_type}"
        super().__init__(self.message)

class TaskResourceHandlerFactory:
    @staticmethod
    def create_resource_handler(resource_type):
        """Create and return a handler object based on the resource type.

        Args:
            resource_type (str): The type of the resource (e.g., 'package', 'file').

        Returns:
            object: An instance of the corresponding handler class.

        Raises:
            UnknownResourceTypeError: If an unknown resource type is provided.
        """
        if resource_type == 'package':
            return PackageHandler()
        elif resource_type == 'file':
            return FileHandler()
        elif resource_type == 'service':
            return ServiceHandler()
        elif resource_type == 'update':
            return UpdateHandler()
        elif resource_type == 'directory':
            return DirectoryHandler()
        elif resource_type == 'command':
            return CommandHandler()
        else:
            raise UnknownResourceTypeError(resource_type)

# Example usage:
# handler = TaskResourceHandlerFactory.create_resource_handler('package')
