
from scapy.all import *
from comm import Pipe
import pickle

header_struct = struct.Struct('!I')

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

    c=0
    sender=Pipe()
    # sender.connect(('localhost',9898))
    lst=[]
    for pkt in f:
        c+=1

        pkt_data=getsrcdest(pkt)
        if(pkt is not None):
          lst.append(pkt_data)  
        else:c-=1

        if(c%10==0):
            data=pickle.dumps(lst)
            lst=[]
            print(data)
            print(pickle.loads(data))
            sender.send(sender.header_struct.pack(len(data)))
            sender.send(data)
