import random
import socket

HOST = "0.0.0.0"
PORT = 5001
CURRENCIES = {"dolar": 5.45, "dólar": 5.45, "euro": 6.05, "libra": 7.10}


def convert(request: str) -> str:
    try:
        value_text, currency = request.strip().split("|", 1)
        value = float(value_text.replace(",", "."))
        currency = currency.strip().lower()
        rate = CURRENCIES.get(currency, round(random.uniform(4.5, 7.5), 2))
        result = value / rate
        return f"R$ {value:.2f} = {result:.2f} {currency} (cotação: R$ {rate:.2f})"
    except (ValueError, UnicodeDecodeError):
        return "ERRO: envie valor|moeda, por exemplo 10|dolar"


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Servidor TCP ouvindo em {HOST}:{PORT}")
        while True:
            connection, client = server.accept()
            with connection:
                print(f"Conexão de {client[0]}:{client[1]}")
                buffer = b""
                while True:
                    chunk = connection.recv(4096)
                    if not chunk:
                        break
                    buffer += chunk
                    while b"\n" in buffer:
                        line, buffer = buffer.split(b"\n", 1)
                        connection.sendall((convert(line.decode("utf-8")) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
