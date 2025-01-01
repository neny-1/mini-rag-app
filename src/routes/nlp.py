from fastapi import FastAPI,APIRouter,Request
from fastapi.responses import JSONResponse
from models import ResponseSignal
from routes.schemes.nlp import PushRequest,SearchRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from controllers import NLPController
from models import ResponseSignal
import logging
from fastapi import status
logger = logging.getLogger('uvicorn.error')

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1","nlp"],
)

@nlp_router.post("/index/push/{project_id}") # endpoint
async def index_project(request:Request,project_id:str,push_request:PushRequest):

    project_model= await ProjectModel.create_instance(db_client=request.app.db_client)
    chunk_model= await ChunkModel.create_instance(db_client=request.app.db_client)  

    project= await project_model.get_project_or_create_one(project_id=project_id)

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal":ResponseSignal.PROJECT_NOT_FOUND.value
            })
    
    nlp_controller=NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
    )

    has_records = True
    page_no = 1
    inserted_items_count = 0
    idx = 0

    while has_records:

        # get all chunks for this project id =>use pagination
        page_chunks = await chunk_model.get_project_chunks(project_id=project.id,page_num=page_no)
        if len(page_chunks):
            page_no += 1
        if not page_chunks or len(page_chunks) == 0:
            has_records = False
            break

        chunks_ids=list(range(idx,idx+len(page_chunks)))
        idx += len(page_chunks)
        
        # store chunks or index into vector db
        inserted = nlp_controller.index_into_vector_db(
            project=project,
            chunks_ids=chunks_ids,
            data_chunks=page_chunks,
            do_reset=push_request.do_reset
        )

        if not inserted:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "Signal":ResponseSignal.INSERT_INTO_VECTOR_DB_FAILED.value
                })
        inserted_items_count += len(page_chunks)
    return JSONResponse(
        content={
            "Signal":ResponseSignal.INSERT_INTO_VECTOR_DB_SUCCESS.value,
            "inserted_items_count":inserted_items_count
        })

@nlp_router.get("/index/info/{project_id}") # endpoint
async def get_project_index_info(request:Request,project_id:str):

    project_model= await ProjectModel.create_instance(db_client=request.app.db_client)
    chunk_model= await ChunkModel.create_instance(db_client=request.app.db_client)  

    project= await project_model.get_project_or_create_one(project_id=project_id)

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal":ResponseSignal.PROJECT_NOT_FOUND.value
            })
    
    nlp_controller=NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
    )

    collection_info = nlp_controller.get_vector_db_collection_info(project=project)

    return JSONResponse(
        content={
            "Signal":ResponseSignal.GET_COLLECTION_INFO_SUCCESS.value,
            "collection_info":collection_info
        })

@nlp_router.post("/index/search/{project_id}") # endpoint
async def search_project(request:Request,project_id:str,search_request:SearchRequest):

    project_model= await ProjectModel.create_instance(db_client=request.app.db_client)
    chunk_model= await ChunkModel.create_instance(db_client=request.app.db_client)  

    project= await project_model.get_project_or_create_one(project_id=project_id)

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal":ResponseSignal.PROJECT_NOT_FOUND.value
            })
    
    nlp_controller=NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client,
    )

    search_results = nlp_controller.search_vector_db_collection(
        project=project,
        query=search_request.query,
        limit=search_request.limit
    )

    if not search_results:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal":ResponseSignal.VECTOR_SEARCH_FAILED.value
            })
    return JSONResponse(
        content={
            "Signal":ResponseSignal.VECTOR_SEARCH_SUCCESS.value,
            "search_results":search_results
        })
    