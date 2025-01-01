from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    file_id:str = None # make it Optional from user if user dont enter it make defualt None
    chunk_size:Optional[int]=100  # make it Optional from user if user dont enter it make defualt 100 byte
    overlap_size:Optional[int]=20
    do_reset:Optional[int]=0  # do =>action baset on this varibael
