from .BaseDataModel import BaseDataModel
from .db_schemes import Project
#from .enums.ProcessingEnum import ProcessingEnum
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    # get db client for data base connection from parent VaseDataModel from his __init__
    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)
        # store in collection this data 
        self.collection  = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value] # connect to database and get value of project name

    # function to add __init__ =>not asynch and init_collection =>asynch must have await
    @classmethod
    async def create_instance(cls,db_client:object):  # __init__(self,db_client:object)
        instance = cls(db_client)  # take an object from ProjectModel and now it is have all values and functions of it
        await instance.init_collection()
        return instance

    # create function for indexing 
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections: # if there is an collection with this name in database 
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value] # create one
            indexes = Project.get_indexes()
            # store the values in database
            for index in indexes:
                await self.collection.create_index( # create in database and it takes three arg index,name,unique
                    index["key"],
                    name=index["name"],
                    unique=index['unique']
                )

    # insert new project in database
    # insert this project as object from project class to get the scheme or out project struectue
    # insert_one =>from motor   and insert_one takes dectionery
    # motor is async so we use async function 
    # await to wait load data
    async def create_project(self,project:Project):
        result = await self.collection.insert_one(project.dict(by_alias=True,exclude_unset=True))
        project.id = result.inserted_id

        return project
    

    # create new function to check if recored exist or not 
    # if not create one if exist return it but motor return it as dicenorey
    # we will convert it as type project by using project(**recored) => from dict to project 
    async def get_project_or_create_one(self,project_id:str):
        record = await self.collection.find_one({"project_id":project_id})
    
        if record is None:
            #create new recored 
            project = Project(project_id=project_id)  # instance or object from Project class with project_id
            project = await self.create_project(project=project)  # call create_project function to create new project
            return project 
        return Project(**record)
    

    # get all data or project we will use find() from motor but it will get all data and if i have large data it will be un evision memory
    # so we will use cursor from motor like a pointer load docs the it move fro it
    async def get_all_project(self,page:int=1,page_size:int=10):
        # count total numer of documnets
        total_documents = await self.collection.count_documents({})

        # calculate total number of pages
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages+=1

        cursor = self.collection.find().skip((page-1)*page_size).limit(page_size)
        projects=[]
        async for doc in cursor:
            projects.append(Project(**doc))  # **doc from dicetionary to normal text

        return Project,total_pages
        