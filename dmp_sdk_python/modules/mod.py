"""模组管理接口 (/v3/mod/*)"""

from typing import List


class ModModule:
    """模组管理模块"""

    def __init__(self, client):
        self._c = client

    def search(
        self,
        search_type: str,
        search_text: str,
        page: int = 1,
        page_size: int = 10,
    ) -> dict:
        """在 Steam 创意工坊搜索模组。

        GET /v3/mod/search

        参数:
            search_type: "id" 或 "text"
            search_text: 搜索关键词
        """
        return self._c._request(
            "GET",
            "/mod/search",
            params={
                "searchType": search_type,
                "searchText": search_text,
                "page": page,
                "pageSize": page_size,
            },
        )

    def download(
        self,
        roomID: int,
        mod_id: int,
        file_url: str,
        update: bool = False,
        size: str = "",
        name: str = "",
    ) -> None:
        """为房间下载模组。

        POST /v3/mod/download
        """
        body = {
            "roomID": roomID,
            "id": mod_id,
            "file_url": file_url,
            "update": update,
            "size": size,
            "name": name,
        }
        return self._c._request("POST", "/mod/download", json_data=body)

    def downloaded(self, roomID: int) -> List[dict]:
        """列出房间已下载的模组。

        GET /v3/mod/downloaded
        """
        return self._c._request(
            "GET", "/mod/downloaded", params={"roomID": roomID}
        )

    def enable(
        self, roomID: int, worldID: int, mod_id: int, file_url: str
    ) -> None:
        """在世界中启用模组。

        POST /v3/mod/add/enable
        """
        body = {
            "roomID": roomID,
            "worldID": worldID,
            "id": mod_id,
            "file_url": file_url,
        }
        return self._c._request("POST", "/mod/add/enable", json_data=body)

    def disable(self, roomID: int, worldID: int, mod_id: int) -> None:
        """在世界中禁用模组。

        POST /v3/mod/setting/disable
        """
        body = {"roomID": roomID, "worldID": worldID, "id": mod_id}
        return self._c._request(
            "POST", "/mod/setting/disable", json_data=body
        )

    def get_config_struct(
        self, roomID: int, worldID: int, mod_id: int, file_url: str
    ) -> dict:
        """获取模组配置选项结构。

        GET /v3/mod/setting/mod_config_struct
        """
        return self._c._request(
            "GET",
            "/mod/setting/mod_config_struct",
            params={
                "roomID": roomID,
                "worldID": worldID,
                "id": mod_id,
                "file_url": file_url,
            },
        )

    def get_config_value(
        self, roomID: int, worldID: int, mod_id: int, file_url: str
    ) -> dict:
        """获取模组配置当前值。

        GET /v3/mod/setting/mod_config_value
        """
        return self._c._request(
            "GET",
            "/mod/setting/mod_config_value",
            params={
                "roomID": roomID,
                "worldID": worldID,
                "id": mod_id,
                "file_url": file_url,
            },
        )

    def set_config_value(
        self,
        roomID: int,
        worldID: int,
        mod_id: int,
        configuration_options: dict,
        enabled: bool = True,
    ) -> None:
        """设置模组配置值。

        PUT /v3/mod/setting/mod_config_value
        """
        body = {
            "roomID": roomID,
            "worldID": worldID,
            "id": mod_id,
            "modORConfig": {
                "configuration_options": configuration_options,
                "enabled": enabled,
            },
        }
        return self._c._request(
            "PUT", "/mod/setting/mod_config_value", json_data=body
        )

    def get_enabled(self, roomID: int, worldID: int) -> List[dict]:
        """获取世界已启用的模组列表。

        GET /v3/mod/setting/enabled
        """
        return self._c._request(
            "GET",
            "/mod/setting/enabled",
            params={"roomID": roomID, "worldID": worldID},
        )

    def delete(self, roomID: int, mod_id: int, file_url: str) -> None:
        """从房间删除模组。

        POST /v3/mod/delete
        """
        body = {"roomID": roomID, "id": mod_id, "file_url": file_url}
        return self._c._request("POST", "/mod/delete", json_data=body)

    def delete_acf(self, roomID: int) -> None:
        """删除房间的 Steam Workshop ACF 文件。

        DELETE /v3/mod/delete/acf
        """
        return self._c._request(
            "DELETE", "/mod/delete/acf", json_data={"roomID": roomID}
        )
