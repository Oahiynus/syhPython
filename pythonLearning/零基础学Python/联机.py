import socket

def client():
    server_ip = input("请输入服务器的IP地址: ")
    server_port = int(input("请输入服务器的端口号: "))
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    while True:
        message = input("请输入要发送的消息: ")
        client_socket.send(message.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        print(f"服务器响应: {response}")

if __name__ == "__main__":
    client()