"""Generate Apache apr1 htpasswd line: user:hash"""
import hashlib
import sys

ITOA64 = "./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def to64(v: int, n: int) -> str:
    out = []
    while n > 0:
        out.append(ITOA64[v & 0x3F])
        v >>= 6
        n -= 1
    return "".join(out)


def apr1(password: str, salt: str) -> str:
    password_b = password.encode("utf-8")
    salt_b = salt.encode("ascii")
    magic = b"$apr1$"

    ctx = hashlib.md5()
    ctx.update(password_b + magic + salt_b)

    ctx_final = hashlib.md5()
    ctx_final.update(password_b + salt_b + password_b)
    final = ctx_final.digest()

    for pl in range(len(password_b), 0, -16):
        ctx.update(final[: min(16, pl)])

    i = len(password_b)
    while i:
        ctx.update(b"\x00" if i & 1 else password_b[:1])
        i >>= 1
    final = ctx.digest()

    for i in range(1000):
        ctx = hashlib.md5()
        if i & 1:
            ctx.update(password_b)
        else:
            ctx.update(final)
        if i % 3:
            ctx.update(salt_b)
        if i % 7:
            ctx.update(password_b)
        if i & 1:
            ctx.update(final)
        else:
            ctx.update(password_b)
        final = ctx.digest()

    parts = []
    for a, b, c in ((0, 6, 12), (1, 7, 13), (2, 8, 14), (3, 9, 15), (4, 10, 5)):
        parts.append(to64((final[a] << 16) | (final[b] << 8) | final[c], 4))
    parts.append(to64(final[11], 2))
    return f"$apr1${salt}${''.join(parts)}"


if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "admin"
    password = sys.argv[2] if len(sys.argv) > 2 else "admin"
    salt = sys.argv[3] if len(sys.argv) > 3 else "k0ngGw01"
    print(f"{user}:{apr1(password, salt)}")
