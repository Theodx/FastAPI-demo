# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-09 10:43
@log     ：
            author datetime(DESC) summary
"""
from __future__ import absolute_import

from fastapi import APIRouter, Request, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from apps.core.security import create_access_token, verify_token
from apps.schemas import schemas_user
from apps.lib.database import get_db
from apps.models.user import User

users_router = APIRouter()


@users_router.post("/register/", response_model=schemas_user.UserOut)
async def create_user(user_info: schemas_user.UserInDB, db: Session = Depends(get_db)):
    """
    注册
    :param user_info: 用户注册信息
    :param db:
    :return:
    """
    db_user = await User.get_user_by_email(db, email=user_info.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已被注册")
    return await User.create_user(db=db, user_info=user_info)


@users_router.post("/login/")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    用户登入
    :param request:
    :param form_data: 用户账号和密码
    :param db:
    :return:
    """
    user = await User.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"user_id": user.id, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@users_router.get("/current_user/", response_model=schemas_user.UserOut, dependencies=[Depends(verify_token)])
async def current_user(request: Request, db: Session = Depends(get_db)):
    """
    查询用户信息
    :param request:
    :param db:
    :return:
    """
    user_id = getattr(request.state, "user_id")
    db_user = await User.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="找不到用户")
    return db_user


@users_router.put("/password/forget/")
async def forget_password(body: schemas_user.ForgetPassword, db: Session = Depends(get_db)):
    """
    忘记密码
    :param body:
    :param db:
    :return:
    """
    await User.forget_password(db, body)
    return {}


@users_router.put("/password/reset/", dependencies=[Depends(verify_token)])
async def reset_password(request: Request, body: schemas_user.ResetPassword, db: Session = Depends(get_db)):
    """
    重制密码
    :param request:
    :param body:
    :param db:
    :return:
    """
    user_id = getattr(request.state, "user_id")
    await User.reset_password(db, body, user_id)
    return {}