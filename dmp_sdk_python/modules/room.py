"""房间 CRUD 接口 (/v3/room/*)"""

from typing import List


class RoomModule:
    """房间管理模块"""

    def __init__(self, client):
        self._c = client

    def create(
        self,
        room_data: dict,
        world_data: List[dict],
        room_setting_data: dict,
    ) -> dict:
        """创建新房间（含世界和设置）。

        POST /v3/room

        返回创建的 Room 模型。
        """
        body = {
            "roomData": room_data,
            "worldData": world_data,
            "roomSettingData": room_setting_data,
        }
        return self._c._request("POST", "/room", json_data=body)

    def update(
        self,
        room_data: dict,
        world_data: List[dict],
        room_setting_data: dict,
    ) -> dict:
        """更新已有房间。

        PUT /v3/room
        """
        body = {
            "roomData": room_data,
            "worldData": world_data,
            "roomSettingData": room_setting_data,
        }
        return self._c._request("PUT", "/room", json_data=body)

    def get(self, room_id: int) -> dict:
        """获取房间完整信息（房间数据 + 世界 + 设置）。

        GET /v3/room
        """
        return self._c._request("GET", "/room", params={"id": room_id})

    def list(
        self,
        page: int = 1,
        page_size: int = 10,
        game_name: str = "",
    ) -> "PaginatedResult":
        """列出房间（含世界和玩家信息）。

        GET /v3/room/list
        """
        from ..paginated import PaginatedResult

        params = {"page": page, "pageSize": page_size}
        if game_name:
            params["gameName"] = game_name
        return self._c._paginated(None, "GET", "/room/list", params=params)

    def factor(self) -> dict:
        """获取房间与世界数量统计。

        GET /v3/room/factor
        返回 {"roomCount": int, "worldCount": int}
        """
        return self._c._request("GET", "/room/factor")

    def basic(self) -> List[dict]:
        """获取所有房间的基本信息列表。

        GET /v3/room/basic
        """
        return self._c._request("GET", "/room/basic")

    def worlds(self, roomID: int) -> List[dict]:
        """获取房间的世界列表（id + worldName）。

        GET /v3/room/worlds
        """
        return self._c._request(
            "GET", "/room/worlds", params={"roomID": roomID}
        )

    def upload(
        self,
        file_path: str = None,
        file_content: bytes = None,
        file_name: str = "upload.zip",
        roomID: str = "",
    ) -> None:
        """上传房间存档（zip 格式）。

        POST /v3/room/upload

        参数:
            file_path: 本地 zip 文件路径
            file_content: zip 文件的二进制内容（与 file_path 二选一）
            file_name: 上传文件名
            roomID: 空字符串表示新建房间，传入房间 ID 表示覆盖
        """
        if file_path:
            with open(file_path, "rb") as f:
                file_content = f.read()
        files = {"file": (file_name, file_content, "application/zip")}
        data = {"roomID": roomID}
        return self._c._request("POST", "/room/upload", data=data, files=files)

    def activate(self, roomID: int) -> None:
        """激活房间（创建 screen 会话等）。

        POST /v3/room/activate
        """
        return self._c._request(
            "POST", "/room/activate", json_data={"roomID": roomID}
        )

    def deactivate(self, roomID: int) -> None:
        """停用房间（停止 screen 会话等）。

        POST /v3/room/deactivate
        """
        return self._c._request(
            "POST", "/room/deactivate", json_data={"roomID": roomID}
        )

    def delete(self, roomID: int) -> None:
        """删除房间（仅管理员 + 房间权限检查）。

        DELETE /v3/room
        """
        return self._c._request(
            "DELETE", "/room", json_data={"roomID": roomID}
        )
