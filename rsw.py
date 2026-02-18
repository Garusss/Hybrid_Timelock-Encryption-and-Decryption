import time
import secrets
from sympy import randprime

def generate_modulus(bits=512):
    p = randprime(2**(bits-1), 2**bits)
    q = randprime(2**(bits-1), 2**bits)
    return p * q

def calibrate_squarings(sample_size=30000):
    n = secrets.randbits(512)
    x = secrets.randbelow(n)

    start = time.time()
    for _ in range(sample_size):
        x = pow(x, 2, n)
    end = time.time()

    return int(sample_size / (end - start))

def create_small_delay_puzzle(aes_key, delay_seconds=5):
    n = generate_modulus()
    a = secrets.randbelow(n)

    sps = calibrate_squarings()
    T = int(delay_seconds * sps)

    x = a
    for _ in range(T):
        x = pow(x, 2, n)

    key_int = int.from_bytes(aes_key, "big")
    puzzle_value = (key_int + x) % n

    return {
        "n": n,
        "a": a,
        "T": T,
        "puzzle_value": puzzle_value
    }

def solve_puzzle(puzzle, progress_callback=None):
    n = puzzle["n"]
    a = puzzle["a"]
    T = puzzle["T"]
    puzzle_value = puzzle["puzzle_value"]

    x = a
    for i in range(T):
        x = pow(x, 2, n)
        if progress_callback and i % 10000 == 0:
            progress_callback(i / T)

    key_int = (puzzle_value - x) % n
    return key_int.to_bytes(32, "big")
