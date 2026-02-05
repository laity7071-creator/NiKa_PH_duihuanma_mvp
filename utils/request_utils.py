#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 18:43
@文件名: request_utils.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/utils\request_utils.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
import requests
from typing import Dict, Optional, Union
from config.base_config import current_config
from utils.log_utils import logger


class RequestClient:
    """接口请求客户端（封装会话、重试、超时、日志）"""

    def __init__(self, role: str = UserConstant.ROLE_ADMIN):
        self.session = requests.Session()
        self.role = role
        self._set_headers()  # 设置默认请求头

    def _set_headers(self):
        """设置默认请求头（Token、Content-Type）"""
        token = current_config.TOKENS.get(self.role.lower(), "")
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "CDK-Platform-Test-Client/Python"
        })

    def switch_role(self, new_role: str):
        """切换用户角色（更新Token）"""
        if new_role not in [UserConstant.ROLE_ADMIN, UserConstant.ROLE_AGENT]:
            raise ValueError(f"不支持的角色：{new_role}")
        self.role = new_role
        self._set_headers()
        logger.info(f"已切换用户角色为：{new_role}")

    def request(self,
                method: str,
                path: str,
                params: Optional[Dict] = None,
                json: Optional[Dict] = None,
                retry: int = 2) -> requests.Response:
        """
        统一请求方法（支持重试、超时、日志记录）
        :param method: 请求方法（GET/POST/PUT/DELETE）
        :param path: 接口路径（如"/cdk/batch/create"）
        :param params: GET请求参数
        :param json: POST/PUT请求体
        :param retry: 重试次数（默认2次，网络波动时自动重试）
        :return: 响应对象
        """
        full_url = f"{current_config.BASE_URL}{path}"
        logger.info(f"发起请求：{method} {full_url} | 参数：{params} |  请求体：{json}")

        for attempt in range(retry + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=full_url,
                    params=params,
                    json=json,
                    timeout=current_config.REQUEST_TIMEOUT
                )
                # 记录响应日志
                logger.info(f"响应状态码：{response.status_code} | 响应内容：{response.text}")
                response.raise_for_status()  # 非2xx状态码抛出异常
                return response
            except requests.exceptions.HTTPError as e:
                logger.error(f"请求失败（{attempt + 1}/{retry + 1}）：状态码{response.status_code}，详情：{e}")
                if attempt == retry:
                    raise
            except Exception as e:
                logger.error(f"请求异常（{attempt + 1}/{retry + 1}）：{str(e)}")
                if attempt == retry:
                    raise