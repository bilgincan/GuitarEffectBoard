from pydantic import BaseModel
from enum import Enum

class ResponseStatus(Enum):
    FAIL = 0
    SUCCESS = 1


class ResponseDto(BaseModel):
    status: ResponseStatus
    message: str
    data: BaseModel