import socket
import threading


class GameServer:
    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"[+] GameServer listening on {self.host}:{self.port}")

        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                print(f"[+] New connection from {addr}")
                thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                thread.start()
        except KeyboardInterrupt:
            print("\n[!] Server shutting down.")
        finally:
            self.server_socket.close()

    def handle_client(self, client_socket):
        try:
            client_socket.sendall("[*] Welcome to Rock Paper Scissors Server!".encode('utf-8'))
        except Exception as e:
            print(f"[!] Error handling client: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    server = GameServer()
    server.start()