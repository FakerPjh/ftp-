from socket import *
import os,sys
#服务器地址
ADDR = ("176.140.6.131",9999)
#创建网络链接
def main_client():
    s = socket(AF_INET,SOCK_DGRAM)
    while True:
        name = input("你的昵称")
        msg = "L " + name
        s.sendto(msg.encode(),ADDR)
        data,addr = s.recvfrom(1024)
        if data.decode() == "OK":
            print("成功进入聊天室")
            break
        else:
            print(data.decode())
    pid = os.fork()
    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(s,name,addr)
    else:
        recv_msg(s)
#发送消息
def send_msg(s,name,addr):
    while True:
        try:
            text = input("输入聊天内容")
        except KeyboardInterrupt:
            text = "quit"
        if text == "quit":
            msg = "Q " + name
            s.sendto(msg.encode(),addr)
            sys.exit("退出聊天室")
        msg = "C %s %s"%(name,text)
        s.sendto(msg.encode(),addr)
#接收信息
def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        if data.decode() == "EXIT":
            sys.exit(0)
        print(data.decode()+"\n发言：",end=" ")





if __name__ == "__main__":
    main_client()