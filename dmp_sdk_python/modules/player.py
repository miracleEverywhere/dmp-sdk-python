"""玩家管理接口 (/v3/player/*)"""

from typing import List, Any


class PlayerModule:
    """玩家管理模块"""

    def __init__(self, client):
        self._c = client

    def online(self, roomID: int) -> List[dict]:
        """获取房间在线玩家。

        GET /v3/player/online
        返回 [{"uid": str, "nickname": str, "prefab": str}, ...]
        """
        return self._c._request(
            "GET", "/player/online", params={"roomID": roomID}
        )

    def get_list(self, roomID: int, list_type: str) -> List[dict]:
        """获取玩家名单（管理员 / 黑名单 / 白名单）。

        GET /v3/player/list

        参数:
            roomID: 房间 ID
            list_type: "admin" | "block" | "whitelist"
        """
        return self._c._request(
            "GET",
            "/player/list",
            params={"roomID": roomID, "listType": list_type},
        )

    def update_list(
        self, roomID: int, uids: List[str], list_type: str, action: str
    ) -> None:
        """在名单中添加或移除玩家。

        POST /v3/player/list

        参数:
            roomID: 房间 ID
            uids: Klei 用户 ID 列表
            list_type: "admin" | "block" | "whitelist"
            action: "add" | "remove"
        """
        body = {
            "roomID": roomID,
            "uids": uids,
            "listType": list_type,
            "actionType": action,
        }
        return self._c._request("POST", "/player/list", json_data=body)

    def add_admin(self, roomID: int, *uids: str) -> None:
        """添加管理员。"""
        return self.update_list(roomID, list(uids), "admin", "add")

    def remove_admin(self, roomID: int, *uids: str) -> None:
        """移除管理员。"""
        return self.update_list(roomID, list(uids), "admin", "remove")

    def add_block(self, roomID: int, *uids: str) -> None:
        """封禁玩家。"""
        return self.update_list(roomID, list(uids), "block", "add")

    def remove_block(self, roomID: int, *uids: str) -> None:
        """解封玩家。"""
        return self.update_list(roomID, list(uids), "block", "remove")

    def add_whitelist(self, roomID: int, *uids: str) -> None:
        """添加白名单。"""
        return self.update_list(roomID, list(uids), "whitelist", "add")

    def remove_whitelist(self, roomID: int, *uids: str) -> None:
        """移除白名单。"""
        return self.update_list(roomID, list(uids), "whitelist", "remove")

    def uidmap(self, roomID: int) -> List[dict]:
        """获取房间的 UID 与昵称映射。

        GET /v3/player/uidmap
        """
        return self._c._request(
            "GET", "/player/uidmap", params={"roomID": roomID}
        )

    def online_time(self, roomID: int) -> Any:
        """获取玩家在线时长统计。

        GET /v3/player/statistics/online_time
        """
        return self._c._request(
            "GET",
            "/player/statistics/online_time",
            params={"roomID": roomID},
        )

    def player_count(
        self, roomID: int, time_range: int = None
    ) -> List[dict]:
        """获取玩家数量快照。

        GET /v3/player/statistics/player_count

        参数:
            roomID: 房间 ID
            time_range: 时间范围（秒），可选
        """
        params = {"roomID": roomID}
        if time_range is not None:
            params["timeRange"] = time_range
        return self._c._request(
            "GET", "/player/statistics/player_count", params=params
        )

    def chat(
        self, roomID: int, lines: int = 50, need_time: bool = False
    ) -> Any:
        """获取游戏服务器聊天日志。

        GET /v3/player/chat
        """
        return self._c._request(
            "GET",
            "/player/chat",
            params={
                "roomID": roomID,
                "lines": lines,
                "needTime": need_time,
            },
        )
