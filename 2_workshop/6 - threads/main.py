from Modules.connection import Connection
from Modules.player import Player
def print_banner() -> None:
    print("""
█▀█ █▀█ █▀▀ █▄▀  
█▀▄ █▄█ █▄▄ █░█  

█▀█ ▄▀█ █▀█ █▀▀ █▀█  
█▀▀ █▀█ █▀▀ ██▄ █▀▄  

█▀ █▀▀ █ █▀ █▀ █▀█ █▀█ █▀
▄█ █▄▄ █ ▄█ ▄█ █▄█ █▀▄ ▄█
    """)

def connect(connection: Connection) -> None:
    connection.connect()
    print_banner()

def main() -> None:
    connection = Connection()
    try:
        connect(connection)
        player_name:str = input("[!] Enter username: ")
        player = Player(player_name)
        connection.send(f"JOIN:{player_name}")

        player_selection:str = input("[!] Enter selection: ")
        player.selection = player_selection
        print(f"[*] Your selection was {player_selection}")
        connection.send(f"MOVE:{player.selection}")
        response = connection.receive()
        print(f"[Server] {response}")

    except ValueError as e:
        print(f"[!] {e}")
    except Exception as e:
        print(f"[!] {e}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()