import socket

def client():
    server_ip = input("请输入服务器的IP地址: ")
    server_port = int(input("请输入服务器的端口号: "))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while True:
        guess = input("请输入你的猜测（1-100）: ")
        client_socket.send(guess.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8')
        print(f"服务器回应: {response}")

        if response == "恭喜你猜对了！":
            break

    client_socket.close()

if __name__ == "__main__":
    client()
