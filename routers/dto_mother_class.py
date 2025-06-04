from pydantic import BaseModel
from enum import Enum

class ResponseStatus(Enum):
    FAIL = "fail"
    SUCCESS = "success"


class ResponseDto(BaseModel):
    status: ResponseStatus
    message: str
    data: dict