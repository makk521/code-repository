'''
Accepts data from both ports simultaneously
'''
import socket
import sys
from threading import Thread

def socket_service_data(address):
    """
    Connect and receive data

    Arguments:
    address   -   ('cloud private mac',port)
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(address)  # 在不同主机或者同一主机的不同系统下使用实际ip
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("..................Wait for Connection..................")

    sock, addr = s.accept()
    
    while True:
        buf = sock.recv(BUFSIZ)  # 接收数据
        buf1 = buf.decode('utf-8')  # 解码
        if not buf:
            break
        print('Received message:', buf1)
    sock.close()


def receive_data_background(addr):
    try:
        soc_bg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc_bg.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soc_bg.bind(addr)  # 在不同主机或者同一主机的不同系统下使用实际ip
        soc_bg.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("..................Wait for Connection..................")
    sock, address = soc_bg.accept()

    while(True):
        buf = sock.recv(BUFSIZ)  # 接收数据
        print('received')
        data_from_raspberry = eval(buf.decode('utf-8'))  # 很重要！经测试只能传输字符串类型，用eval转换成tuple。得到(led_status , fun_status , temperature , humidity)
        print(data_from_raspberry)

if __name__ == '__main__':
    # 初始化
    HOST = '10.0.12.13'
    BUFSIZ = 1024
    ADDR1 = (HOST, 7789)
    ADDR2 = (HOST, 8081)

    Thread(target = socket_service_data,args=(ADDR1,)).start()
    Thread(target = receive_data_background,args=(ADDR2,)).start()
