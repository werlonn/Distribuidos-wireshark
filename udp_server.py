import random
import socket

HOST = "0.0.0.0"
PORT = 5000
CURRENCIES = {"dolar": 5.45, "dólar": 5.45, "euro": 6.05, "libra": 7.10}


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))
        print(f"Servidor UDP ouvindo em {HOST}:{PORT}")
        while True:
            data, client = server.recvfrom(4096)
            try:
                value_text, currency = data.decode("utf-8").strip().split("|", 1)
                value = float(value_text.replace(",", "."))
                currency = currency.strip().lower()
                rate = CURRENCIES.get(currency, round(random.uniform(4.5, 7.5), 2))
                result = value / rate
                response = f"R$ {value:.2f} = {result:.2f} {currency} (cotação: R$ {rate:.2f})"
            except (ValueError, UnicodeDecodeError):
                response = "ERRO: envie valor|moeda, por exemplo 10|dolar"
            server.sendto(response.encode("utf-8"), client)


if __name__ == "__main__":
    main()
