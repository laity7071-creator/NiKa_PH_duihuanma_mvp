#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 19:01
@文件名: log_utils.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/utils\log_utils.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
import logging
import os
from datetime import datetime

# 日志目录创建（若不存在）
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "log_reports")
os.makedirs(log_dir, exist_ok=True)

# 日志文件名（按日期生成）
log_file = f"test_log_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"
log_path = os.path.join(log_dir, log_file)

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8"),  # 写入文件（UTF-8编码避免乱码）
        logging.StreamHandler()  # 控制台输出
    ]
)

# 全局logger实例（全项目通过 from utils.log_utils import logger 导入）
logger = logging.getLogger("CDK-Test")