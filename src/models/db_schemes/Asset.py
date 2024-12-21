from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime


class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id") #id of mongodb we will use bson.ObjectId to deal with it in python
    asset_project_id: ObjectId
    asset_type: str = Field(..., min_length=1) # type of asset in our project will be file
    asset_name: str = Field(..., min_length=1) 
    asset_size: int = Field(ge=0, default=None) #size in mb of file and it must be grater than 0
    asset_config: dict = Field(default=None) # if we have config later
    asset_pushed_at: datetime = Field(default=datetime.utcnow) #we will not enter the data so it will take by defualt the current data

    class Config:
        arbitrary_types_allowed = True
    
    # create indexing for asset
    @classmethod
    def get_indexes(cls):

        return [
            # for searching by only asset_project_id 
            {
                "key": [
                    ("asset_project_id", 1)
                ],
                "name": "asset_project_id_index_1",
                "unique": False
            },

            # for searchin by asset_project_id and asset_name togther
            {
                "key": [
                    ("asset_project_id", 1),
                    ("asset_name", 1)
                ],
                "name": "asset_project_id_name_index_1",
                "unique": True
            },
        ]

