"""面板 / 游戏控制接口 (/v3/dashboard/*)"""

from typing import List


class DashboardModule:
    """面板与游戏控制模块"""

    def __init__(self, client):
        self._c = client

    def exec_game(
        self,
        type: str,
        roomID: int,
        worldID: int = 0,
        extra: str = "",
    ) -> None:
        """执行游戏控制操作。

        POST /v3/dashboard/exec/game

        参数:
            type: "startup" | "shutdown" | "restart" | "update" | "reset" |
                  "delete" | "announce" | "systemMsg" | "console"
            roomID: 房间 ID
            worldID: 世界 ID（0 表示操作所有世界）
            extra: 附加数据，依 type 而定:
                - startup/shutdown: "all" 表示操作所有世界
                - update: 不使用
                - reset: "force" 表示强制重置
                - delete: 不使用
                - announce: 公告文本
                - systemMsg: 系统消息文本
                - console: Lua 控制台命令
        """
        body = {
            "type": type,
            "roomID": roomID,
            "worldID": worldID,
            "extra": extra,
        }
        return self._c._request("POST", "/dashboard/exec/game", json_data=body)

    # --- exec_game 便捷方法 ---

    def startup(self, roomID: int, worldID: int = 0) -> None:
        """启动世界（worldID=0 则启动全部）。"""
        extra = "all" if worldID == 0 else ""
        return self.exec_game("startup", roomID, worldID, extra)

    def startup_all(self, roomID: int) -> None:
        """启动房间内所有世界。"""
        return self.exec_game("startup", roomID, 0, "all")

    def shutdown(self, roomID: int, worldID: int = 0) -> None:
        """停止世界（worldID=0 则停止全部）。"""
        extra = "all" if worldID == 0 else ""
        return self.exec_game("shutdown", roomID, worldID, extra)

    def shutdown_all(self, roomID: int) -> None:
        """停止房间内所有世界。"""
        return self.exec_game("shutdown", roomID, 0, "all")

    def restart(self, roomID: int) -> None:
        """重启房间内所有世界（先停止再启动）。"""
        return self.exec_game("restart", roomID, 0)

    def update(self, roomID: int) -> None:
        """执行 steamcmd 更新（仅管理员，后台运行）。"""
        return self.exec_game("update", roomID, 0)

    def reset(self, roomID: int, force: bool = False) -> None:
        """重置房间。"""
        extra = "force" if force else ""
        return self.exec_game("reset", roomID, 0, extra)

    def delete_world(self, roomID: int, worldID: int) -> None:
        """删除世界数据并重启。"""
        return self.exec_game("delete", roomID, worldID)

    def announce(self, roomID: int, text: str) -> None:
        """发送游戏内公告。"""
        return self.exec_game("announce", roomID, 0, text)

    def system_msg(self, roomID: int, text: str) -> None:
        """发送游戏内系统消息。"""
        return self.exec_game("systemMsg", roomID, 0, text)

    def console(self, roomID: int, worldID: int, command: str) -> None:
        """在世界中执行 Lua 控制台命令。"""
        return self.exec_game("console", roomID, worldID, command)

    # --- 信息接口 ---

    def get_info(self, roomID: int) -> dict:
        """获取房间详细信息（世界、设置、会话、玩家）。

        GET /v3/dashboard/info/base
        """
        return self._c._request(
            "GET", "/dashboard/info/base", params={"roomID": roomID}
        )

    def get_sys_info(self) -> dict:
        """获取系统概览（CPU、内存、更新状态）。

        GET /v3/dashboard/info/sys
        """
        return self._c._request("GET", "/dashboard/info/sys")

    # --- 连接码 ---

    def get_connection_code(self, roomID: int) -> str:
        """获取房间的 c_connect() Lua 连接命令。

        GET /v3/dashboard/connection_code
        """
        return self._c._request(
            "GET", "/dashboard/connection_code", params={"roomID": roomID}
        )

    def update_connection_code(self, roomID: int, ip: str, port: int) -> None:
        """更新连接码使用的公网 IP/端口。

        PUT /v3/dashboard/connection_code
        """
        body = {"roomID": roomID, "ip": ip, "port": port}
        return self._c._request(
            "PUT", "/dashboard/connection_code", json_data=body
        )

    # --- 大厅检测 ---

    def check_lobby(
        self, game_name: str, max_player: int, regions: List[str]
    ) -> bool:
        """检查 Klei 大厅中是否存在匹配的房间。

        POST /v3/dashboard/check/lobby
        """
        body = {
            "gameName": game_name,
            "maxPlayer": max_player,
            "regions": regions,
        }
        return self._c._request(
            "POST", "/dashboard/check/lobby", json_data=body
        )
