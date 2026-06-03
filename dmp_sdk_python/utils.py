import hashlib


def sha512_hex(text: str) -> str:
    """对文本做 SHA-512 哈希，返回十六进制字符串，与 Go 后端密码哈希一致。"""
    return hashlib.sha512(text.encode()).hexdigest()
