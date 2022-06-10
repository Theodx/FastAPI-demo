# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-09 10:26
@log     ：
            author datetime(DESC) summary
"""
from sqlalchemy import Column, ForeignKey, Integer, String, func, DateTime
from sqlalchemy.orm import relationship
from apps.lib.database import Base


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), index=True, comment='标题')
    description = Column(String(255), comment='描述')
    owner_id = Column(Integer, ForeignKey("user.id"))
    # owner = relationship("User", back_populates="items")

    created_time = Column(DateTime, server_default=func.now(), comment='创建时间')
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment='最后一次更新时间')

    def __repr__(self):
        return f'{self.title}_{self.description}'