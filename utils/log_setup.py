"""
日志统一初始化模块（基于 loguru）
author: your_name
date  : 2025-09-06
"""

import os
import sys
from datetime import datetime
from loguru import logger


def init_logger(
    env: str = "dev",
    *,
    log_dir: str = "logs",
    stdout_color: bool = True,
    file_encoding: str = "utf-8",
) -> None:
    """
    根据运行环境一键初始化 loguru 日志

    Parameters
    ----------
    env : str, optional
        运行环境，支持 dev / test / prod，默认 "dev"
    log_dir : str, optional
        日志文件存放目录，默认项目根目录下 "logs"
    stdout_color : bool, optional
        开发环境是否彩色输出，默认 True
    file_encoding : str, optional
        日志文件编码，默认 "utf-8"

    Returns
    -------
    None
    """

    # ① 清空 loguru 默认全局 handler，防止重复打印
    logger.remove()

    # ② 获取当前日期，用于文件名
    date_str = datetime.now().strftime("%Y-%m-%d")

    # ③-------------------- 开发环境：控制台 --------------------
    if env == "dev":
        logger.add(
            sink=sys.stdout,  # 输出到标准输出
            level="TRACE",  # 最低级别，全开
            format="<green>{time:HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
            backtrace=True,  # 异常追溯
            diagnose=True,  # 显示变量值（仅 dev）
            colorize=stdout_color,  # 是否彩色
        )
        logger.debug("【dev】日志初始化完成，级别：TRACE → CRITICAL，输出：控制台")
        return

    # ④-------------------- 测试 / 生产：写文件 --------------------
    # 只有需要写文件时才创建目录
    os.makedirs(log_dir, exist_ok=True)

    if env == "test":
        allowed = {"INFO", "SUCCESS", "WARNING", "ERROR", "CRITICAL"}
        logger.add(
            sink=os.path.join(log_dir, f"test_{date_str}.log"),
            level="INFO",
            filter=lambda rec: rec["level"].name in allowed,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            rotation="00:00",
            retention="7 days",
            compression="zip",
            encoding=file_encoding,
        )
        logger.info(
            "【test】日志初始化完成，级别：INFO → CRITICAL，输出：test_YYYY-MM-DD.log"
        )
        return

    if env == "prod":
        allowed = {"WARNING", "ERROR", "CRITICAL"}
        logger.add(
            sink=os.path.join(log_dir, f"prod_{date_str}.log"),
            level="WARNING",
            filter=lambda rec: rec["level"].name in allowed,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            rotation="50 MB",
            retention="30 days",
            compression="zip",
            encoding=file_encoding,
        )
        logger.warning(
            "【prod】日志初始化完成，级别：WARNING → CRITICAL，输出：prod_YYYY-MM-DD.log"
        )
        return

    # ⑤ 未知环境
    raise ValueError(f"Unknown env={env!r}，仅支持 dev / test / prod")
