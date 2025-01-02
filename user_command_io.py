from directory_access_layer import DirectoryAccessLayer
from handles import Object

class UserCommandIO:
    def __init__(self):
        self.directory_access_layer = DirectoryAccessLayer()

    def run(self):
        print("Welcome to the Toy Secure File System!")
        print("Enter commands in the format: <operation> <object_type> <path> [content]")
        print("Example: write file root/file1 'Hello, World!'")
        print("Enter 'exit' or cltr+c to quit the program.")

        while True:
            command = input("\nEnter a command: ")
            if command.lower() == 'exit':
                print("Exiting the program.")
                break

            args = command.split()
            if len(args) < 3:
                print("Invalid command. Please provide the required arguments.")
                continue

            operation = args[0]
            object_type = args[1]
            path = args[2].split('/')
            parent_path = '/'.join(path[:-1])
            object_name = path[-1]
            obj = Object(parent_path, object_name, object_type)

            if operation not in ["read", "write", "chmod"]:
                print("Invalid operation. Supported operations: read, write, chmod")
                continue

            if object_type not in ["file", "directory"]:
                print("Invalid object type. Supported types: file, directory")
                continue
            
            
            if operation not in ["read", "write", "chmod"]:
                return "Invalid Operation"
            
            if object_type not in ["file", "directory"]:
                return "Invalid Filetype"
            
            
            try:
                if operation == "read":
                    result = self._read(obj)
                    print(result)
                elif operation == "write":
                    if len(args) < 4:
                        print("Invalid command. Please provide the content for write operation.")
                        continue
                    content = ' '.join(args[3:])
                    
                    result = self._write(obj, content)
                    print(result)
                elif operation == "chmod":
                    if len(args) < 4:
                        print("Invalid command. Please provide the mode for changeMode operation.")
                        continue
                    mode = int(args[3])
                    result = self._chmod(obj, mode)
                    print(result)
            except Exception as e:
                print(f"Error: {str(e)}")

    def command_input(self, args):
        if len(args) < 3:
            return "Invalid Operation"
        
        operation = args[0]
        object_type = args[1]
        path = args[2].split('/')
        parent_path = '/'.join(path[:-1])
        object_name = path[-1]
        
        if operation not in ["read", "write", "chmod"]:
            return "Invalid Operation"
        
        if object_type not in ["file", "directory"]:
            return "Invalid Filetype"
        
        obj = Object(parent_path, object_name, object_type)
        
        try:
            if operation == "read":
                return self._read(obj)
            elif operation == "write":
                if len(args) < 4:
                    return "Invalid Writing command"
                content = args[3]
                return self._write(obj, content)
            elif operation == "chmod":
                if len(args) < 4:
                    return "Invalid chmod command"
                mode = int(args[3])
                if mode not in [0, 1, 2, 3]:
                    return "Invalid chmod command"
                return self._chmod(obj, mode)
        except Exception as e:
               print(f"Error: {str(e)}")
            
    def _read(self, obj):
        result = self.directory_access_layer.read_access(obj)
        return result.result_content
    
    def _write(self, obj, content):
        return self.directory_access_layer.write_access(obj, content)
    
    def _chmod(self, obj, mode):
        return self.directory_access_layer.change_access(obj, mode)