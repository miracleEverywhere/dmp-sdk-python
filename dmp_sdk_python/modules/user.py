"""用户管理接口 (/v3/user/*)"""

from typing import List

from ..utils import sha512_hex


class UserModule:
    """用户管理模块"""

    def __init__(self, client):
        self._c = client

    def register_check(self) -> bool:
        """检查是否允许注册（尚无用户时允许）。

        GET /v3/user/register
        """
        return self._c._request("GET", "/user/register")

    def register(self, username: str, password: str, **kwargs) -> None:
        """注册首个用户（仅当系统中无用户时可用）。

        POST /v3/user/register
        密码发送前会做 SHA-512 哈希。
        """
        body = {"username": username, "password": sha512_hex(password), **kwargs}
        return self._c._request("POST", "/user/register", json_data=body)

    def get_base(self) -> dict:
        """获取当前用户基本信息。

        GET /v3/user/base
        """
        return self._c._request("GET", "/user/base")

    def create_user(self, **user_fields) -> None:
        """创建新用户（仅管理员）。

        POST /v3/user/base
        """
        return self._c._request("POST", "/user/base", json_data=user_fields)

    def update_user(self, **user_fields) -> None:
        """按用户名更新用户（仅管理员）。

        PUT /v3/user/base
        """
        return self._c._request("PUT", "/user/base", json_data=user_fields)

    def delete_user(self, username: str) -> None:
        """删除用户（仅管理员，最后一个用户时拒绝删除）。

        DELETE /v3/user/base
        """
        return self._c._request(
            "DELETE", "/user/base", json_data={"username": username}
        )

    def get_menu(self) -> List[dict]:
        """获取当前用户侧边栏菜单。

        GET /v3/user/menu
        管理员可见全部菜单项，普通用户看到精简版。
        """
        return self._c._request("GET", "/user/menu")

    def list_users(
        self, page: int = 1, page_size: int = 10, q: str = ""
    ) -> "PaginatedResult":
        """列出用户（仅管理员）。

        GET /v3/user/list
        """
        from ..paginated import PaginatedResult

        return self._c._paginated(
            None, "GET", "/user/list",
            params={"page": page, "pageSize": page_size, "q": q},
        )

    def update_myself(
        self,
        password: str = None,
        nickname: str = None,
        avatar: str = None,
    ) -> None:
        """修改个人信息（用户名不可更改）。

        PUT /v3/user/myself
        密码发送前会做 SHA-512 哈希。
        """
        body = {}
        if password is not None:
            body["password"] = sha512_hex(password)
        if nickname is not None:
            body["nickname"] = nickname
        if avatar is not None:
            body["avatar"] = avatar
        return self._c._request("PUT", "/user/myself", json_data=body)
