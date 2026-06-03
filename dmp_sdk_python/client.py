from typing import Optional, Any

import requests

from .error import DMPError
from .paginated import PaginatedResult
from .modules.user import UserModule
from .modules.dashboard import DashboardModule
from .modules.room import RoomModule
from .modules.mod import ModModule
from .modules.player import PlayerModule
from .modules.tools import ToolsModule
from .modules.logs import LogsModule
from .modules.platform import PlatformModule


class DMPClient:
    """DMP API 客户端，支持链式模块调用。

    用法:
        client = DMPClient("http://server:80", "your-token")
        client.room.list(page=1)
        client.dashboard.get_info(roomID=1)
    """

    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        timeout: int = 30,
        lang: str = "zh",
    ):
        """
        参数:
            base_url: 服务器地址，例如 "http://192.168.1.1:80"
            token: JWT 令牌（也可通过 set_token 后续设置）
            timeout: 请求超时时间（秒）
            lang: 国际化语言，通过 X-I18n-Lang 请求头发送（"zh" 或 "en"）
        """
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.lang = lang
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "X-I18n-Lang": lang,
            }
        )
        if token:
            self._session.headers["X-DMP-TOKEN"] = token

        # 链式模块
        self.user = UserModule(self)
        self.dashboard = DashboardModule(self)
        self.room = RoomModule(self)
        self.mod = ModModule(self)
        self.player = PlayerModule(self)
        self.tools = ToolsModule(self)
        self.logs = LogsModule(self)
        self.platform = PlatformModule(self)

    # ---- 令牌管理 ----

    def set_token(self, token: str) -> "DMPClient":
        """更新认证使用的 JWT 令牌。"""
        self.token = token
        self._session.headers["X-DMP-TOKEN"] = token
        return self

    def set_lang(self, lang: str) -> "DMPClient":
        """设置国际化语言（zh / en）。"""
        self.lang = lang
        self._session.headers["X-I18n-Lang"] = lang
        return self

    # ---- 底层 HTTP 请求 ----

    def _request(
        self,
        method: str,
        path: str,
        params: dict = None,
        json_data: dict = None,
        data: Any = None,
        files: dict = None,
        raw: bool = False,
    ) -> Any:
        """发送 HTTP 请求到 API。

        参数:
            method: HTTP 方法
            path: API 路径（不含 /v3 前缀），例如 "/room/list"
            params: URL 查询参数
            json_data: JSON 请求体
            data: 原始请求体
            files: 文件上传字典
            raw: 为 True 时返回原始 requests.Response，否则返回解析后的 data 字段

        返回:
            解析后的响应数据（JSON 信封中的 "data" 字段），
            raw=True 或二进制下载时返回原始 Response。
        """
        url = f"{self.base_url}/v3{path}"
        resp = self._session.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
            data=data,
            files=files,
            timeout=self.timeout,
        )

        if raw:
            return resp

        ct = resp.headers.get("Content-Type", "")
        if "application/json" not in ct:
            return resp

        body = resp.json()
        code = body.get("code", 500)
        if code != 200:
            raise DMPError(code, body.get("message", "unknown error"))

        return body.get("data")

    def _paginated(
        self, data: Any, method: str, path: str, params: dict
    ) -> PaginatedResult:
        """获取单页数据，返回 PaginatedResult 对象。"""
        result = self._request(method, path, params=params)
        return PaginatedResult(result) if result else PaginatedResult({})

    # ---- 快捷属性 ----

    @property
    def u(self):
        """.user 的简写"""
        return self.user

    @property
    def db(self):
        """.dashboard 的简写"""
        return self.dashboard

    @property
    def rm(self):
        """.room 的简写"""
        return self.room

    @property
    def md(self):
        """.mod 的简写"""
        return self.mod

    @property
    def pl(self):
        """.player 的简写"""
        return self.player

    @property
    def tl(self):
        """.tools 的简写"""
        return self.tools

    @property
    def lg(self):
        """.logs 的简写"""
        return self.logs

    @property
    def pt(self):
        """.platform 的简写"""
        return self.platform
