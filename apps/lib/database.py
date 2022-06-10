# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-08 17:23
@log     ：
            author datetime(DESC) summary
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

file_path = os.path.abspath(os.getcwd())

SQLALCHEMY_DATABASE_URL = f"sqlite:///{file_path}/FastAPI-demo.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, encoding='utf-8', connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    得到对数据库的链接
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()