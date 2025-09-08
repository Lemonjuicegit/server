from sqlmodel import SQLModel
from fastapi import HTTPException
class ErrorCode(SQLModel):
    code: int  = 0
    msg:str = ""
class ERR:
    SUCCESS: ErrorCode = ErrorCode()
    BAD_REQUEST: ErrorCode = ErrorCode(code=400, msg="请求参数错误")
    NO_ACCESS_RIGHTS = HTTPException(status_code=401,detail="设备无权访问")
    FORBIDDEN = HTTPException(status_code=403, detail="Token 已过期")
    NOT_FOUND:ErrorCode = ErrorCode(code=404, msg="请求的资源不存在")
    METHOD_NOT_ALLOWED:ErrorCode = ErrorCode(code=405, msg="请求方法不允许")
    LOCKED:ErrorCode = ErrorCode(code=423, msg="请求失败，请稍后重试")
    TOO_MANY_REQUESTS:ErrorCode = ErrorCode(code=429, msg="请求次数过多，请稍后重试")
    INTERNAL_SERVER_ERROR:ErrorCode = ErrorCode(code=500, msg="服务器内部错误")
    REPEATED_REQUESTS:ErrorCode = ErrorCode(code=409, msg="请求重复")
    UNKNOWN:ErrorCode = ErrorCode(code=999, msg="未知错误")
