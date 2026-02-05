#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/5 09:39
@文件名: test_cdk_redeem.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/core/cdk_manage\test_cdk_redeem.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
from typing import Dict
from utils.request_utils import RequestClient
from utils.db_utils import db_client
from config.constant import CdkConstant, ErrorMessage
from utils.log_utils import logger


class TestCdkRedeem:
    """CDK核销测试（正常/重复/过期/禁用场景）"""

    def __init__(self, client: RequestClient):
        self.client = client
        self.redeem_api_path = "/cdk/redeem"  # 核销接口路径（后续替换为真实路径）

    def redeem_cdk(self, redeem_params: Dict) -> Dict:
        """调用CDK核销接口"""
        response = self.client.request(method="POST", path=self.redeem_api_path, json=redeem_params)
        return response.json()

    def test_normal_redeem(self, redeem_params: Dict) -> Dict:
        """测试正常核销"""
        logger.info(f"执行正常核销测试：CDK={redeem_params['cdk']}")
        result = self.redeem_cdk(redeem_params)
        if result.get("code") != 0:
            raise Exception(f"正常核销失败：{result.get('msg', '未知错误')}")
        # 数据库校验核销状态
        db_client.verify_data(
            sql="SELECT status FROM cdk_info WHERE cdk = %s",
            args=(redeem_params["cdk"],),
            expected={"status": CdkConstant.CDK_STATUS_USED}
        )
        logger.info("正常核销测试通过")
        return result

    def test_duplicate_redeem(self, redeem_params: Dict) -> None:
        """测试重复核销（预期失败）"""
        logger.info(f"执行重复核销测试：CDK={redeem_params['cdk']}")
        # 先正常核销一次
        self.test_normal_redeem(redeem_params)
        # 再次核销
        try:
            self.redeem_cdk(redeem_params)
            raise Exception(f"重复核销未被拦截：CDK={redeem_params['cdk']}")
        except Exception as e:
            if ErrorMessage.CDK_DUPLICATE_REDEEM not in str(e):
                raise Exception(f"重复核销错误提示不符：{str(e)}")
        logger.info("重复核销测试通过")

    def test_disabled_batch_redeem(self, redeem_params: Dict) -> None:
        """测试禁用批次核销（预期失败）"""
        logger.info(f"执行禁用批次核销测试：CDK={redeem_params['cdk']}")
        try:
            self.redeem_cdk(redeem_params)
            raise Exception(f"禁用批次核销未被拦截：CDK={redeem_params['cdk']}")
        except Exception as e:
            if ErrorMessage.CDK_BATCH_DISABLED not in str(e):
                raise Exception(f"禁用批次错误提示不符：{str(e)}")
        logger.info("禁用批次核销测试通过")