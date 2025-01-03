from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED ="This file type is not supported"
    FILE_SIZE_NOT_ALLWOEDT ="This file size is not allowed"
    FILL_Success_upload ="Success upload the file "
    FILL_FAILED_upload="Failed to upload the file"
    PROCESSING_SUCCESS="Processing success"
    PROCESSING_FAILED="Processing failed"
    PROJECT_NOT_FOUND="Project not found"
    INSERT_INTO_VECTOR_DB_SUCCESS="Insert into vector db success"
    INSERT_INTO_VECTOR_DB_FAILED="Insert into vector db failed"
    FILE_ID_ERROR ="File id error"
    NO_FILES_ERROR="No files with this id found"
    GET_COLLECTION_INFO_SUCCESS="Get collection info success"
    VECTOR_SEARCH_FAILED="Search failed"
    VECTOR_SEARCH_SUCCESS="Search success"
    ANSWER_GENERATION_FAILED="Answer generation failed"
    ANSWER_GENERATION_SUCCESS="Answer generation success"