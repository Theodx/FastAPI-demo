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
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
    init_router(app)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app


app = create_app()
templates = Jinja2Templates(directory="templates")