"""日志管理接口 (/v3/logs/*)"""

from typing import Any, Union


class LogsModule:
    """日志管理模块"""

    def __init__(self, client):
        self._c = client

    def content(
        self,
        roomID: int,
        worldID: int = 0,
        log_type: str = "game",
        lines: int = 100,
    ) -> str:
        """读取日志内容。

        GET /v3/logs/content

        参数:
            roomID: 房间 ID
            worldID: 世界 ID
            log_type: "game" | "chat" | "steam" | "access" | "runtime"
            lines: 读取行数
        """
        return self._c._request(
            "GET",
            "/logs/content",
            params={
                "roomID": roomID,
                "worldID": worldID,
                "logType": log_type,
                "lines": lines,
            },
        )

    def history_list(
        self, roomID: int, worldID: int = 0, log_type: str = "game"
    ) -> Any:
        """列出历史日志文件。

        GET /v3/logs/history/list
        """
        return self._c._request(
            "GET",
            "/logs/history/list",
            params={
                "roomID": roomID,
                "worldID": worldID,
                "logType": log_type,
            },
        )

    def history_content(
        self,
        roomID: int,
        worldID: int,
        log_type: str,
        log_file: str,
    ) -> str:
        """读取历史日志文件内容。

        GET /v3/logs/history/content
        """
        return self._c._request(
            "GET",
            "/logs/history/content",
            params={
                "roomID": roomID,
                "worldID": worldID,
                "logType": log_type,
                "logFile": log_file,
            },
        )

    def clean_info(self, roomID: int) -> Any:
        """获取日志大小和路径信息（仅管理员）。

        GET /v3/logs/clean/info
        """
        return self._c._request(
            "GET", "/logs/clean/info", params={"roomID": roomID}
        )

    def clean(
        self,
        roomID: int,
        game: bool = False,
        chat: bool = False,
        steam: bool = False,
        access: bool = False,
        runtime: bool = False,
    ) -> None:
        """清理日志文件（仅管理员）。

        DELETE /v3/logs/clean
        """
        body = {
            "roomID": roomID,
            "game": game,
            "chat": chat,
            "steam": steam,
            "access": access,
            "runtime": runtime,
        }
        return self._c._request(
            "DELETE", "/logs/clean", json_data=body
        )

    def download(
        self, roomID: int, save_path: str = None
    ) -> Union[bytes, str]:
        """下载房间全部日志（zip 格式）。

        GET /v3/logs/download

        参数:
            roomID: 房间 ID
            save_path: 指定则保存到该路径并返回路径，否则返回原始 bytes

        返回:
            原始 bytes 或 save_path 路径。
        """
        resp = self._c._request(
            "GET",
            "/logs/download",
            params={"roomID": roomID},
            raw=True,
        )
        content = resp.content
        if save_path:
            with open(save_path, "wb") as f:
                f.write(content)
            return save_path
        return content
