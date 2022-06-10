# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-09 17:20
@log     ：
            author datetime(DESC) summary
"""
from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status
from starlette.responses import JSONResponse

from config.setting import settings

white_paths = [
    "/users/login",  # 登入
    "/docs",
    "/openapi.json"
]


def request_id_middleware(app):
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        response = JSONResponse(
            content={"message": "Token错误"},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        path = request.url.path
        if path in white_paths:
            pass
        else:
            authorization = request.headers.get("authorization")
            if not authorization or not authorization.lower().startswith("bearer"):
                return response
            token = await OAuth2PasswordBearer(tokenUrl="/token")(request)
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                user_id = payload.get("user_id")
                if not user_id:
                    return response
            except JWTError:
                return response
            setattr(request.state, "user_id", user_id)
        return await call_next(request)
