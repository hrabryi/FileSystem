import logging

logging.basicConfig(filename='output.txt', filemode='w', level=logging.INFO, format='%(message)s')
logger = logging.getLogger('FileSystem')


class FileSystem:
    """
    Fake file system
    Nested dictionary was used to store directories tree.
    """

    def __init__(self):
        self.root = {}

    def create(self, path: str) -> str:
        """
        Create a new folder
        :param path: full folder path like 'fruits/apples/fuji'
        :return: message with operation result
        """
        current_directory = self.root
        for directory in path.split('/'):
            if directory not in current_directory:
                current_directory[directory] = {}
            current_directory = current_directory[directory]
        return f"CREATE {path}"

    def search(self, path: str) -> (bool, str):
        """
        Search a folder
        :return: Tuple (True, parent directory name) if folder exist and (False, missed_folder) otherwise.
        """
        parent_directory = curr_directory = self.root
        for directory in path.split('/'):
            if directory not in curr_directory:
                return False, directory
            parent_directory = curr_directory
            curr_directory = curr_directory[directory]
        return True, parent_directory

    def delete(self, path: str) -> str:
        """
        Delete directory with path. Return error message if directory doesn't exit.
        :return: message with operation result.
        """
        messages = [f"DELETE {path}"]
        path_exist, parent_directory = self.search(path)
        if not path_exist:
            messages.append(f"Cannot delete {path} - {parent_directory} does not exist")
            return "\n".join(messages)
        directory_name_to_delete = path.split('/')[-1]
        parent_directory.pop(directory_name_to_delete)
        return "\n".join(messages)

    def move(self, source, destination) -> str:
        """
        Move directory from source to destination
        :return: message with operation result
        """
        messages = [f"MOVE {source} {destination}"]
        # Check that source path exist
        source_dir_exist, source_parent_dir = self.search(source)
        if source_dir_exist:
            source_dir = source.split('/')[-1]
            self.root[destination].update({source_dir: source_parent_dir.pop(source_dir)})
        else:
            messages.append("Error can't move directory. Directory doesn't exist.")
        return "\n".join(messages)

    def list(self) -> str:
        """
        Return a string with formatted directory tree
        :return: message with operation result
        """
        messages = ["LIST"]

        def _list_helper(directory: dict, indent=0):
            for k, v in sorted(directory.items()):
                messages.append('\t' * indent + str(k))
                if isinstance(v, dict):
                    _list_helper(v, indent + 1)
                else:
                    messages.append('\t' * (indent + 1) + str(v))

        _list_helper(directory=self.root)
        return "\n".join(messages)


def read_file(file_name: str) -> str:
    """
    Read file line by line
    :param file_name:
    :return: one line of data
    """
    with open(file_name) as file:
        for line in file:
            yield line.strip()


def extract_command(line: str) -> dict:
    """
    Extract commands and path from string and convert it to a dictionary
    :param line: one string of data
    :return: dictionary with command and parameters
    """
    splitted_line = line.split(' ')
    operation = source = destination = None
    if len(splitted_line) == 1:
        operation = splitted_line[0]
    elif len(splitted_line) == 2:
        operation, source = splitted_line
    elif len(splitted_line) == 3:
        operation, source, destination = splitted_line
    return {'operation': operation, 'source': source, 'destination': destination}


def execute_command(filesystem: FileSystem, command: dict) -> str:
    """
    Execute command from operation dictionary
    :param command: dictionary with command, source and destination
    """
    if command.get('operation') == 'CREATE':
        return filesystem.create(path=command.get('source'))
    if command.get('operation') == 'LIST':
        return filesystem.list()
    if command.get('operation') == 'MOVE':
        return filesystem.move(source=command.get('source'), destination=command.get('destination'))
    if command.get('operation') == 'DELETE':
        return filesystem.delete(path=command.get('source'))
    return f"ERROR. Unsupported command:{command.get('operation')}"


if __name__ == '__main__':
    input_file_name = "input.txt"
    file_system = FileSystem()
    for data_line in read_file(input_file_name):
        command = extract_command(data_line)
        output = execute_command(filesystem=file_system, command=command)
        logger.info(output)
