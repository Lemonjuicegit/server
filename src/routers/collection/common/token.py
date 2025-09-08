import jwt
from fastapi import Header, Request
from ..ErrorCode import ERR
from src.routers.collection.service import deviceIpService
from datetime import datetime, timedelta

SECRET_KEY = "jiayu"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ip_list = deviceIpService.getIpList()

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=180)):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(req: Request):
    ip = req.client.host
    if ip not in ip_list:
        raise ERR.NO_ACCESS_RIGHTS
    else:
        token: str = req.headers.get("Token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if 'ip' not in payload:
            raise ERR.NO_ACCESS_RIGHTS
        if payload['ip'] != ip:  
            raise ERR.NO_ACCESS_RIGHTS 
    except jwt.ExpiredSignatureError:
        raise ERR.FORBIDDEN
    except jwt.InvalidTokenError:  
        raise ERR.NO_ACCESS_RIGHTS
    
    return ip