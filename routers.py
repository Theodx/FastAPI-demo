# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-08 16:26
@log     ：
            author datetime(DESC) summary
"""
from __future__ import absolute_import

from apps.controllers.user import users_router


def init_router(app):
    """
    初始化路由
    :param app:
    :return:
    """
    app.include_router(users_router, prefix='/users')
