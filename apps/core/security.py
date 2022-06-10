# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-09 11:01
@log     ：
            author datetime(DESC) summary
"""
from __future__ import absolute_import

from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from starlette import status

from config.setting import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    生成token
    :param data: 字典
    :param expires_delta: 有效时间
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    对密码进行校验
    :param plain_password: 明文密码
    :param hashed_password: hash密码
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    加密明文密码
    :param password: 明文密码
    :return:
    """
    return pwd_context.hash(password)


async def verify_token(request: Request):
    """
    token认证
    :param request:
    :param call_next:
    :return:
    """
    response = HTTPException(
        detail="Token错误",
        status_code=status.HTTP_401_UNAUTHORIZED
    )
    authorization = request.headers.get("authorization")
    if not authorization or not authorization.lower().startswith("bearer"):
        raise response
    token = await OAuth2PasswordBearer(tokenUrl="/token")(request)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        if not user_id:
            raise response
    except JWTError:
        raise response
    setattr(request.state, "user_id", user_id)
