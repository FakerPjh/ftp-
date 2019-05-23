from socket import *
import os

ADDR = ("0.0.0.0",9999)
user = {}
def do_request(s):
    while True:
        data,addr = s.recvfrom(1024)
        msg = data.decode().split(" ")
        if msg[0] == "L":
            do_login(s,msg[1],addr)
        if msg[0] == "C":
            text = " ".join(msg[2:])
            do_chat(s,msg[1],text)
        elif msg[0] == "Q":
            if msg[1] not in user:
                s.sendto(b"EXIT",addr)
                continue
            exit_group(s,msg[1])
#创建UDP客户端
def main_server():
    s = socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    pid = os.fork()
    if pid <0:
        return
    elif pid == 0:
        while True:
            msg = input("管理员消息")
            msg = "C 管理员消息" + msg
            s.sendto(msg.encode(),ADDR)
    else:
        do_request(s)


#客户端登入服务端判断
def do_login(s,name,addr):
    if name in user or "管理员" in name:
        s.sendto("\n该用户名已存在".encode(),addr)
        return
    else:
        s.sendto(b"OK",addr)
    #群体通知新成员入群
    msg = "\n欢迎%s进入聊天室"%name
    for i in user:
        s.sendto(msg.encode(),user[i])
    user[name] = addr

#发送消息
def do_chat(s,name,test):
    msg = "\n%s:%s"%(name,test)
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])
#退出聊天室
def exit_group(s,name):
    msg = "\n" + name + "退出了群聊"
    for i in user:
        if i == name:
            s.sendto(b"EXIT",user[i])
        else:
            s.sendto(msg.encode(),user[i])
        #删除用户
    del user[name]



if __name__ == "__main__":
    main_server()
