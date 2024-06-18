from enum import Enum


class StatusCode(Enum):
    Unknown = -1
    Success = 0
    Finished = 1
    StopSignal = 2
    LoadConfigError = 3
    

class HttpCode(Enum):
    Continue = 100
    Ok = 200
    BadRequest = 400
    Gone = 410
    ServiceUnvaliable = 503
