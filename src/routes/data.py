from fastapi import FastAPI,APIRouter,Depends,UploadFile,status,Request,File,HTTPException
from fastapi.responses import JSONResponse
from models import ResponseSignal
import aiofiles  #file cunks
import os
import logging
from helper.config import get_settings,Settings
from controllers import DataController,ProjectController,ProcessController
from .schemes.ProcessRequest import ProcessRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunks



logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"],
)

# Instantiate the controller
data_controller = DataController()
project_controller = ProjectController()

@data_router.post("/upload/{project_id}") # endpoint
# upload_data will tack file_id with type string,uploaded file
async def upload_data(request:Request,project_id:str,file:UploadFile,app_settings:Settings =Depends(get_settings)):
    
    project_model= ProjectModel(db_client=request.app.db_client)

    project= await project_model.get_project_or_create_one(project_id=project_id)

    # validate file properties
    is_valid,result_signal = data_controller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": str(result_signal.value),
            }
        )
    
    # use ProjectController to get the path and name of file that you want to store it in which directory
    #project_dir_path = project_controller().get_project_path(project_id=file_id)
    file_path,generated_file_name = data_controller.generate_unique_filename(
        orig_file_name=file.filename,
        project_id=project_id
    )
    try:
        # start take chunks and store it in file path
        # wb weriting as binary =>open this file as binary 
        # Start taking chunks and store them in the file path
        async with aiofiles.open(file_path, "wb") as f:
            # Read chunks of the file in the specified chunk size
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)      

    # error while uploading the file                 
    except Exception as e:
        logger.error(f"error while uploading the file :{e}")
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.FILL_FAILED_upload.value
                }
        )

    # FILL_Success_upload
    return JSONResponse(
                content={
                    "signal": ResponseSignal.FILL_Success_upload.value,
                    "unique file name":generated_file_name,
                    "Projecct":str(project._id)
                }
            )

# new endpoint
@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request,project_id:str,ProcessRequest:ProcessRequest):

    # to get project id 
    chunk_model= ProjectModel(db_client=request.app.db_client)
    project= await chunk_model.get_project_or_create_one(project_id=project_id)

    file_id=ProcessRequest.file_id
    chunk_size=ProcessRequest.chunk_size
    overlap_size=ProcessRequest.overlab_size
    do_reset = ProcessRequest.do_reset


    process_cotroller=ProcessController(project_id=project_id)
    file_content = process_cotroller.get_file_content(file_id=file_id)

    file_chunks=process_cotroller.process_file_content(
        file_contnet=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        chunk_overlap=overlap_size,
    )

    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.PROCESSING_FAILED.value
                }
        )
    
    # use chunkModel
    # convert chunks into ChunkModel object to take the form of it before store it in database
    file_chunks_records=[
        DataChunks(
            chunk_text=chunk.page_content,
            cunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id =project.id
        )
        for i,chunk in enumerate(file_chunks)
    ]
    # connect to database to delete or insert
    chunk_model=ChunkModel(db_client=request.app.db_client)

    # delete the chunks if the user enter the same id so delete the old and insert new

    _ = await chunk_model.delete_chunks_by_project_id(
        project_id=project.id
    )

    # after create chunks send theme to stores in data base 
    no_records = await chunk_model.create_many_chunks(chunks=file_chunks_records)
    
    # FILL_Success_upload
    return JSONResponse(
                content={
                    "signal": ResponseSignal.FILL_Success_upload.value,
                    "number of inserted chunks":no_records,
                    "Projecct":str(project.id)
                }
            )


# tast function for test any think
@data_router.post("/test/{file_id}")
async def create_upload_file(file: UploadFile=File(...)):
    return {"filename": file.filename}
  