from .BaseDataModel import BaseDataModel
from .enums import DataBaseEnum
from .db_schemes import Asset
from .enums import AssetTypeEnum
from bson.objectid import ObjectId   

class AssetModel(BaseDataModel):

    def __init__(self,db_client:object):
        super().__init__(db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
    
    # function to add __init__ =>not asynch and init_collection =>asynch must have await
    @classmethod
    async def create_instance(cls,db_client:object):  # __init__(self,db_client:object)
        instance = cls(db_client)  # take an object from DataChunkModel and now it is have all values and functions of it
        await instance.init_collection()
        return instance
    
    # check if there is an connectio or not if not create one
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )
        
    async def create_asset(self, asset: Asset):

        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True))
        asset.id = result.inserted_id

        return asset