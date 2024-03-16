import random

def GenRandomHex(size: int = 16):
    return "".join(random.choice("0123456789abcdef") for _ in range(size))