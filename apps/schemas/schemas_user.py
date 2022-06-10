# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-09 10:42
@log     ：
            author datetime(DESC) summary
"""
from __future__ import absolute_import

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

    class Config:
        orm_mode = True


class UserInDB(User):
    """注册"""
    password: str


class UserOut(User):
    """用户信息输出"""
    id: str
    is_superuser: bool
    created_time: Optional[datetime] = None
    is_active: bool


class ResetPassword(BaseModel):
    """重置登录密码"""
    newPassword: str
    originPassword: str


class ForgetPassword(BaseModel):
    """忘记密码"""
    email: EmailStr
    newPassword: str
    verifyCode: str
