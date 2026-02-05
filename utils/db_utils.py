#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 18:43
@文件名: db_utils.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/utils\db_utils.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
import pymysql
from pymysql.cursors import DictCursor  # 补充游标导入
from typing import Dict, Optional, List
from config.db_config import DBConfig
from utils.log_utils import logger


class DBClient:
    """数据库操作客户端（连接池、查询、校验）"""
    _instance = None  # 单例模式，避免重复创建连接

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_conn()
        return cls._instance

    def _init_conn(self):
        """初始化数据库连接（从配置获取信息）"""
        self.db_info = DBConfig.get_db_info()
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self):
        """创建数据库连接"""
        try:
            # 修正游标配置（直接使用DictCursor）
            self.conn = pymysql.connect(
                **self.db_info,
                cursorclass=DictCursor  # 明确指定游标类型
            )
            self.cursor = self.conn.cursor()
            logger.info("数据库连接成功")
        except pymysql.err.OperationalError as e:
            logger.error(f"数据库连接失败：{str(e)}")
            raise

    def _reconnect(self):
        """连接断开时自动重连"""
        logger.info("数据库连接断开，尝试重连...")
        self._init_conn()

    def query_one(self, sql: str, args: Optional[tuple] = None) -> Optional[Dict]:
        """
        执行查询（返回单条结果）
        :param sql: 查询SQL
        :param args: SQL参数（避免SQL注入）
        :return: 单条结果字典
        """
        try:
            if not self.conn.ping():
                self._reconnect()
            self.cursor.execute(sql, args)
            result = self.cursor.fetchone()
            logger.info(f"执行SQL：{sql} | 参数：{args} | 结果：{result}")
            return result
        except Exception as e:
            logger.error(f"查询失败：{str(e)} | SQL：{sql} | 参数：{args}")
            raise

    def query_all(self, sql: str, args: Optional[tuple] = None) -> List[Dict]:
        """执行查询（返回多条结果）"""
        try:
            if not self.conn.ping():
                self._reconnect()
            self.cursor.execute(sql, args)
            result = self.cursor.fetchall()
            logger.info(f"执行SQL：{sql} | 参数：{args} | 结果条数：{len(result)}")
            return result
        except Exception as e:
            logger.error(f"查询失败：{str(e)} | SQL：{sql} | 参数：{args}")
            raise

    def verify_data(self, sql: str, args: Optional[tuple], expected: Dict) -> bool:
        """
        数据校验（查询结果与预期对比）
        :param sql: 查询SQL
        :param args: SQL参数
        :param expected: 预期结果（如{"status": "已使用", "user_id": "test_001"}）
        :return: 校验通过返回True，否则抛出异常
        """
        result = self.query_one(sql, args)
        if not result:
            raise Exception(f"未查询到对应数据：SQL={sql}，参数={args}")

        # 逐字段对比预期与实际结果
        for key, expected_val in expected.items():
            actual_val = result.get(key)
            if actual_val != expected_val:
                raise Exception(
                    f"数据校验失败：字段[{key}]，预期[{expected_val}]，实际[{actual_val}]"
                )
        logger.info(f"数据校验通过：预期{expected}，实际{result}")
        return True

    def __del__(self):
        """销毁时关闭连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        logger.info("数据库连接已关闭")


# 全局数据库客户端实例（直接导入使用，无需重复创建）
db_client = DBClient()