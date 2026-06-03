"""工具接口 (/v3/tools/*)"""

from typing import Any, List, Union


class ToolsModule:
    """工具模块（备份、公告、地图、令牌、快照）"""

    def __init__(self, client):
        self._c = client

    # ---- 备份 ----

    def list_backups(self, roomID: int) -> Any:
        """列出房间备份文件。

        GET /v3/tools/backup
        """
        return self._c._request(
            "GET", "/tools/backup", params={"roomID": roomID}
        )

    def create_backup(self, roomID: int) -> None:
        """为房间创建新备份。

        POST /v3/tools/backup
        """
        return self._c._request(
            "POST", "/tools/backup", json_data={"roomID": roomID}
        )

    def delete_backups(self, roomID: int, filenames: List[str]) -> int:
        """删除备份文件，返回已删除文件数。

        DELETE /v3/tools/backup
        """
        return self._c._request(
            "DELETE",
            "/tools/backup",
            json_data={"roomID": roomID, "filenames": filenames},
        )

    def restore_backup(self, roomID: int, filename: str) -> None:
        """为房间恢复备份。

        POST /v3/tools/backup/restore
        """
        body = {"roomID": roomID, "filename": filename}
        return self._c._request(
            "POST", "/tools/backup/restore", json_data=body
        )

    def download_backup(
        self, roomID: int, filename: str, save_path: str = None
    ) -> Union[bytes, str]:
        """下载备份文件。

        GET /v3/tools/backup/download

        参数:
            roomID: 房间 ID
            filename: 备份文件名
            save_path: 指定则保存到该路径并返回路径，否则返回原始 bytes

        返回:
            原始 bytes 或 save_path 路径。
        """
        resp = self._c._request(
            "GET",
            "/tools/backup/download",
            params={"roomID": roomID, "filename": filename},
            raw=True,
        )
        content = resp.content
        if save_path:
            with open(save_path, "wb") as f:
                f.write(content)
            return save_path
        return content

    # ---- 公告 ----

    def get_announce(self, roomID: int) -> str:
        """获取房间公告设置。

        GET /v3/tools/announce
        """
        return self._c._request(
            "GET", "/tools/announce", params={"roomID": roomID}
        )

    def update_announce(self, roomID: int, setting: str) -> None:
        """更新房间公告设置。

        PUT /v3/tools/announce
        """
        body = {"roomID": roomID, "setting": setting}
        return self._c._request(
            "PUT", "/tools/announce", json_data=body
        )

    # ---- 地图 ----

    def map(self, roomID: int, worldID: int = 0) -> dict:
        """获取世界地图（base64 图片、实体、玩家）。

        GET /v3/tools/map
        """
        params = {"roomID": roomID}
        if worldID:
            params["worldID"] = worldID
        return self._c._request("GET", "/tools/map", params=params)

    # ---- 令牌 ----

    def create_token(self, expiration: int = 0) -> str:
        """生成新 JWT 令牌（仅管理员）。

        POST /v3/tools/token

        参数:
            expiration: 令牌有效期（小时），0 表示永久（约 99 年）。
        """
        return self._c._request(
            "POST", "/tools/token", json_data={"expiration": expiration}
        )

    # ---- 快照 ----

    def list_snapshots(self, roomID: int) -> Any:
        """列出房间快照。

        GET /v3/tools/snapshot
        """
        return self._c._request(
            "GET", "/tools/snapshot", params={"roomID": roomID}
        )

    def delete_snapshot(self, roomID: int, name: str) -> None:
        """删除快照。

        DELETE /v3/tools/snapshot
        """
        body = {"roomID": roomID, "name": name}
        return self._c._request(
            "DELETE", "/tools/snapshot", json_data=body
        )
