#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 18:44
@文件名: test_cdk_data.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/data\test_cdk_data.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
{
  "batch_create_params": {
    "normal_batch": {
      "agent_id": "test_agent_001",
      "product_id": "prod_duration_101",  # 时长卡商品（nika平台C端商品）
      "cdk_count": 100,
      "expire_time": "2026-12-31 23:59:59",
      "remark": "测试正常批次"
    },
    "large_batch": {
      "agent_id": "test_agent_001",
      "product_id": "prod_duration_101",
      "cdk_count": 100000,
      "expire_time": "2026-12-31 23:59:59",
      "remark": "10万条CDK测试批次"
    },
    "expired_batch": {
      "agent_id": "test_agent_001",
      "product_id": "prod_duration_101",
      "cdk_count": 50,
      "expire_time": "2023-01-01 00:00:00",
      "remark": "已过期测试批次"
    }
  },
  "redeem_params": {
    "normal_redeem": {
      "user_id": "test_user_001",
      "tenant_id": "test_tenant_001",
      "device_no": "test_dev_12345678",
      "ip_address": "192.168.1.100"
    },
    "duplicate_redeem": {
      "user_id": "test_user_001",
      "tenant_id": "test_tenant_001",
      "device_no": "test_dev_12345678",
      "ip_address": "192.168.1.100"
    }
  }
}