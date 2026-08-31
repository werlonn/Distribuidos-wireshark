import socket

SERVER = ("127.0.0.1", 5001)


def receive_line(connection: socket.socket) -> str:
    data = bytearray()
    while not data.endswith(b"\n"):
        chunk = connection.recv(1)
        if not chunk:
            break
        data.extend(chunk)
    return data.decode("utf-8").rstrip("\n")


def main() -> None:
    try:
        with socket.create_connection(SERVER, timeout=3) as client:
            print("Cliente TCP conectado. Digite três conversões no formato valor|moeda.")
            for number in range(3):
                request = input(f"Conversão {number + 1}: ").strip()
                client.sendall((request + "\n").encode("utf-8"))
                print(f"Resposta: {receive_line(client)}")
    except ConnectionRefusedError:
        print("Servidor TCP indisponível: conexão recusada.")
    except TimeoutError:
        print("Servidor TCP indisponível: timeout na conexão ou na resposta.")


if __name__ == "__main__":
    main()
