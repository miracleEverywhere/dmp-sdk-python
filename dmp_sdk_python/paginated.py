from typing import List


class PaginatedResult:
    """分页查询结果，支持迭代和下标访问。"""

    def __init__(self, raw: dict):
        self.rows: List[dict] = raw.get("rows", [])
        self.page: int = raw.get("page", 1)
        self.page_size: int = raw.get("pageSize", 0)
        self.total: int = raw.get("total", 0)

    def __repr__(self):
        return (
            f"PaginatedResult(page={self.page}, pageSize={self.page_size}, "
            f"total={self.total}, rows={len(self.rows)})"
        )

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):
        return self.rows[index]

    def __iter__(self):
        return iter(self.rows)
