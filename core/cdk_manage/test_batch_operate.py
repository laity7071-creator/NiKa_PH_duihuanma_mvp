#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/5 09:39
@文件名: test_batch_operate.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/core/cdk_manage\test_batch_operate.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
from typing import Dict, List
from utils.request_utils import RequestClient
from utils.db_utils import db_client
from config.constant import CdkConstant
from utils.log_utils import logger
import os


class TestBatchOperate:
    """批次管理测试（状态切换、导出、搜索）"""

    def __init__(self, client: RequestClient):
        self.client = client
        self.status_api_path = "/cdk/batch/{batch_id}/status"  # 批次状态接口
        self.export_api_path = "/cdk/batch/{batch_id}/export"  # 导出接口
        self.search_api_path = "/cdk/batch/search"  # 搜索接口

    def update_batch_status(self, batch_id: str, target_status: str) -> Dict:
        """更新批次状态（启用/禁用）"""
        path = self.status_api_path.format(batch_id=batch_id)
        response = self.client.request(method="PUT", path=path, json={"target_status": target_status})
        return response.json()

    def enable_batch(self, batch_id: str) -> Dict:
        """启用批次"""
        return self.update_batch_status(batch_id, "enable")

    def disable_batch(self, batch_id: str) -> Dict:
        """禁用批次"""
        return self.update_batch_status(batch_id, "disable")

    def test_batch_status_switch(self, batch_id: str) -> None:
        """测试批次状态切换（启用→禁用→启用）"""
        logger.info(f"执行批次状态切换测试：batch_id={batch_id}")
        # 禁用批次
        disable_result = self.disable_batch(batch_id)
        if disable_result["data"]["status"] != CdkConstant.BATCH_STATUS_DISABLE:
            raise Exception("批次禁用失败")
        # 启用批次
        enable_result = self.enable_batch(batch_id)
        if enable_result["data"]["status"] != CdkConstant.BATCH_STATUS_ENABLE:
            raise Exception("批次启用失败")
        logger.info("批次状态切换测试通过")

    def test_batch_export(self, batch_id: str, export_format: str = "csv") -> str:
        """测试批次导出（CSV格式）"""
        logger.info(f"执行批次导出测试：batch_id={batch_id}")
        path = self.export_api_path.format(batch_id=batch_id)
        response = self.client.request(method="GET", path=path, params={"format": export_format}, stream=True)
        # 保存导出文件
        export_dir = "./export_test"
        os.makedirs(export_dir, exist_ok=True)
        file_path = os.path.join(export_dir, f"batch_{batch_id}.{export_format}")
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        # 校验文件存在
        if not os.path.exists(file_path):
            raise Exception(f"导出文件未生成：{file_path}")
        logger.info(f"批次导出测试通过：文件路径={file_path}")
        return file_path

    def test_search_batch_by_cdk(self, cdk: str) -> List[Dict]:
        """测试按CDK ID搜索批次"""
        logger.info(f""
        执行按CDK搜索批次测试：cdk = {cdk}
        ")
        response = self.client.request(
            method="GET",
            path=self.search_api_path,
            params={"keyword_type": "cdk_id", "keyword": cdk}
        )
        result = response.json()
        batch_list = result.get("data", [])
        if not batch_list:
            raise Exception(f"未找到CDK所属批次：cdk={cdk}")
        logger.info(f"按CDK搜索批次测试通过：匹配批次={[b['batch_id'] for b in batch_list]}")
        return batch_list