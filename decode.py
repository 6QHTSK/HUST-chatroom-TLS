from Crypto.Cipher import AES
crypt_file_name = input("输入加密聊天记录文件> ")
crypt_file = open(crypt_file_name,"rb")
if crypt_file is None:
    print("文件路径错误")
passwd = input("输入密码").encode('utf-8')
while len(passwd) <= 16:
    passwd = passwd + b'\x00'
passwd = passwd[0:16]
aes = AES.new(passwd,AES.MODE_ECB)
en_text = crypt_file.read()
den_text = aes.decrypt(en_text) # 解密密文
print("加密的聊天记录如下：",den_text.decode())