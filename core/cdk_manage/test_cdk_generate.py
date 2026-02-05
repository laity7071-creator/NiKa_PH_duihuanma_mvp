#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 18:44
@文件名: test_cdk_generate.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/core/cdk_manage\test_cdk_generate.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
import json
import os
from typing import Dict, List
from core.cdk_manage import test_cdk_data
from utils.request_utils import RequestClient
from utils.data_utils import DataValidator
from utils.db_utils import db_client
from config.constant import CdkConstant
from utils.log_utils import logger
# 错误导入（可能路径错误）
# from config.constant import CdkConstant, UserConstant
# 正确导入（按项目目录结构）
from config.constant import CdkConstant, UserConstant, ErrorMessage
from utils.log_utils import logger  # 日志工具导入

# 读取测试数据
TEST_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "test_cdk_data.json")
with open(TEST_DATA_PATH, "r", encoding="utf-8") as f:
    test_data = json.load(f)


class TestCdkGenerate:
    """CDK生成测试类（正常生成、大数量生成、格式校验、离散度校验）"""

    def __init__(self):
        self.client = RequestClient(role=CdkConstant.ROLE_ADMIN)  # 管理员角色（仅管理员可创建CDK）
        self.batch_api_path = "/cdk/batch/create"  # 新建批次接口路径（后续替换为真实路径）
        self.batch_id = None  # 测试生成的批次ID（后续复用）
        self.generated_cdks = []  # 生成的CDK列表（用于后续校验）

    def test_normal_cdk_generate(self) -> Dict:
        """测试正常批次CDK生成（参数合法，生成成功）"""
        logger.info("开始执行【正常批次CDK生成】测试")
        # 1. 构造请求参数
        params = test_data["batch_create_params"]["normal_batch"]

        # 2. 调用接口生成批次
        response = self.client.request(method="POST", path=self.batch_api_path, json=params)
        result = response.json()

        # 3. 校验接口响应（状态码、返回字段）
        if result.get("code") != 0:
            raise Exception(f"正常批次生成失败：{result.get('msg', '未知错误')}")

        # 4. 提取批次ID和CDK列表
        self.batch_id = result["data"]["batch_id"]
        self.generated_cdks = result["data"]["cdk_list"]
        logger.info(f"正常批次生成成功：batch_id={self.batch_id}，生成CDK{len(self.generated_cdks)}条")

        # 5. 校验CDK格式（批量）
        DataValidator.batch_check_cdk_format(self.generated_cdks)

        # 6. 校验CDK离散度
        DataValidator.check_cdk_discrete(self.generated_cdks)

        # 7. 数据库校验（批次信息是否同步入库）
        db_client.verify_data(
            sql="SELECT batch_id, agent_id, product_id, status FROM cdk_batch WHERE batch_id = %s",
            args=(self.batch_id,),
            expected={
                "agent_id": params["agent_id"],
                "product_id": params["product_id"],
                "status": CdkConstant.BATCH_STATUS_ENABLE
            }
        )

        logger.info("【正常批次CDK生成】测试执行完成")
        return result

    def test_large_scale_cdk_generate(self) -> Dict:
        """测试大数量CDK生成（10万条，验证系统承载能力）"""
        logger.info("开始执行【大数量CDK生成】测试")
        # 1. 构造请求参数（10万条）
        params = test_data["batch_create_params"]["large_batch"]
        expected_count = params["cdk_count"]

        # 2. 调用接口生成批次（记录耗时）
        import time
        start_time = time.time()
        response = self.client.request(method="POST", path=self.batch_api_path, json=params)
        end_time = time.time()
        generate_duration = end_time - start_time

        # 3. 校验接口响应
        result = response.json()
        if result.get("code") != 0:
            raise Exception(f"大数量批次生成失败：{result.get('msg', '未知错误')}")

        # 4. 校验生成数量
        actual_cdks = result["data"]["cdk_list"]
        if len(actual_cdks) != expected_count:
            raise Exception(
                f"大数量CDK生成数量不符：预期{expected_count}条，实际{len(actual_cdks)}条"
            )

        # 5. 抽样校验格式与离散度（1000条，避免内存溢出）
        sample_cdks = random.sample(actual_cdks, 1000)
        DataValidator.batch_check_cdk_format(sample_cdks)
        DataValidator.check_cdk_discrete(sample_cdks)

        # 6. 校验生成耗时（合理范围内，无超时）
        max_allowed_duration = 300  # 最大允许耗时5分钟（可根据实际调整）
        if generate_duration > max_allowed_duration:
            raise Exception(
                f"大数量CDK生成耗时过长：{generate_duration:.2f}秒，最大允许{max_allowed_duration}秒"
            )

        logger.info(
            f"【大数量CDK生成】测试执行完成：生成{expected_count}条，耗时{generate_duration:.2f}秒"
        )
        return result