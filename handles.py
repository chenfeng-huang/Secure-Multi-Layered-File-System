class Object:
    def __init__(self, parent_path, object_name, object_type):
        self.parent_path = parent_path
        self.object_name = object_name
        self.object_type = object_type

class Segment:
    def __init__(self, segment_id, object_name, object_type):
        self.segment_id = segment_id
        self.object_name = object_name
        self.object_type = object_type

class Content:
    def __init__(self, parsed_content, operation, segment_id, parent_id, object_type, object_name):
        self.parsed_content = parsed_content
        self.operation = operation
        self.segment_id = segment_id
        self.parent_id = parent_id
        self.object_type = object_type
        self.object_name = object_name

class Result:
    def __init__(self, result_content):
        self.result_content = result_content