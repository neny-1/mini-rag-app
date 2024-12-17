from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    file_id:str
    chunk_size:Optional[int]=100  # make it Optional from user if user dont enter it make defualt 100 byte
    overlab_size:Optional[int]=20
    do_reset:Optional[int]=0  # do =>action baset on this varibael
