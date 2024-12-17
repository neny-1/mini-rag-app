from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId

class DataChunks(BaseModel):
    id:Optional[ObjectId]=Field(None,alias="_id")  # id generated by mongodb for each chunk and filed
    chunk_text:str =Field(...,min_length=1) # at least 1 char
    cunk_metadata:dict  # of type dictionary 
    chunk_order:int=Field(...,gr=0) #value must be gr =>greater than 0 
    chunk_project_id:ObjectId
 
    # to avoid error of miss understnding in type of the _id here => _id:Optional[ObjectId]  so allow if there is error in type
    class Config:
        arbitrary_types_allowed = True

   