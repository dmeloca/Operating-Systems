from Modules.connection import Connection
from Modules.player import Player

def banner() -> str:
    return """
█▀█ █▀█ █▀▀ █▄▀  
█▀▄ █▄█ █▄▄ █░█  

█▀█ ▄▀█ █▀█ █▀▀ █▀█  
█▀▀ █▀█ █▀▀ ██▄ █▀▄  

█▀ █▀▀ █ █▀ █▀ █▀█ █▀█ █▀
▄█ █▄▄ █ ▄█ ▄█ █▄█ █▀▄ ▄█
        """

class Client:
    def __init__(self):
        self.connection = Connection()
        self.player = None
        self.running = True

    def start(self):
        try:
            self.connection.connect()
            banner()
            name = input("[?] Enter your username: ")
            self.player = Player(name)
            self.connection.send(f"JOIN:{self.player.name}")

            print("[*] Waiting for the game to start...")

            while self.running:
                message = self.connection.receive()

                if message == "":
                    print("[!] Server closed the connection.")
                    break

                if message == "YOUR_TURN":
                    self.handle_turn()

                elif message.startswith("RESULT:"):
                    self.handle_response(message)

                elif message == "EXIT":
                    print("[*] Server ended the game.")
                    break

                else:
                    print(f"[?] Server says: {message}")

        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            self.end_game()

    def end_game(self):
        self.connection.close()
        print("[*] Game ended. Connection closed.")

    def handle_turn(self):
        print("[*] It's your turn!")

        if not self.player.ask_selection():
            self.connection.send("EXIT")
            self.running = False
            print("[*] You chose to exit the game.")
            return

        self.connection.send(f"MOVE:{self.player.selection}")

    def handle_response(self, message):
        result = message.split(":", 1)[1].strip().upper()

        if result == "WIN":
            print("[:)] You won this round!")
        elif result == "LOSE":
            print("[:(] You lost this round.")
        elif result == "DRAW":
            print("[:/] It's a draw.")
        else:
            print(f"[?] Unknown result from server: {message}")


if __name__ == "__main__":
    client = Client()
    client.start()
