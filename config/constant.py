#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 18:43
@文件名: constant.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp/config\constant.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""


class CdkConstant:
    """CDK相关常量（与需求对齐）"""
    # CDK格式规则
    CDK_LENGTH_MIN = 12
    CDK_LENGTH_MAX = 16
    CDK_CHARSET = "ABCDEFGHJKLMNPQRSTUVWXYZ0123456789"  # 排除I/L/1/0/O
    CDK_PATTERN = r'^[A-HJ-KM-NP-Z0-9]{12,16}$'  # 正则表达式

    # 批次状态
    BATCH_STATUS_ENABLE = "可用"
    BATCH_STATUS_DISABLE = "禁用"
    BATCH_STATUS_EXPIRED = "已过期"

    # 核销状态
    CDK_STATUS_UNUSED = "未使用"
    CDK_STATUS_USED = "已使用"
    CDK_STATUS_INVALID = "已作废"


class UserConstant:
    """用户相关常量（与需求对齐）"""
    # 用户角色
    ROLE_ADMIN = "系统管理员"
    ROLE_AGENT = "代理商"

    # 用户状态
    USER_STATUS_ENABLE = "可用"
    USER_STATUS_DISABLE = "禁用"

    # 用户归属层级
    USER_BELONG_FIRST = "一级代理"
    USER_BELONG_SECOND = "二级代理"
    USER_BELONG_TENANT = "租户"


class ErrorMessage:
    """预期错误信息（与需求/开发对齐）"""
    CDK_DUPLICATE_REDEEM = "该兑换码已使用"
    CDK_EXPIRED = "该兑换码已过期"
    CDK_BATCH_DISABLED = "该批次已禁用"
    PERMISSION_DENIED = "权限不足"
    PARAM_REQUIRED = "不能为空"
    USER_NOT_FOUND = "无匹配用户数据"