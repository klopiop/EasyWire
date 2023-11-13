import socket
import platform
import threading
import uuid
import os

# 指定使用的协议
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 启动程序之后进行对服务器的连接，首先让用户输入指定的服务端ip和port
ip = input("请输入服务器ip:")
port = input("请输入服务端port:")

# 连接服务器

# 获取设备信息存储在目录的__devices_info.txt文件中
# 建立一个字典，存储这些信息
host_basic_info = []
# 获取操作系统以及版本信息
sys_basic_info = platform.platform()
# 获取系统名称
sys_name = platform.node()
# 获取mac地址
mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
mac_address = ":".join([mac_address[e:e+2] for e in range(0, 11, 2)])
# 获取ip地址
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
#将信息丢进字典

# 创建文件，并且每次重启脚本后都清空一次文件
with open("_divers.txt", "w") as file:
        pass

# 同时始终监听，来自服务端发来的消息
# 连接服务器
server_socket.connect((ip, int(port)))

# 定义一个函数，用于接收服务端发来的消息
def recv_msg():
    while True:
        # 接收服务端发来的数据，1024是缓冲区大小
        data = server_socket.recv(1024)
        # 解码数据并打印
        print(data.decode("utf-8"))

# 创建一个子线程，用于执行recv_msg函数
t = threading.Thread(target=recv_msg)
# 设置为守护线程，主线程结束时子线程也结束
t.setDaemon(True)
# 启动子线程
t.start()

# 在主线程中，循环发送用户输入的消息给服务端
while True:
    # 获取用户输入的消息
    msg = input()
    # 如果输入exit，退出循环
    if msg == "exit":
        break
    # 发送消息给服务端，需要编码为字节
    server_socket.send(msg.encode("utf-8"))
