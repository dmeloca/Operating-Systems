#!/bin/python3
import sys
import os
import random
import subprocess

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREY = "\033[90m"

def generate_test(size: int, bound: int) -> list[int]:
    return [random.randint(0, bound) for _ in range(size)]

def save_test(size: int, test: list[int]) -> None:
    with open('input.txt', 'w') as f:
        f.write(f"{size}\n")
        f.write(" ".join(map(str, test)))

def print_header():
    print(f"{BOLD}{CYAN}===[ Test Runner v1.0 ]===\n{RESET}")

def main(size: int, bound: int, script: str) -> None:
    print_header()
    test = generate_test(size, bound)
    save_test(size, test)

    if not os.path.exists(script):
        print(f"{RED}[!] Script '{script}' not found.{RESET}")
        return

    os.chmod(script, 0o755)

    print(f"{BLUE}[*] Running test with size={size}, bound={bound}, script='{script}'{RESET}")
    
    try:
        result = subprocess.run(
            ["bash", "-c", f"time ./{script} < input.txt"],
            capture_output=True
        )

        output = result.stdout.decode().strip()
        timing = result.stderr.decode().strip()
        expected = " ".join(map(str, sorted(test)))

        print(f"\n{YELLOW}[*] Output:{RESET}")
        print(output if output else f"{GREY}(No output){RESET}")

        print(f"\n{CYAN}[/] Execution Stats:{RESET}")
        print(timing)

        print(f"\n{BOLD}[*] Verdict:{RESET}")
        if output == expected:
            print(f"{GREEN}[✓] Test passed ✔️{RESET}")
        else:
            print(f"{RED}[✗] Wrong answer ❌{RESET}")
            print(f"{BOLD}Expected:{RESET}")
            print(expected)

    except Exception as e:
        print(f"{RED}[!] Error while executing: {e}{RESET}")

if __name__ == "__main__":
    if len(sys.argv) == 4:
        try:
            size = int(sys.argv[1])
            bound = int(sys.argv[2])
            script = sys.argv[3]
            main(size, bound, script)
        except ValueError:
            print(f"{RED}[!] Size and bound must be integers.{RESET}")
    else:
        print(f"{YELLOW}[!] Usage: {RESET}python {sys.argv[0]} <size> <bound> <script>")
