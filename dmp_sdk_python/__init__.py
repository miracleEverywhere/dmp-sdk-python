"""
DMP (饥荒联机版管理平台) Python SDK

用法:
    from dmp_sdk import DMPClient

    client = DMPClient("http://your-server:80", "your-token")

    # 链式调用: client.模块.方法()
    client.room.list(page=1, pageSize=10)
    client.dashboard.get_info(roomID=1)
    client.dashboard.startup(roomID=1, worldID=1)
"""

__version__ = "1.0.0"

from .client import DMPClient
from .error import DMPError
from .paginated import PaginatedResult

__all__ = ["DMPClient", "DMPError", "PaginatedResult"]
