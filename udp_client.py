import socket

SERVER = ("127.0.0.1", 5000)


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(3)
        print("Cliente UDP. Digite três conversões no formato valor|moeda.")
        for number in range(3):
            request = input(f"Conversão {number + 1}: ").strip()
            client.sendto(request.encode("utf-8"), SERVER)
            try:
                data, address = client.recvfrom(4096)
                print(f"Resposta de {address[0]}:{address[1]}: {data.decode('utf-8')}")
            except socket.timeout:
                print("Sem resposta: timeout UDP.")


if __name__ == "__main__":
    main()
