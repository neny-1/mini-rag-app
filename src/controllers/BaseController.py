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

    # we will use this function in DataController
    def generate_random_string(self, length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
