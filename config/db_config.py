#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 18:43
@文件名: db_config.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/config\db_config.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
from config.base_config import current_config
from typing import Dict


class DBConfig:
    """数据库配置（与当前环境绑定）"""

    @classmethod
    def get_db_info(cls) -> Dict:
        """获取数据库连接信息（从环境变量或配置文件读取）"""
        return {
            "host": current_config.DB_HOST,
            "user": current_config.DB_USER,
            "password": current_config.DB_PWD,
            "db": current_config.DB_NAME,
            "port": current_config.DB_PORT,
            "charset": "utf8mb4"
            # 游标类型已在DBClient中指定，此处无需重复配置
        }