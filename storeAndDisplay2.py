from pyvis.network import Network 
import sqlite3
import statistics
import threading
import socket
import pickle
import queue
import os
import struct
import time
def display(q,net):
    dbName="pcapDb"

    if(not os.path.exists(dbName)):
        conn = sqlite3.connect(dbName)
        conn.execute("""create table packetdata (src text,dst text,len integer);""")
        
    else:
        conn=sqlite3.connect(dbName)

    cursor=conn.cursor()

    
    while(True):
        data=q.get()
        nodes=set()
        for src,dst,length in data:
            cursor.execute("insert into packetdata (src,dst,len) values(?,?,?)",(src,dst,length))
            nodes.add(src)
            nodes.add(dst)
        weights=[]

        for i in nodes:
            la="IP: "+i
            net.add_node(i,label=i,title=la)

        for src,dst,weight in data:
            net.add_edge(src,dst,value=weight)

        net.write_html("index.html")


def recvall(s,length):
    
    data = b''
    while (len(data) < length):
        more = s.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                        ' %d bytes before the socket closed'
                        % (length, len(data)))
        data += more
    return data


def main():
    net=Network(height=600,width=900)
    net.barnes_hut()
    dbName="pcapDb"

    if(not os.path.exists(dbName)):
        conn = sqlite3.connect(dbName)
        conn.execute("""create table packetdata (src text,dst text,len integer);""")
        
    else:
        conn=sqlite3.connect(dbName)

    cursor=conn.cursor()

    header_struct = struct.Struct('!I')
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind(("localhost",9888))
    sock.listen(1)
    q=queue.Queue()
    reciever,_=sock.accept()
    t=threading.Thread(target=display,args=(q,net))
    # t.start()
    while(True):
        data_len=recvall(reciever,header_struct.size)
        (data_len,)=header_struct.unpack(data_len)
        data=recvall(reciever,data_len)
        data=pickle.loads(data)
        # print(data)
        nodes=set()
        for i in data:
            if(i is None ):
                continue
            src,dst,length=i
            # print(type(i))
            cursor.execute("insert into packetdata (src,dst,len) values(?,?,?)",(src,dst,length))
            nodes.add(src)
            nodes.add(dst)
        weights=[]
        # print("Here")
        for i in nodes:
            la="IP: "+i
            net.add_node(i,label=i,title=la)

        for i in data:
            if(i is None ):
                continue
            src,dst,weight=i
            net.add_edge(src,dst,value=weight)
        net.write_html("index.html")
        time.sleep(4)


        

main()