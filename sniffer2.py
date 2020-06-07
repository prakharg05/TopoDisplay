
from scapy.all import *
# from comm import Pipe
import pickle
import socket
import struct

def getsrcdest(pkt):
    while(not isinstance(pkt,scapy.packet.NoPayload)):
        if(pkt.name is not "IP"): #Check ig the layer is IP
                pkt=pkt.payload #recursivly go into further layers
        else:
            tup=(sorted([pkt.fields['src'],pkt.fields['dst']]))
            tup.append(pkt.fields['len'])
            tup=tuple(tup)
            return tup
    return None



if __name__=="__main__":

    f=sniff(offline="master")
    header_struct = struct.Struct('!I')
    c=0
    sender=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sender.connect(('localhost',9888))
    lst=[]
    mod=200
    for pkt in f:
        c+=1

        pkt_data=getsrcdest(pkt)
        if(pkt is not None):
          lst.append(pkt_data)  
        else:c-=1

        if(c%mod==0):
            mod+=50
            data=pickle.dumps(lst)
            lst=[]
            # print(data)
            # print(pickle.loads(data))
            sender.sendall(header_struct.pack(len(data)))
            sender.sendall(data)
