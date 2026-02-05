#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 18:43
@文件名: data_utils.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/utils\data_utils.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
import re
import random
from typing import List, Dict
from itertools import groupby
from config.constant import CdkConstant
from utils.log_utils import logger


class DataValidator:
    """数据验证工具（CDK格式、离散度、参数合法性）"""

    @staticmethod
    def check_cdk_format(cdk: str) -> bool:
        """校验单个CDK格式（长度、字符集、易混淆字符）"""
        # 校验长度
        if not (CdkConstant.CDK_LENGTH_MIN <= len(cdk) <= CdkConstant.CDK_LENGTH_MAX):
            raise Exception(
                f"CDK长度不合规：{len(cdk)}位，要求{CDK_LENGTH_MIN}-{CDK_LENGTH_MAX}位"
            )
        # 校验字符集与易混淆字符
        if not re.match(CdkConstant.CDK_PATTERN, cdk):
            raise Exception(
                f"CDK字符不合规：{cdk}，仅支持大写字母（排除I/L/O）+数字（排除1/0）"
            )
        logger.info(f"CDK格式校验通过：{cdk}")
        return True

    @staticmethod
    def batch_check_cdk_format(cdk_list: List[str]) -> bool:
        """批量校验CDK格式"""
        invalid_cdks = []
        for cdk in cdk_list:
            try:
                DataValidator.check_cdk_format(cdk)
            except Exception as e:
                invalid_cdks.append(f"{cdk}：{str(e)}")

        if invalid_cdks:
            raise Exception(f"批量CDK格式校验失败：{'; '.join(invalid_cdks)}")
        logger.info(f"批量CDK格式校验通过，共{len(cdk_list)}条")
        return True

    @staticmethod
    def check_cdk_discrete(cdk_list: List[str]) -> bool:
        """校验CDK离散度（避免连续序列、重复）"""
        # 1. 校验无重复
        unique_cdks = len(set(cdk_list))
        total_cdks = len(cdk_list)
        if unique_cdks != total_cdks:
            raise Exception(f"CDK存在重复：总条数{total_cdks}，唯一条数{unique_cdks}")

        # 2. 校验无连续3位及以上相同字符/数字（防撞库）
        consecutive_pattern = re.compile(r'([A-Z0-9])\1{2,}')  # 连续3位及以上相同
        consecutive_cdks = [cdk for cdk in cdk_list if consecutive_pattern.search(cdk)]
        if consecutive_cdks:
            raise Exception(f"CDK含连续序列（防撞库失败）：{consecutive_cdks}")

        # 3. 校验字符分布均匀性（字母与数字占比1:1±10%）
        letter_count = sum(1 for cdk in cdk_list for char in cdk if char.isalpha())
        digit_count = sum(1 for cdk in cdk_list for char in cdk if char.isdigit())
        total_chars = letter_count + digit_count
        letter_ratio = letter_count / total_chars if total_chars > 0 else 0

        if not (0.4 <= letter_ratio <= 0.6):
            raise Exception(
                f"CDK字符分布不均：字母占比{letter_ratio:.2%}，要求40%-60%"
            )

        logger.info(f"CDK离散度校验通过：无重复、无连续序列、字符分布均匀")
        return True