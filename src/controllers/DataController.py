from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import os
import re

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024 # convert mb to bytes
    
    def validate_uploaded_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATE_SUCCESS.value
    
    def generate_unique_filepath(self, orig_file_name: str, project_id: str) -> str:
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_file_name = self.get_clean_file_name(orig_file_name=orig_file_name)

        while True:
            random_key = self.generate_random_string()
            new_file_name = f"{random_key}_{cleaned_file_name}"
            new_file_path = os.path.join(project_path, new_file_name)
            
            if not os.path.exists(new_file_path):
                return new_file_path, new_file_name

    
    def get_clean_file_name(self, orig_file_name: str) -> str:
        # First, replace spaces with underscores
        name = orig_file_name.replace(" ", "_")
        # Then, remove any character that is not a letter, number, dot, or underscore
        cleaned_name = re.sub(r"[^\w._]", "", name)
        return cleaned_name