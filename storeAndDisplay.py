from pyvis.network import Network 
import sqlite3
import statistics
import threading
from comm import Pipe
import os
import time

def getDBData(reciever,e):
    reciever.startListening(("localhost",9898))




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

    reciever=Pipe()
    eventObj=threading.Event()
    t=threading.Thread(target=getDBData,args=(reciever,eventObj))
    t.start()   
    while(True):
        # eventObj.wait()
        data=reciever.queue.get()
        time.sleep(1)
        # e.clear()
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
    

main()