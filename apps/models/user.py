# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-09 10:22
@log     ：
            author datetime(DESC) summary
"""
from __future__ import absolute_import

from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session

from apps.core.security import verify_password
from apps.lib.database import Base
from apps.schemas import schemas_user
from apps.core import security


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), index=True, comment='名称')
    email = Column(String(100), unique=True, index=True, nullable=False, comment='邮箱')
    hashed_password = Column(String(100), nullable=False, comment='密码')
    is_active = Column(Boolean(), default=True, comment='是否活跃')
    is_superuser = Column(Boolean(), default=False, comment='是否超级管理员')
    # items = relationship('Item', back_populates='owner')

    created_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='最后一次更新时间')

    def __repr__(self):
        return f'{self.id}_{self.email}'

    @staticmethod
    async def get_user_by_email(db: Session, email: str):
        """
        通过邮箱查找用户
        :param db:
        :param email: 用户的邮箱
        :return:
        """
        db_user = db.query(User).filter_by(email=email).first()
        return db_user

    @staticmethod
    async def get_user_by_id(db: Session, user_id: int):
        """
        通过邮箱查找用户
        :param db:
        :param user_id: 用户的主键id
        :return:
        """
        db_user = db.query(User).filter_by(id=user_id).first()
        return db_user

    @staticmethod
    async def create_user(db: Session, user_info: schemas_user.UserInDB):
        """
        创建用户
        :param db:
        :param user_info: 用户的基础信息
        :return:
        """
        fake_hashed_password = security.get_password_hash(user_info.password)
        db_user = User(
            email=user_info.email,
            full_name=user_info.full_name,
            hashed_password=fake_hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    async def authenticate_user(db: Session, username: str, password: str):
        """
        对用户密码进行校验
        :param db:
        :param username: 用户的账号
        :param password: 用户的密码
        :return:
        """
        db_user = await User.get_user_by_email(db, username)
        if not db_user:
            return False
        if not verify_password(password, db_user.hashed_password):
            return False
        return db_user