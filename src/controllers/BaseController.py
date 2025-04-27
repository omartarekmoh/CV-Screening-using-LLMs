from helpers.config import get_settings, Settings
import os
import random
import string

class BaseController:
    def __init__(self):
        
        self.app_settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__)) 
        self.file_dir = os.path.join(
            self.base_dir, 
            "assets/files"
        )
        
    def generate_random_string(self, length: int = 12):
        chars = string.ascii_letters + string.digits  # letters + 0-9
        return ''.join(random.choice(chars) for _ in range(length))