#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 18:42
@文件名: test_config.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/config/env_config\test_config.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""


class TestConfig:
    """测试环境配置"""
    # 接口基础URL
    BASE_URL = "https://test-cdk-platform.com/api"

    # 角色Token（后续可通过登录接口动态获取，此处暂用固定值）
    TOKENS = {
        "admin": "test_admin_token_123456",
        "agent": "test_agent_token_789012"
    }

    # 接口超时时间（单位：秒）
    REQUEST_TIMEOUT = 10

    # 性能测试配置
    PERF_CONFIG = {
        "concurrent_num": 500,  # 并发用户数
        "max_response_time": 0.2,  # 最大响应时间（200ms）
        "large_batch_count": 100000  # 大数量CDK生成测试（10万条）
    }