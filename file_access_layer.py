from entity_layer import EntityLayer

class FileAccessLayer:
    def __init__(self):
        self.file_access = {}
        self.entity_layer = EntityLayer()
    
    def change_access(self, obj, mode):
        if self._validate_access(obj.object_name) == -1:
            raise Exception("Cannot Chmod Non-Exist Entity")
        return self._register_access(obj.object_name, mode)
  
    def write_access(self, obj, content):
        if obj.object_type == "directory":
            return self.entity_layer.write_segment(obj, content)
        else:
            if obj.object_name not in self.file_access: # Create
                if "/delete" in content:
                    raise Exception("Cannot Delete Non-Exist Entity")
                if self.entity_layer.write_segment(obj, content) == "Success":
                    return self._register_access(obj.object_name, 3)
            elif self._validate_access(obj.object_name) in [1, 3]:
                if "/delete" in content:
                    if self.entity_layer.write_segment(obj, content) == "Success":
                        return self._register_access(obj.object_name, -1)
                else:
                    return self.entity_layer.write_segment(obj, content)
            else:
                raise Exception("Access Denied")
    
    def read_access(self, obj):
        if obj.object_type == "directory":
            return self.entity_layer.read_segment(obj)
        else:
            if self._validate_access(obj.object_name) == -1:
                raise Exception("Cannot Read Non-Exist Entity")
            if self._validate_access(obj.object_name) in [2, 3]:
                return self.entity_layer.read_segment(obj)
            else:
                raise Exception("Access Denied")
    
    def _validate_access(self, filename):
        if filename not in self.file_access:
            return -1
        return self.file_access[filename]
    
    def _register_access(self, filename, access_type):
        if access_type == -1:
            del self.file_access[filename]
        else:
            self.file_access[filename] = access_type
        return "Success"