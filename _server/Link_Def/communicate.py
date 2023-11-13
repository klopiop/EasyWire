import os
import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt_message(key, message):
    # 生成随机的 IV（Initialization Vector）
    iv = os.urandom(16)

    # 使用 AES 加密算法和 CBC 模式创建 Cipher 对象
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

    # 创建加密器对象
    encryptor = cipher.encryptor()

    # 加密消息
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()

    # 返回 IV 和加密后的消息
    return iv + ciphertext

def decrypt_message(key, encrypted_message):
    # 提取 IV 和加密后的消息
    iv = encrypted_message[:16]
    ciphertext = encrypted_message[16:]

    # 使用 AES 解密算法和 CBC 模式创建 Cipher 对象
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())

    # 创建解密器对象
    decryptor = cipher.decryptor()

    # 解密消息
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()

    # 返回解密后的消息
    return decrypted_message.decode()

def connect_devices(device_info, ip, port, key):
    target_devices_port = port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        device_ip = ip
        device_port = target_devices_port
        server_socket.connect((device_ip, device_port))

        while True:
            message = input("input:")

            # 加密消息
            encrypted_message = encrypt_message(key, message)

            # 发送加密后的消息给设备
            server_socket.send(encrypted_message)

            data = server_socket.recv(2048)
            received_message = data.decode()

            # 解密设备发送的消息
            decrypted_message = decrypt_message(key, received_message)

            print(f"Received: {decrypted_message}")

            if decrypted_message.lower() == "exit":
                break

    except ConnectionError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    # 32字节的密钥，可以根据需要更改
    encryption_key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10' * 2

    device_info = "Device1"
    ip_address = "192.168.1.100"
    port_number = 12345

    connect_devices(device_info, ip_address, port_number, encryption_key)
