#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@作者: laity.wang
@创建日期: 2026/2/4 18:45
@文件名: run.py
@项目名称: NiKa_PH_duihuanma_mvp
@文件完整绝对路径: D:/LaityTest/NiKa_PH_duihuanma_mvp\run.py
@文件相对项目路径:   # 可选，不需要可以删掉这行
@描述: 
"""
import argparse
import pytest
import os
from typing import List
from utils.log_utils import logger


def parse_args() -> argparse.Namespace:
    """解析命令行参数（指定测试模块、环境、报告格式）"""
    parser = argparse.ArgumentParser(description="C端兑换码分销平台接口测试启动脚本")

    # 测试模块选择（默认执行所有测试）
    parser.add_argument(
        "-m", "--module",
        type=str,
        choices=["all", "user", "cdk", "permission", "performance"],
        default="all",
        help="指定测试模块：all(全部)、user(用户管理)、cdk(CDK管理)、permission(权限)、performance(性能)"
    )

    # 运行环境选择（默认test环境）
    parser.add_argument(
        "-e", "--env",
        type=str,
        choices=["dev", "test", "prod"],
        default="test",
        help="指定运行环境：dev(开发)、test(测试)、prod(生产)"
    )

    # 报告格式选择（默认生成HTML+日志报告）
    parser.add_argument(
        "-r", "--report",
        type=str,
        choices=["html", "json", "log", "all"],
        default="all",
        help="指定报告格式：html、json、log、all(全部)"
    )

    return parser.parse_args()


def get_test_commands(args: argparse.Namespace) -> List[str]:
    """根据参数生成pytest命令"""
    # 基础命令
    cmd = ["pytest", "-v", "--tb=short", "-rN"]

    # 指定测试模块（通过pytest标记筛选）
    if args.module != "all":
        cmd.append(f"-m {args.module}")

    # 指定运行环境（通过环境变量传递）
    os.environ["RUN_ENV"] = args.env
    logger.info(f"当前运行环境：{args.env}")

    # 测试报告配置
    report_dir = os.path.join(os.path.dirname(__file__), "reports")
    # HTML报告
    if args.report in ["html", "all"]:
        html_report_path = os.path.join(report_dir, "html_reports", "test_report.html")
        cmd.append(f"--html={html_report_path}")
        cmd.append("--self-contained-html")  # 生成独立HTML文件（无需依赖外部资源）
    # JSON报告
    if args.report in ["json", "all"]:
        json_report_path = os.path.join(report_dir, "json_reports", "test_report.json")
        cmd.append(f"--json-report={json_report_path}")
    # 日志报告（通过log_utils配置，无需额外参数）

    # 测试用例路径
    test_case_path = os.path.join(os.path.dirname(__file__), "tests")
    cmd.append(test_case_path)

    return cmd


def main():
    """主函数：解析参数、生成命令、执行测试"""
    args = parse_args()
    cmd = get_test_commands(args)

    logger.info(f"开始执行测试，命令：{' '.join(cmd)}")
    print(f"===== 开始执行{args.module}模块测试（{args.env}环境）=====")

    # 执行pytest命令
    exit_code = pytest.main(cmd)

    # 输出执行结果
    if exit_code == 0:
        logger.info("测试执行成功！")
        print(f"===== 测试执行成功！报告已生成至reports目录 =====")
    else:
        logger.error("测试执行失败！")
        print(f"===== 测试执行失败！请查看日志报告排查问题 =====")
        exit(exit_code)


if __name__ == "__main__":
    main()