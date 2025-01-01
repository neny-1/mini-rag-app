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
from models.AssetModel import AssetModel
from models.db_schemes import DataChunks, Asset
from models.enums.AssetTypeEnum import AssetTypeEnum



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
    
    project_model= await ProjectModel.create_instance(db_client=request.app.db_client)

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
    file_path,file_id = data_controller.generate_unique_filename(
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

    # store the assets into the database
    asset_model = await AssetModel.create_instance(
        db_client=request.app.db_client
    )

    asset_resource = Asset(
        asset_project_id=project.id,
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )

    asset_record = await asset_model.create_asset(asset=asset_resource)

    return JSONResponse(
            content={
                #"file_name": asset_record.asset_project_id,
                "signal": ResponseSignal.FILL_Success_upload.value,
                "file_id": str(asset_record.id),
            }
        )

# new endpoint
@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):

    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    asset_model = await AssetModel.create_instance(
            db_client=request.app.db_client
        )

    project_files_ids = {}
    if process_request.file_id:
        asset_record = await asset_model.get_asset_record(
            asset_project_id=project.id,
            asset_name=process_request.file_id
        )

        if asset_record is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.FILE_ID_ERROR.value,
                }
            )

        project_files_ids = {
            asset_record.id: asset_record.asset_name
        }
    
    else:
        
        project_files = await asset_model.get_all_project_assets(
            asset_project_id=project.id,
            asset_type=AssetTypeEnum.FILE.value,
        )

        project_files_ids = {
            record.id: record.asset_name
            for record in project_files
        }

    if len(project_files_ids) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.NO_FILES_ERROR.value,
            }
        )
    
    process_controller = ProcessController(project_id=project_id)

    no_records = 0
    no_files = 0

    chunk_model = await ChunkModel.create_instance(
                        db_client=request.app.db_client
                    )

    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )

    for asset_id, file_id in project_files_ids.items():

        file_content = process_controller.get_file_content(file_id=file_id)

        if file_content is None:
            logger.error(f"Error while processing file: {file_id}")
            continue

        file_chunks = process_controller.process_file_content(
            file_content=file_content,
            file_id=file_id,
            chunk_size=chunk_size,
            chunk_overlap=overlap_size
        )

        if file_chunks is None or len(file_chunks) == 0:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.PROCESSING_FAILED.value
                }
            )

        file_chunks_records = [
            DataChunks(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunk_project_id=project.id,
                chunk_asset_id=asset_id
            )
            for i, chunk in enumerate(file_chunks)
        ]

        no_records += await chunk_model.insert_many_chunks(chunks=file_chunks_records)
        no_files += 1

    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records,
            "processed_files": no_files
        }
    )
# tast function for test any think
@data_router.post("/test/{file_id}")
async def create_upload_file(file: UploadFile=File(...)):
    return {"filename": file.filename}
  