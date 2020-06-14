# -*- coding: utf-8 -*-
import select
import socket
import ssl
import time
from threading import Timer
import threading



def dec2hex4string(val):
    """
    :param val: a tuple ,which include decimal number!
    :return: a tuple ,which include hex number!
    """
    temp = []
    for item in val:
        temp_item = hex(item).replace('0x', '')
        if len(temp_item) < 2:
            temp_item = "0" + temp_item
        # print item,temp_item
        temp.append(temp_item)

    result = ''.join(temp)
    return result


def receive():
    # r_inputs = set()
    # r_inputs.add(client.ssock)
    # w_inputs = set()
    # w_inputs.add(client.ssock)
    # e_inputs = set()
    # e_inputs.add(client.ssock)
    # while 1:
    # print("start rec")
    try:
        msg_rec = client_ssl.ssock.recv(1024)
        print("rec:", str(msg_rec, encoding="utf-8"))
    except socket.timeout as e:
        # err = e.args[0]
        # # this next if/else is a bit redundant, but illustrates how the
        # # timeout exception is setup
        # if err == 'timed out':
        #     # time.sleep(1)
        #     print ('recv timed out, retry later')
        #     # continue
        # else:
        print(e, "rec null, ", "Retry in 5 seconds")
    Timer(5.0, receive).start()
    # sys.exit(1)
    # try:
    #     r_list, w_list, e_list = select.select(r_inputs, w_inputs, e_inputs, 1)
    #     print("r")  # 产生了可读事件，即服务端发送信息
    #     for event in r_list:
    #         try:
    #             data = event.recv(128)
    #         except Exception as e:
    #             print(e)
    #         if data:
    #             print(data)
    #             print("rec:", str(data, encoding="utf-8"))
    #
    #             # print("收到信息")
    #         # else:
    #         #     print("远程断开连接")
    #         #     r_inputs.clear()
    #
    #         print("w")
    #         if len(w_list) > 0:  # 产生了可写的事件，即连接完成
    #             print(w_list)
    #             w_inputs.clear()  # 当连接完成之后，清除掉完成连接的socket
    #
    #         print("e")
    #         if len(e_list) > 0:  # 产生了错误的事件，即连接错误
    #             print(e_list)
    #             e_inputs.clear()  # 当连接有错误发生时，清除掉发生错误的socket
    # except OSError as e:
    #     print(e)
    # 接收服务端返回的信息
    # msg_rec = client_ssl.ssock.recv(128)
    # print("rec:", str(msg_rec, encoding="utf-8"))
    # if not len(msg_rec):
    #     break


def connect():
    msg_con = "CS*865339003627911*0003*CON".encode("utf-8")
    client_ssl.ssock.send(msg_con)
    print("send:", msg_con)
    # 接收服务端返回的信息
    msg_rec = client_ssl.ssock.recv(128)
    print("rec:", str(msg_rec, encoding="utf-8"))
    msg_lk = "CS*0009*LK,0,0,83".encode("utf-8")
    client_ssl.ssock.send(msg_lk)
    print("send:", msg_lk)
    # 接收服务端返回的信息
    msg_rec = client_ssl.ssock.recv(128)
    print("rec:", str(msg_rec, encoding="utf-8"))
    # time.sleep(0.5)


def heartbeat():
    msg_lk = "CS*0009*LK,0,0,83".encode("utf-8")
    client_ssl.ssock.send(msg_lk)
    print("send:", msg_lk)
    # 接收服务端返回的信息
    # msg_rec = client_ssl.ssock.recv(128)
    # print("rec:", str(msg_rec, encoding="utf-8"))
    # time.sleep(0.5)
    Timer(60.0, heartbeat).start()


def send_command():
    msg = "CS*865339003627911*0003*CON".encode("utf-8")
    msg_lk = "CS*0009*LK,0,0,83".encode("utf-8")
    msg_ud = "CS*0009*LK,0,0,83".encode("utf-8")
    msg_ud2 = "CS*00BD*UD2,120118,070625,A,22.570720,N,113.8220167,E,2.12,188.6,0.0,9,100,51,14188,0,00000010,6,255,460,0,9360,5081,156,9360,4081,129,9360,4151,128,9360,5082,127,9360,4723,122,9360,4082,120,0,22.4".encode(
        "utf-8")
    msg_al = "CS*00BC*AL,120118,070625,A,22.570720,N,113.8620167,E,2.20,188.6,0.0,9,100,51,14188,0,00010008,6,255,460,0,9360,5081,156,9360,4081,129,9360,4151,128,9360,5082,127,9360,4723,122,9360,4082,120,0,22.4".encode(
        "utf-8")
    msg_pp = "CS*00D4*PP,091046,180916,085033,A,22.570193,N,113.8621950,E,0.48,60.3,0.0,9,100,100,0,0,00000010,7,255,460,1,9529,21809,160,9529,21405,133,9529,63555,133,9529,63554,124,9529,21242,119,9529,21151,118,9529,63574,116,0,23.2".encode(
        "utf-8")
    msg_heart = "CS*0009*heart,100".encode("utf-8")
    msg_bp = "CS*0015*bpxy,0,79,170,1,20,60".encode("utf-8")
    msg_upload = "CS*0009*UPLOAD,10".encode("utf-8")
    msg_center = "CS*0012*CENTER,00000000000".encode("utf-8")
    msg_pw = "CS*0009*PW,111111".encode("utf-8")
    msg_monitor = "CS*0007*MONITOR".encode("utf-8")
    msg_factory = "CS*0007*FACTORY".encode("utf-8")
    msg_remove = "CS*0008*REMOVE,1".encode("utf-8")
    msg_walktime = "CS*002A*WALKTIME,8:10-9:30,10:10-11:30,12:10-13:30".encode("utf-8")
    msg_rp = "CS*002A*rcapture".encode("utf-8")

    ssock1 = client_ssl.ssock
    while 1:
        com = input()
        print("get input: ", com)

        if ("con" == com):
            ssock1.send(msg)
            print("send:", msg)

        elif ("exit" == com):
            ssock1.close()
            break
        elif ("lk" == com):
            ssock1.send(msg_lk)
            print("send:", msg_lk)

        elif ("ud2" == com):
            ssock1.send(msg_ud2)
            # 无回复
        elif ("al" == com):
            ssock1.send(msg_al)
            print("send:", msg_al)
        elif ("pp" == com):
            ssock1.send(msg_pp)
            print("send:", msg_pp)
        elif ("heart" == com):
            ssock1.send(msg_heart)
            print("send:", msg_heart)
        elif ("bp" == com):
            ssock1.send(msg_bp)
            print("send:", msg_bp)
        elif ("upload" == com):
            ssock1.send(msg_upload)
            print("send:", msg_upload)
        elif ("center" == com):
            ssock1.send(msg_center)
            print("send:", msg_center)
        elif ("pw" == com):
            ssock1.send(msg_pw)
            print("send:", msg_pw)
        elif ("monitor" == com):
            ssock1.send(msg_monitor)
            print("send:", msg_monitor)
        elif ("factory" == com):
            ssock1.send(msg_factory)
            print("send:", msg_factory)
        elif ("remove" == com):
            ssock1.send(msg_remove)
            print("send:", msg_remove)
        elif ("walktime" == com):
            ssock1.send(msg_walktime)
            print("send:", msg_walktime)
        elif ("rp" == com):
            ssock1.send(msg_rp)
            print("send:", msg_rp)
        # time.sleep(0.5)


class client_ssl:
    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def creat_sock(self):
        # 生成SSL上下文
        # context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        # # 加载信任根证书
        # context.load_verify_locations("/Users/yunba/Downloads/ca.crt")

        # 与服务端建立socket连接
        # ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 连接服务端
        # ssock.connect(('127.0.0.1', 7780))
        # ssock.connect(('182.92.1.50', 8899))
        client_ssl.ssock.connect(('116.63.128.9', 7780))
        client_ssl.ssock.setblocking(0)
        client_ssl.ssock.settimeout(2)

def lk_timer():
    t = Timer(60.0, heartbeat)
    t.start()

def rec_timer():
    t1 = Timer(5.0, receive)
    t1.start()

if __name__ == "__main__":
    client = client_ssl()
    client.creat_sock()
    connect()

    # client.receive()
    # 创建两个线程
    # try:
    # thread1.join()
    # thread2.join()
    # except:
    #     print ("Error: unable to start thread")

    threads = []

    # 创建线程

    thread1 = threading.Thread(target=rec_timer())
    thread2 = threading.Thread(target=lk_timer())
    thread3 = threading.Thread(target=send_command())

    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)

    # 启动线程
    for t in threads:
        t.start()
    for t in threads:
        t.join()
