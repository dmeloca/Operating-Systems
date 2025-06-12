import socket
import threading

HOST = 'localhost'
PORT = 12345

waiting_clients = []  # Client stack waiting for play
lock = threading.Lock()  # Avoid run condition

def check_winner(j1, j2):
    if j1 == j2:
        return "Draw"
    elif (j1 == "s" and j2 == "p") or \
         (j1 == "p" and j2 == "r") or \
         (j1 == "r" and j2 == "s"):
        return "Player 1 wins"
    else:
        return "Player 2 wins"

def match(conn1, conn2):
    try:
        conn1.sendall(b"[*] Welcome player 1. Enter (r)rock, (p)aper or (s)cissor:\n")
        conn2.sendall(b"[*] Welcome player 2. Enter (r)rock, (p)aper or (s)cissor:\n")

        player1_selection = conn1.recv(1024).decode().strip().lower()
        player2_selection = conn2.recv(1024).decode().strip().lower()

        result = check_winner(player1_selection, player2_selection)
        resume = f"[!] Player 1 choose: {player1_selection}\n[!] Player 2 choose: {player2_selection}\n[-] Result: {result}\n"

        conn1.sendall(resume.encode())
        conn2.sendall(resume.encode())
    finally:
        conn1.close()
        conn2.close()

def accept_clients():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[SERVER] Listening in {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            print(f"[CONNECTED] Client {addr}")

            threading.Thread(target=assign_match, args=(conn,), daemon=True).start()

def assign_match(conn):
    with lock:
        waiting_clients.append(conn)
        if len(waiting_clients) >= 2:
            conn1 = waiting_clients.pop(0)
            conn2 = waiting_clients.pop(0)
            threading.Thread(target=match, args=(conn1, conn2), daemon=True).start()

if __name__ == "__main__":
    accept_clients()
