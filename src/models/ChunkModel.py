from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunks
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId   
from pymongo import InsertOne 


class ChunkModel(BaseDataModel):

    def __init__(self, db_client:object):
        super().__init__(db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_chunk(self,chunk:DataChunks):
        result = await self.collection.insert_one(chunk.dict(by_alias=True,exclude_unset=True)) # chunk.dict() whene insert data in data base convert it to diectionery
        chunk._id =result.inserted_id
        return chunk

    async def get_chunk(self,chunk_id:str):
        result = await self.collection.find_one({"_id",ObjectId(chunk_id)}) # _id stores in database in ObjectId form so we must convert it to check if exist ot not
        if result is None:
            return "there is no _id for this chunk"
        return DataChunks(**result)         # to return result return it in form of DataChunks object to take its varibles and **result to convert it from dict() or te form that came from database
    
    # range(from,to,step =>0,1000,100) =>10 iteraction from 0 to 1000 each time take 100 so 0=>100 ,100=>200,200=>300
    # انا بكون عايز اخد الداتا زي بالك كدا يعني عشان دي طريقة احسن للتعامل مع الداتا بيز
    async def create_many_chunks(self,chunks:list,batch_size=100):

        for i in range(0,len(chunks),batch_size):
            batch =chunks[i:i+batch_size] # batch[0] = chunks[0:100] ...

            operations=[
                InsertOne(chunk.dict(by_alias=True,exclude_unset=True))
                for chunk in batch      # loop over each batch[0]=chunks[0:100] and store this bulk in the operations
            ]

        await self.collection.bulk_write(operations) # send the stored values of operations into data base collection

        return len(chunks)
    
    # delete the chunks for this project id if the usere enter reset = 1
    async def delete_chunks_by_project_id(self,project_id:ObjectId):
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })
        
        if result.deleted_count >0:
            return {f"deleted {result.deleted_count}"}
        return "there is no deleted cunk"

    
