# -*- coding: utf-8 -*-
import socket
import ssl


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



class client_ssl:


    def send_hello(self,):
        client1 = client_ssl()
        # 生成SSL上下文
        # context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        # # 加载信任根证书
        # context.load_verify_locations("/Users/yunba/Downloads/ca.crt")

        #与服务端建立socket连接
        ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 连接服务端
        ssock.connect(('127.0.0.1', 7780))
        # ssock.connect(('182.92.1.50', 8899))
        msg = "CS*865339003627910*0003*CON".encode("utf-8")
        msg_lk = "CS*0009*LK,0,0,83".encode("utf-8")
        # msg_ud = "CS*0009*LK,0,0,83".encode("utf-8")
        msg_ud = "CS*00CD*UD,180916,025723,A,22.570733,N,113.8626083,E,0.00,249.5,0.0,6,100,60,0,0,00000010,7,255,460,1,9529,21809,158,9529,63555,133,9529,63554,129,9529,21405,126,9529,21242,124,9529,21151,120,9529,63556,119,0,40.7".encode("utf-8")
        msg_ud2 = "CS*00BD*UD2,120118,070625,A,22.570720,N,113.8620167,E,0.00,188.6,0.0,9,100,51,14188,0,00000010,6,255,460,0,9360,5081,156,9360,4081,129,9360,4151,128,9360,5082,127,9360,4723,122,9360,4082,120,0,22.4".encode("utf-8")
        msg_al = "CS*00BC*AL,120118,070625,A,22.570720,N,113.8620167,E,0.00,188.6,0.0,9,100,51,14188,0,00010008,6,255,460,0,9360,5081,156,9360,4081,129,9360,4151,128,9360,5082,127,9360,4723,122,9360,4082,120,0,22.4".encode("utf-8")
        msg_pp = "CS*00D4*PP,091046,180916,085033,A,22.570193,N,113.8621950,E,0.48,60.3,0.0,9,100,100,0,0,00000010,7,255,460,1,9529,21809,160,9529,21405,133,9529,63555,133,9529,63554,124,9529,21242,119,9529,21151,118,9529,63574,116,0,23.2".encode("utf-8")
        msg_heart = "CS*0009*heart,100".encode("utf-8")
        msg_bp = "CS*0015*bpxy,0,79,170,1,20,60".encode("utf-8")
        msg_upload = "CS*0009*UPLOAD,10".encode("utf-8")
        msg_tk = "CS*0009*TK,1,3613201,1356212,34312314161,2154211421".encode("utf-8")
        msg_config = "CS*0009*CONFIG,TY:G75,UL:60,SY:1,CM:1".encode("utf-8")


        while 1:
            com = input()

            if ("con" == com):
                ssock.send(msg)
                print("send:", msg)
                # 接收服务端返回的信息
                msg_rec = ssock.recv(128)
                # my_bytes = bytearray(msg)
                print("rec:", str(msg_rec, encoding = "utf-8"))

            elif ("exit" == com):
                ssock.close()
                break
            elif ("lk" == com):
                ssock.send(msg_lk)
                print("send:", msg_lk)
                # 接收服务端返回的信息
                msg_rec = ssock.recv(128)
                print("rec:", str(msg_rec, encoding = "utf-8"))
                #
                # # 接收服务端返回的信息
                # msg_rec = ssock.recv(128)
                # print("rec:", str(msg_rec, encoding = "utf-8"))

            elif ("ud2" == com):
                ssock.send(msg_ud2)
                # 无回复
                # msg_rec = ssock.recv(128)
                print("send:", msg_ud2)
                # print("rec:", str(msg_rec, encoding = "utf-8"))
            elif ("al" == com):
                ssock.send(msg_al)
                print("send:", msg_al)
                # 接收服务端返回的信息
                msg_rec = ssock.recv(128)
                print("rec:", str(msg_rec, encoding = "utf-8"))
            elif ("pp" == com):
                ssock.send(msg_pp)
                print("send:", msg_pp)
                # 接收服务端返回的信息
                msg_rec = ssock.recv(128)
                print("rec:", str(msg_rec, encoding = "utf-8"))
                #
                # # 接收服务端返回的信息
                # msg_rec = ssock.recv(128)
                # print("rec:", str(msg_rec, encoding = "utf-8"))

            elif ("heart" == com):
                ssock.send(msg_heart)
                print("send:", msg_heart)
                # 接收服务端返回的信息
                msg_rec = ssock.recv(128)
                print("rec:", str(msg_rec, encoding = "utf-8"))
            elif ("bp" == com):
                ssock.send(msg_bp)
                print("send:", msg_bp)
                # 接收服务端返回的信息
                msg_rec = ssock.recv(128)
                print("rec:", str(msg_rec, encoding="utf-8"))
            elif ("upload" == com):
                ssock.send(msg_upload)
                print("send:", msg_upload)
                # 接收服务端返回的信息
                msg_rec = ssock.recv(128)
                print("rec:", str(msg_rec, encoding="utf-8"))
            elif ("ud" == com):
                ssock.send(msg_ud)
                print("send:", msg_ud)
                # 接收服务端返回的信息
                # msg_rec = ssock.recv(128)
                # print("rec:", str(msg_rec, encoding="utf-8"))
            elif ("tk" == com):
                ssock.send(msg_tk)
                print("send:", msg_tk)
                # 接收服务端返回的信息
                msg_rec = ssock.recv(128)
                print("rec:", str(msg_rec, encoding="utf-8"))
            elif ("config" == com):
                ssock.send(msg_config)
                print("send:", msg_config)
                # 接收服务端返回的信息
                msg_rec = ssock.recv(128)
                print("rec:", str(msg_rec, encoding="utf-8"))



if __name__ == "__main__":
    client = client_ssl()
    client.send_hello()
