from handles import Segment, Result
from types import MappingProxyType
import random
import time
import string

class SegmentLayer:
    def __init__(self):
        self.segment_access = MappingProxyType({"0_0":3}) # Special MAC access restriction. Immutatble.
        self.segment_content = {"0_0":[]} 
    
    def extract(self, segment):
        if self._validate(segment.segment_id) not in [-1, 2, 3]:
            raise Exception("Access Denied")
        if segment.object_type == "file":
            return Result(self._read_content(segment.segment_id))
        else:
            return Result(self._read_ID(segment.segment_id))

    def create(self, content):
        segment_id = self._allocate()
        if content.object_type == "file":
            parent_ids = self._read_ID(content.parent_id) + [segment_id]
            self._modify(content.parent_id, parent_ids) # parent ID update

            content_segment_id = self._allocate()
            self._modify(content_segment_id, content.parsed_content)
            self._modify(segment_id, [content_segment_id])
        else:
            parent_ids = self._read_ID(content.parent_id) + [segment_id]
            self._modify(content.parent_id, parent_ids) # parent ID update

            self._modify(segment_id, content.parsed_content)
        return Segment(segment_id, content.object_name, content.object_type)
    
    def purge(self, content):
        if self._validate(content.segment_id) not in [-1, 1, 3]:
            raise Exception("Access Denied")
        return self._modify(content.segment_id, '/delete')
    
    def append(self, content):
        if self._validate(content.segment_id) not in [-1, 1, 3]:
            raise Exception("Access Denied")
        current_content = self._read_ID(content.segment_id)
        new_segment_id = self._allocate()
        if self._modify(new_segment_id, content.parsed_content) == "Success":
            return self._modify(content.segment_id, current_content + [new_segment_id])
    
    def overwrite(self, content):
        if self._validate(content.segment_id) not in [-1, 1, 3]:
            raise Exception("Access Denied")
        new_segment_id = self._allocate()
        if self._modify(new_segment_id, content.parsed_content) == "Success":
            return self._modify(content.segment_id, [new_segment_id])
    
    def _validate(self, segment_id):
        if segment_id not in self.segment_access:
            return -1
        return self.segment_access[segment_id]
    
    def _modify(self, segment_id, content):
        if content == '/delete':
            del self.segment_content[segment_id]
        else:
            self.segment_content[segment_id] = content
        return "Success"
    
    def _read_content(self, segment_id):
        if segment_id not in self.segment_content:
            return None
        
        content = self.segment_content[segment_id]
        
        if isinstance(content, list):
            # If the content is a list of segment IDs, recursively read each segment
            character_content = ""
            for sub_segment_id in content:
                sub_content = self._read_content(sub_segment_id)
                if sub_content is not None:
                    character_content += sub_content
            return character_content
        else:
            # If the content is a string, return it as the character content
            return content
        
    def _read_ID(self, segment_id):
        if segment_id not in self.segment_content:
            return None

        content = self.segment_content[segment_id]
        if not isinstance(content, list):
            content = [content]
        return content
    
    def _allocate(self):
        timestamp = str(int(time.time() * 1000))  # Get current timestamp in milliseconds
        random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=8))  # Generate 8 random characters
        segment_id = f"{timestamp}_{random_chars}"  # Combine timestamp and random characters
        self.segment_content[segment_id] = ""
        return segment_id
