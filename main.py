# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-08 16:26
@log     ：
            author datetime(DESC) summary
"""
from __future__ import absolute_import
import uvicorn
from apps import app


if __name__ == '__main__':
    uvicorn.run(app, port=5000, host="0.0.0.0")
