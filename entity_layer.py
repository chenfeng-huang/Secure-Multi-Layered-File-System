from segment_layer import SegmentLayer
from handles import Segment, Content

class EntityLayer:
    def __init__(self):
        self.name_to_segment = {'root':"0_0"}  # Mapping object names to segment IDs
        self.segment_to_name = {"0_0":'root'}  # Mapping segment IDs to object names
        self.segment_layer = SegmentLayer()
    
    def read_segment(self, obj):
        segment_id = self._find_segment_by_name(obj.object_name)
        segment = Segment(segment_id, obj.object_name, obj.object_type)
        result = self.segment_layer.extract(segment)
        if obj.object_type == 'directory':
            fileNames = ""
            for seg_id in result.result_content:
               
                fileNames += self._find_name_by_segment(seg_id) + ","
            result.result_content = fileNames[:-1]
        return result
    
    def write_segment(self, obj, content):
        parsed_content = self._parse_content(obj, content)
        if parsed_content.operation == "append":
            return self.segment_layer.append(parsed_content)
        elif parsed_content.operation == "overwrite":
            return self.segment_layer.overwrite(parsed_content)
        elif parsed_content.operation == "delete":
            self.segment_layer.purge(parsed_content)
            return self._remove_segment(parsed_content.segment_id, parsed_content.object_name)
        elif parsed_content.operation == "create":
            segment = self.segment_layer.create(parsed_content)
            return self._register_segment(segment)
    
    def _register_segment(self, segment):
        self.name_to_segment[segment.object_name] = segment.segment_id
        self.segment_to_name[segment.segment_id] = segment.object_name
        return "Success"
    
    def _remove_segment(self, segment_id, object_name):
        del self.name_to_segment[object_name]
        del self.segment_to_name[segment_id]
        return "Success"
    
    def _find_segment_by_name(self, object_name):
        return self.name_to_segment.get(object_name)
    
    def _find_name_by_segment(self, segment_id):
        return self.segment_to_name.get(segment_id)
    
    def _parse_content(self, obj, content):
        operation = "overwrite"
        if "/+" in content:
            operation = "append"
            content = content.replace("/+", "")
        elif "/delete" in content:
            operation = "delete"
            content = ""
        
        segment_id = self._find_segment_by_name(obj.object_name)

        directory_list = obj.parent_path.split('/')
        parent_id = self._find_segment_by_name(directory_list[-1])

        if segment_id is None:
            operation = "create"
        
        if obj.object_type == "file":
            parsed_content = content
        else:
            parsed_content = []
 
            for object_name in content.split(','):

                object_name = object_name.strip('"')
                if object_name == '': continue
                segment_id = self._find_segment_by_name(object_name)
                if segment_id is None:
                    raise Exception("Cannot list Non-Exist Entity into directory")
                parsed_content.append(segment_id)
            
        return Content(parsed_content, operation, segment_id, parent_id, obj.object_type, obj.object_name)