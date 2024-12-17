from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import os
import re
class DataController(BaseController):

    def __init__(self):

        # call __init__() from BaseController if self.__init__() call .__init__() of DataController cause self 
        super().__init__()

        # we get file from user with byets but will but file_max_size with MB 
        self.size_scale = 104875  # convert MB to byets


    # tell function that the file will be of type UploadFile
    # validate duplicate file name and 
    def validate_uploaded_file(self, file: UploadFile):
        
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPE:
            return False,ResponseSignal.FILE_TYPE_NOT_SUPPORTED
        
        if file.size > self.app_settings.FILE_MAX_SIZE*self.size_scale:
            return False,ResponseSignal.FILE_SIZE_NOT_ALLWOEDT
        return True ,ResponseSignal.FILL_Success_upload
    
    def generate_unique_filename(self,orig_file_name:str,project_id:str):

        randome_key = self.generate_random_string()
        project_dir = ProjectController().get_project_path(project_id=project_id)

        cleaned_file_name= self.get_clean_file_name(orig_file_name=orig_file_name)

        new_file_path=os.path.join(
            project_dir,
            randome_key+"_"+cleaned_file_name
        )

        # if new_file_path exist so we will make new random name
        while os.path.exists(new_file_path):
            randome_key = self.generate_random_string()

            new_file_path=os.path.join(
            project_dir,
            randome_key+"_"+cleaned_file_name
        )

        return new_file_path,randome_key+"_"+cleaned_file_name
    
    # make regulr expression to clean file name
    def get_clean_file_name(self, orig_file_name: str):

        # remove any special characters, except underscore and .
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # replace spaces with underscore
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name
