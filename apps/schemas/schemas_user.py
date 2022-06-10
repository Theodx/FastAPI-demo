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
from pydantic import BaseModel


class User(BaseModel):
    email: str
    full_name: Optional[str] = None

    class Config:
        orm_mode = True


class UserInDB(User):
    password: str


class UserOut(User):
    id: str
    is_superuser: bool
    created_time: Optional[datetime] = None
    is_active: bool
