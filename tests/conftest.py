#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 18:45
@文件名: conftest.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/tests\conftest.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
import pytest
import json
import os
from typing import Dict
from utils.request_utils import RequestClient
from utils.db_utils import db_client
from config.constant import UserConstant

# 读取测试数据
TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "test_cdk_data.json")
with open(TEST_DATA_PATH, "r", encoding="utf-8") as f:
    test_data = json.load(f)


@pytest.fixture(scope="session")
def init_test_env() -> Dict:
    """
    会话级夹具：初始化测试环境（创建管理员客户端、清理历史测试数据）
    :return: 测试环境变量（客户端、测试数据等）
    """
    logger.info("开始初始化测试环境...")

    # 1. 创建管理员客户端
    admin_client = RequestClient(role=UserConstant.ROLE_ADMIN)

    # 2. 创建代理商客户端
    agent_client = RequestClient(role=UserConstant.ROLE_AGENT)

    # 3. 清理历史测试数据（避免影响本次测试）
    clean_test_data()

    # 4. 返回测试环境变量
    env = {
        "admin_client": admin_client,
        "agent_client": agent_client,
        "test_data": test_data,
        "batch_id": None,  # 后续存储测试生成的批次ID
        "test_cdk": None  # 后续存储测试用CDK
    }

    logger.info("测试环境初始化完成")
    yield env

    # 测试结束后清理测试数据
    logger.info("开始清理测试环境...")
    clean_test_data()
    logger.info("测试环境清理完成")


def clean_test_data():
    """清理历史测试数据（批次、CDK、核销日志）"""
    # 清理测试批次（根据备注筛选）
    test_batch_remarks = ["测试正常批次", "10万条CDK测试批次", "已过期测试批次"]
    for remark in test_batch_remarks:
        # 1. 查询测试批次ID
        batch_ids = db_client.query_all(
            sql="SELECT batch_id FROM cdk_batch WHERE remark = %s",
            args=(remark,)
        )
        if not batch_ids:
            continue

        # 2. 清理CDK核销日志
        batch_id_list = [item["batch_id"] for item in batch_ids]
        db_client.query_one(
            sql=f"DELETE FROM cdk_redeem_log WHERE batch_id IN ({','.join(['%s'] * len(batch_id_list))})",
            args=batch_id_list
        )

        # 3. 清理CDK信息
        db_client.query_one(
            sql=f"DELETE FROM cdk_info WHERE batch_id IN ({','.join(['%s'] * len(batch_id_list))})",
            args=batch_id_list
        )

        # 4. 清理批次信息
        db_client.query_one(
            sql=f"DELETE FROM cdk_batch WHERE batch_id IN ({','.join(['%s'] * len(batch_id_list))})",
            args=batch_id_list
        )

        logger.info(f"清理测试数据：备注={remark}，批次ID={batch_id_list}")