import socket
import ssl
from time import sleep

class client_ssl:
    def connect_server(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

        context.load_verify_locations('cert/ca.crt')
        context.load_cert_chain('cert/client.crt','cert/client.key')

        context.check_hostname = False

        with socket.create_connection(('127.0.0.1', 2903)) as sock:

            with context.wrap_socket(sock, server_hostname='server.psk') as ssock:
                while True:
                    # 向服务端发送信息
                    send_msg = input("Client> ") or "\\exit"
                    if send_msg == "\\exit":
                        break
                    ssock.send(send_msg.encode("utf-8"))
                    # 接收服务端返回的信息
                    msg = ssock.recv(1024).decode("utf-8")
                    if len(msg) >= 0:
                        print(f"Server> {msg}")
                    sleep(0.5)

                ssock.close()

if __name__ == "__main__":
    client = client_ssl()
    client.connect_server()
