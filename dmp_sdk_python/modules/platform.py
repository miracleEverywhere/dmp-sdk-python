"""平台 / 系统接口 (/v3/platform/*)"""

from typing import List


class PlatformModule:
    """平台与系统管理模块"""

    def __init__(self, client):
        self._c = client

    def overview(self) -> dict:
        """获取平台概览（仅管理员）。

        GET /v3/platform/overview

        返回运行时长、内存、房间/世界/用户数、峰值指标等。
        """
        return self._c._request("GET", "/platform/overview")

    def game_version(self) -> str:
        """获取 DST 游戏版本号。

        GET /v3/platform/game_version
        """
        return self._c._request("GET", "/platform/game_version")

    def os_info(self) -> dict:
        """获取操作系统信息。

        GET /v3/platform/os_info
        """
        return self._c._request("GET", "/platform/os_info")

    def metrics(self, time_range: int = 60) -> List[dict]:
        """获取系统指标历史（仅管理员）。

        GET /v3/platform/metrics

        参数:
            time_range: 时间范围（分钟），默认 60
        """
        return self._c._request(
            "GET",
            "/platform/metrics",
            params={"timeRange": time_range},
        )

    def get_global_settings(self) -> dict:
        """获取全局设置（仅管理员）。

        GET /v3/platform/global_settings
        """
        return self._c._request("GET", "/platform/global_settings")

    def update_global_settings(self, **settings) -> None:
        """更新全局设置（仅管理员）。

        POST /v3/platform/global_settings

        主要字段:
            playerGetFrequency: int      玩家数据获取频率
            playerInfoSaveTime: int     玩家信息保存时长
            UIDMaintainEnable: bool     UID 维护开关
            sysMetricsEnable: bool      系统指标采集开关
            sysMetricsSetting: int      系统指标采集间隔
            autoUpdateEnable: bool      自动更新开关
            autoUpdateSetting: str      自动更新时间设置
            autoUpdateRestart: bool     自动更新后重启
        """
        return self._c._request(
            "POST", "/platform/global_settings", json_data=settings
        )

    def screen_running(self, roomID: int) -> List[str]:
        """列出房间正在运行的 screen 会话（仅管理员）。

        GET /v3/platform/screen/running
        """
        return self._c._request(
            "GET",
            "/platform/screen/running",
            params={"roomID": roomID},
        )

    def screen_kill(self, screen_name: str) -> None:
        """终止一个 screen 会话（仅管理员）。

        POST /v3/platform/screen/kill
        """
        return self._c._request(
            "POST",
            "/platform/screen/kill",
            json_data={"screenName": screen_name},
        )
