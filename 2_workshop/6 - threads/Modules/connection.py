import socket

DEFAULT_SERVER_IP = '127.0.0.1'
DEFAULT_SERVER_PORT = 5000

class Connection:
    def __init__(self, host:str = DEFAULT_SERVER_IP, port:int = DEFAULT_SERVER_PORT):
        self.host = host
        self.port = port
        self.sock = None
    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print("[+] Connected to server at {}:{}".format(self.host, self.port))
        except ConnectionRefusedError:
            print("[!] Cannot connect to server at {}:{}".format(self.host, self.port))
            raise
        except socket.error as e:
            print(f"[!] Unexpected error during connection: {e}")
            raise

    def send(self, data: str):
        try:
            self.sock.sendall(data.encode('utf-8'))
        except BrokenPipeError:
            print("[!] Connection lost. Could not send data.")
            raise
        except Exception as e:
            print(f"[!] Unexpected error during connection: {e}")
    def receive(self, buffer_size: int = 1024) -> str:
        try:
            data = self.sock.recv(buffer_size)
            if not data:
                print("[!] Server disconnected.")
                return ""
            return data.decode('utf-8')
        except Exception as e:
            print(f"[!] Unexpected error during connection: {e}")
            raise

    def close(self):
        if self.sock:
            self.sock.close()
            print("[+] Closing connection.")
