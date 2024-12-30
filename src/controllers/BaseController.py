from helper.config import get_settings,Settings
import os
import random
import string

class BaseController:

    #constructor load when code is run no need to call it
    def __init__(self):  
        self.app_settings = get_settings()

        # get the path of files directort and we created it here to us it if needed in another controllers
        self.base_dir = os.path.dirname(os.path.dirname(__file__)) # get the directory name of this file
        self.files_dir = os.path.join(
            self.base_dir,
            "assets/files"
        )

        self.database_dir = os.path.join(
            self.base_dir,
            "assets/database"
        )

    # we will use this function in DataController
    def generate_random_string(self, length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    
    # we will use this function in src/stores/vectordb/VectorDBProviderFactory.py
    def get_database_path(self,database_name:str):
        database_path=os.path.join(self.database_dir,database_name)

        if not os.path.exists(database_path):
            os.makedirs(database_path)
            
        return database_path