import datetime
import os.path
import socket
import ssl
import threading
from Crypto.Cipher import AES

class msg_recorder:
    def __init__(self, passwd="123456"):
        self.passwd = passwd.encode('utf-8')
        while len(self.passwd) <= 16:
            self.passwd = self.passwd + b'\x00'
        self.passwd = self.passwd[0:16]
        self.buff = ""

    def record(self, sender, content):
        msg = "[{}]{}> {}".format(datetime.datetime.now(), sender, content)
        self.buff = "{}\n{}".format(self.buff, msg)

    def output(self, file):
        aes = AES.new(self.passwd, AES.MODE_ECB)  # 创建一个aes对象
        text = self.buff.encode('utf-8')
        while len(text) % AES.block_size != 0:
            text = text + b'\x00'
        file.write(aes.encrypt(text))


recorder = None


class ssl_client:
    def __init__(self, ssl_client, ssl_client_address):
        self.client = ssl_client
        self.addr = ssl_client_address

    def build(self):
        global recorder
        ssl_client = self.client

        while True:
            recv_data = ssl_client.recv(1024)

            if recv_data:
                print("Client> ".format(self.addr), recv_data.decode())
                recorder.record("Client",recv_data.decode())
                send_msg = input("Server> ".format(self.addr)).encode("utf-8")
                recorder.record("Server", send_msg.decode())
                ssl_client.send(send_msg)
            else:
                print("Client Logged out, encrypted record is generated.".format(self.addr))
                if not os.path.exists("./record"):
                    os.mkdir("./record")
                file = open("./record/{}".format(datetime.datetime.now()),"wb")
                recorder.output(file)
                ssl_client.close()
                break


class server_ssl:

    def __init__(self, port, client_num=100):
        self.port = port
        self.client_num = client_num

    def build_server(self):

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER, )
        context.verify_mode = ssl.CERT_REQUIRED

        context.load_cert_chain('cert/server.crt', 'cert/server.key')
        context.load_verify_locations('cert/ca.crt')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
            sock.bind(('0.0.0.0', self.port))
            sock.listen(self.client_num)
            print("开始监听客户端")

            with context.wrap_socket(sock, server_side=True, ) as ssock:
                while True:

                    try:
                        client_socket, addr = ssock.accept()
                    except:
                        print("客户端连接失败")
                        continue

                    client = ssl_client(client_socket, addr)

                    thd = threading.Thread(target=client.build, args=())
                    thd.setDaemon(True)
                    thd.start()


if __name__ == "__main__":
    passwd = input("请输入聊天记录加密密码，默认123456> ") or "123456"
    recorder = msg_recorder(passwd)
    server = server_ssl(port=2903)
    server.build_server()
