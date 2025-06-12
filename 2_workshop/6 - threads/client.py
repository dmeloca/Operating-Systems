import socket

HOST = 'localhost'
PORT = 12345

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = s.recv(1024).decode()
        print(message)
        selection = input("[!] Your Selection: ").strip().lower()
        s.sendall(selection.encode())
        result = s.recv(1024).decode()
        print(result)

if __name__ == "__main__":
    main()
