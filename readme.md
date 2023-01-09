# 华中科技大学网络安全程序设计
## 基于OpenSSL的安全聊天系统

一个简单的半双工安全聊天系统，聊天结束后可以将聊天记录加密保存。

## 使用说明

### 环境安装
```bash
pip install -r reqirements.txt
```

### 生成证书
```bash
cd cert
make cert
```
### 删除证书
```bash
cd cert
make clean
```

### 启动服务端（端口已配置好）
```bash
python3 server.py
```

跟随提示配置密钥，会话记录会以结束时间为文件名存储于record目录。

### 启动客户端（端口已配置好）
```bash
python3 client.py
```
启动即自动连接服务端。

### 启动解密程序
```bash
python3 decode.py
```
跟随提示指定加密会话记录文件，输入密钥即可解密。

## 鸣谢

本项目部分代码和灵感来自于互联网。