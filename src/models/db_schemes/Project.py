from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId


# this class is for validate project id
class Project (BaseModel):
    id:Optional[ObjectId]=Field(None,alias="_id")  # this id generated by mongogdb of type ObjectId and it can be Optional
    project_id:str = Field(...,min_length=1) #>mini char must be 1

    # create manualy validation set the project_id properties
    @validator("project_id")
    def validate_project_id(cls,value):
        if not value.isalnum(): # if the vlaue of project id not alphanumeric output error message
            raise ValueError("Project_id must be alphanumeric")
        return value
    
    # to avoid error of miss understnding in type of the _id here => _id:Optional[ObjectId]  so allow if there is error in type
    class Config:
        arbitrary_types_allowed = True
    
    @classmethod
    def get_indexes(cls):
        return[
            {
                "key": [("project_id",1)], # 1 means asc order -1 means desc
                "name":"project_id_index_1",  #the name of collection it can be any name
                "unique":True # project_id must be unique
                
            }
        ]