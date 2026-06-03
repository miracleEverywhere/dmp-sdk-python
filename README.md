# DMP SDK

饥荒管理平台 (DST Management Platform) Python SDK。

## 安装

```bash
pip install dmp-sdk-python
```

## 快速开始

```python
from dmp_sdk_python import DMPClient


# 初始化客户端（通过 token 认证）
client = DMPClient("http://your-server:80", "your-jwt-token")


# 链式调用: client.模块.方法()
users = client.user.list_users()
print(users.rows)

rooms = client.room.list()
print(rooms.rows)

room_info = client.rm.get(room_id=8)
print(room_info)

mods = client.mod.get_enabled(roomID=8, worldID=24)
print(mods)

sys_info = client.pt.os_info()
print(sys_info)

cpu_usage = client.dashboard.get_sys_info()['cpu']
print(cpu_usage)
```

## 模块一览

| 属性 | 简写 | 模块        | 说明 |
|---|---|-----------|---|
| `client.user` | `client.u` | 用户管理      | 注册、登录、用户CRUD、菜单 |
| `client.dashboard` | `client.db` | dashboard | 游戏控制、信息、连接码、大厅检测 |
| `client.room` | `client.rm` | 房间管理      | 房间CRUD、激活/停用、上传存档 |
| `client.mod` | `client.md` | 模组管理      | 搜索、下载、启用/禁用、配置 |
| `client.player` | `client.pl` | 玩家管理      | 在线玩家、名单、统计、聊天日志 |
| `client.tools` | `client.tl` | 工具        | 备份、公告、地图、令牌、快照 |
| `client.logs` | `client.lg` | 日志管理      | 日志查看、历史、清理、下载 |
| `client.platform` | `client.pt` | 平台管理      | 系统概览、版本、全局设置 |

## 特性

- **链式调用** — `client.模块.方法()` 风格，IDE 友好
- **错误处理** — 非 200 状态码抛出 `DMPError` 异常
- **分页支持** — 列表接口返回 `PaginatedResult` 对象，支持迭代和下标访问
- **文件下载** — 备份和日志支持保存到本地或返回原始 bytes
- **便捷方法** — `dashboard.startup_all()`、`player.add_admin()` 等语义化封装

## 切换语言

```python
client.set_lang("en")  # 英文
client.set_lang("zh")  # 中文（默认）
```

## 切换令牌

```python
client.set_token("new-jwt-token")
```

## 依赖

- Python >= 3.9
- requests >= 2.28
