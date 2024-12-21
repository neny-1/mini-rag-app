from enum import Enum

class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED ="This file type is not supported"
    FILE_SIZE_NOT_ALLWOEDT ="This file size is not allowed"
    FILL_Success_upload ="Success upload the file "
    FILL_FAILED_upload="Failed to upload the file"
    PROCESSING_SUCCESS="Processing success"
    PROCESSING_FAILED="Processing failed"
    