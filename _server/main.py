import os
import socket
from Link_Def import communicate  # 等待开发

# 使用指定协议
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connected_new_devices():
    # 接受新连接的设备
    client_socket, client_add = server_socket.accept()
    print(f"A new diverse link: {client_add}")

    # 接收设备发送的mac
    data = client_socket.recv(1024).decode()
    mac = data  # 设备的MAC地址
    ip = client_add[0]  # 设备的IP地址

    # 生成设备编号
    device_id = len(devices) + 1

    # 记录设备信息到文件
    with open("_divers.txt", "a") as file:
        file.write(f"{device_id},{mac},{ip}\n")

    # 存储设备信息到字典
    devices[device_id] = {"mac": mac, "ip": ip, "socket": client_socket}

    # 返回设备列表给连接的设备
    # 读取设备列表文件内容
    with open("_divers.txt", "r") as file:
        device_list = file.read()
    # 发送设备列表给连接的设备
    client_socket.send(device_list.encode())

def cheak_devices_connected():
    # 接收用户选择的设备编号
    data = client_socket.recv(1024).decode()
    if data == "exit":
        # 关闭连接
        client_socket.close()
        return False # 返回False表示退出循环

    # 根据用户选择的设备编号获取设备信息
    device_id = int(data)
    device_info = devices.get(device_id)
    ip = device_info["ip"]

    if device_info is None: # 使用is None判断空值
        # 设备不存在的处理逻辑...
        result = '0'  # 连接异常
        client_socket.send(result.encode())
    else:
        # 发送测试值给客户端
        test_value = 'Test'
        device_socket = device_info["socket"]
        device_socket.send(test_value.encode())

        # 接收客户端返回的数据
        response = device_socket.recv(1024).decode()

        # 判断回响结果并设置返回值
        if response == 'Test':
            result = '1'  # 连接正常
        else:
            result = '0'  # 连接异常
        # 调用 communicate.py 库进行设备通信
        result = communicate.connect_devices(device_info, ip)

        # 发送返回值给客户端
        client_socket.send(result.encode())
    return True # 返回True表示继续循环

def main():

    # 清空存储设备的文件
    with open("_divers.txt", "w") as file:
        pass

    devices = {}  # 存储设备信息的字典，键为设备编号，值为设备信息（包括MAC地址和IP）


    try:
        # 指定服务端的地址和端口
        server_add = ("localhost", 25565)
        server_socket.bind(server_add)

        # 开始监听
        server_socket.listen(10)
        # 提示
        print("Server was started to listening....")

        while True:
            connected_new_devices()
            while cheak_devices_connected(): # 使用函数的返回值作为循环条件
                pass
                
    except socket.error as e:
        print(f"Socket error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
