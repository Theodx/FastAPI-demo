# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-09 10:51
@log     ：
            author datetime(DESC) summary
"""
import secrets
from pydantic import BaseSettings



class Settings(BaseSettings):

    # JWTtoken相关
    ALGORITHM: str = "HS256"  # 加密算法
    # SECRET_KEY: str = secrets.token_urlsafe(32)  # 随机生成的base64位字符串
    SECRET_KEY: str = "2vUgiZ_C4hliwVq9rtRqsxKVsX3o3RaQfSo1SSwR2MU"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3  # token的时效 3 天 = 60 * 24 * 3


settings = Settings()