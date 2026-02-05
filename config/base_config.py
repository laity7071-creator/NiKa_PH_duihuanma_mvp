#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 18:42
@文件名: base_config.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/config\base_config.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
import os
from dotenv import load_dotenv
from typing import Optional
from config.env_config.dev_config import DevConfig
from config.env_config.test_config import TestConfig
from config.env_config.prod_config import ProdConfig

# 加载.env环境变量（优先读取环境变量，其次读取配置文件）
load_dotenv()


class BaseConfig:
    """基础配置类：加载环境、切换配置"""
    # 当前环境（通过.env文件指定，默认test）
    ENV = os.getenv("RUN_ENV", "test")

    @classmethod
    def get_env_config(cls):
        """根据当前环境获取对应配置"""
        env_map = {
            "dev": DevConfig,
            "test": TestConfig,
            "prod": ProdConfig
        }
        if cls.ENV not in env_map:
            raise ValueError(f"不支持的环境：{cls.ENV}，仅支持dev/test/prod")
        return env_map[cls.ENV]()


# 初始化当前环境配置（全局可调用）
current_config = BaseConfig.get_env_config()