from fastapi import Request

from fastapi.responses import JSONResponse
from readMenuitemURL import config

async def check_static_access(request: Request, call_next):
    if request.url.path[1:] in config.re_routerName:
        return JSONResponse(
            content={"detail": "Static content access disabled."}, status_code=404
        )
    print(request)
    response = await call_next(request)
    return response

def add_middleware(app):
    middleware_list = [check_static_access]
    for middleware in middleware_list:
        app.add_middleware(middleware)
