#!/bin/python
import sys
import os 
import random
import subprocess

def generate_test(size: int, bound: int) -> list[int]:
    return [random.randint(0, bound) for _ in range(size)]

def save_test(size: int, test: list[int]) -> None:
    with open('input.txt', 'w') as f:
        f.write(f"{size}\n")
        f.write(" ".join(map(str, test)))

def main(size: int, bound: int, script: str) -> None:
    test = generate_test(size, bound)
    save_test(size, test)

    if not os.path.exists(script):
        print(f"[!] Script {script} not found.")
        return

    os.chmod(script, 0o755)

    try:
        result = subprocess.run(
            ["bash", "-c", f"time ./{script} < input.txt"],
            capture_output=True
        )

        output = result.stdout.decode().strip()
        expected = " ".join(map(str, sorted(test)))

        print("[*] Result:")
        print(output)
        print("[/] Execution Time:")
        print(result.stderr.decode())

        if output == expected:
            print("[✓] Test passed")
        else:
            print("[✗] Wrong answer")
            print("Expected:")
            print(expected)

    except Exception as e:
        print(f"Error while executing: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 4:
        print(f"[*] Running {sys.argv[0]} for {sys.argv[2]} with {sys.argv[1]} test cases.")
        main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
    else:
        print("[!] Usage: python test.py <size> <bound> <script>")
