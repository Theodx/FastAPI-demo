# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-08 16:27
@log     ：
            author datetime(DESC) summary
"""
from __future__ import absolute_import
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from apps.lib.middlewares import request_id_middleware
from routers import init_router


def create_app():
    """
    创建app
    :return:
    """
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    request_id_middleware(app)
    init_router(app)
    return app


app = create_app()
