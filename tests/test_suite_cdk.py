#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 18:45
@文件名: test_suite_cdk.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/tests\test_suite_cdk.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
import pytest
from typing import Dict
from core.cdk_manage.test_cdk_generate import TestCdkGenerate
from core.cdk_manage.test_cdk_redeem import TestCdkRedeem
from core.cdk_manage.test_batch_operate import TestBatchOperate


@pytest.mark.cdk
@pytest.mark.run(order=1)
def test_cdk_generate(init_test_env: Dict):
    """测试1：CDK生成（正常批次+大数量批次）"""
    env = init_test_env
    cdk_generate = TestCdkGenerate()

    # 执行正常批次生成测试
    normal_result = cdk_generate.test_normal_cdk_generate()
    # 存储批次ID和CDK到环境变量（供后续测试复用）
    env["batch_id"] = normal_result["data"]["batch_id"]
    env["test_cdk"] = normal_result["data"]["cdk_list"][0]

    # 执行大数量批次生成测试（可选，根据测试需求启用）
    # cdk_generate.test_large_scale_cdk_generate()


@pytest.mark.cdk
@pytest.mark.run(order=2)
def test_cdk_redeem(init_test_env: Dict):
    """测试2：CDK核销（正常核销+重复核销+过期/禁用核销）"""
    env = init_test_env
    # 初始化核销测试类
    cdk_redeem = TestCdkRedeem(env["admin_client"])
    # 构造核销参数（复用生成的CDK）
    redeem_params = env["test_data"]["redeem_params"]["normal_redeem"]
    redeem_params["cdk"] = env["test_cdk"]

    # 执行正常核销测试
    cdk_redeem.test_normal_redeem(redeem_params)

    # 执行重复核销测试
    cdk_redeem.test_duplicate_redeem(redeem_params)

    # 执行禁用批次核销测试（先禁用批次，再核销）
    batch_operate = TestBatchOperate(env["admin_client"])
    batch_operate.disable_batch(env["batch_id"])
    cdk_redeem.test_disabled_batch_redeem(redeem_params)

    # 恢复批次状态（避免影响后续测试）
    batch_operate.enable_batch(env["batch_id"])


@pytest.mark.cdk
@pytest.mark.run(order=3)
def test_batch_operate(init_test_env: Dict):
    """测试3：批次管理（状态切换、导出、搜索）"""
    env = init_test_env
    batch_operate = TestBatchOperate(env["admin_client"])

    # 测试批次状态切换（启用→禁用→启用）
    batch_operate.test_batch_status_switch(env["batch_id"])

    # 测试批次导出（CSV格式）
    batch_operate.test_batch_export(env["batch_id"])

    # 测试按CDK ID搜索批次
    batch_operate.test_search_batch_by_cdk(env["test_cdk"])