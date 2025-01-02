from file_access_layer import FileAccessLayer

class DirectoryAccessLayer:
    def __init__(self):
        self.directory_access = {'root': 3}
        self.file_access_layer = FileAccessLayer()
    
    def change_access(self, obj, mode):
        if obj.object_type == "directory":
            if self._validate_access(obj.object_name) == -1:
                raise Exception("Cannot Chmod Non-Exist Entity")
            return self._register_access(obj.object_name, mode)
        else:
            return self.file_access_layer.change_access(obj, mode)
    
    def write_access(self, obj, content):
        directory_list = obj.parent_path.split('/')
        if obj.object_type == "directory":
            if self._validate_access(obj.object_name) == -1: # Create
                if self._validate_access(directory_list[-1]) == -1:
                    raise Exception("Cannot Create under Non-Exist Directory")
                if self._validate_access(directory_list[-1]) not in [1, 3]:
                    raise Exception("Access Denied")
                if "/delete" in content:
                    raise Exception("Cannot Delete Non-Exist Entity")
                
                if self.file_access_layer.write_access(obj, content) == "Success":
                    return self._register_access(obj.object_name, 3)
            elif self._validate_access(obj.object_name) in [1, 3]: # Target write allowed
                if "/delete" in content: 
                    if self._validate_access(directory_list[-1]) not in [1, 3]:
                        raise Exception("Access Denied") # Parent write not allowed  
                    if self.file_access_layer.write_access(obj, content) == "Success": 
                        return self._register_access(obj.object_name, -1)
                else:
                    return self.file_access_layer.write_access(obj, content)
            else: # Target write not allowed
                raise Exception("Access Denied")
        else: # File
            if self._validate_access(directory_list[-1]) == -1:
                raise Exception("Cannot Create under Non-Exist Directory")
            if self._validate_access(directory_list[-1]) not in [1, 3] and "/delete" in content:
                raise Exception("Access Denied")
            return self.file_access_layer.write_access(obj, content)


    
    def read_access(self, obj):
        if obj.object_type == "directory":
            for directory in obj.parent_path.split('/') + [obj.object_name]:
                if not directory: continue # In case parse an empty string for the first eg //root will be '', root
                if self._validate_access(directory) not in [2, 3]:    
                    raise Exception("Access Denied")
            return self.file_access_layer.read_access(obj)
        else:
            for directory in obj.parent_path.split('/'):
                if self._validate_access(directory) not in [2, 3]:
                    raise Exception("Access Denied")
            return self.file_access_layer.read_access(obj)

        
    def _validate_access(self, directory_name):
        if directory_name not in self.directory_access:
            return -1
        return self.directory_access[directory_name]
    
    def _register_access(self, directory_name, access_type):
        if access_type == -1:
            del self.directory_access[directory_name]
        else:
            self.directory_access[directory_name] = access_type
        return "Success"