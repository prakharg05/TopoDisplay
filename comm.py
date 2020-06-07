import socket
import select
import queue
import threading
import struct
import time

class Pipe:
    header_struct = struct.Struct('!I')

    def recvall(self,length):
        s=self.recv_sock
        data = b''
        while (len(data) < length):
            more = s.recv(length - len(data))
            if not more:
                raise EOFError('was expecting %d bytes but only received'
                            ' %d bytes before the socket closed'
                            % (length, len(data)))
            data += more
        return data



    def __init__(self):
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.queue=queue.Queue()

    def startListening(self,addr):
        self.sock.bind(addr)

        self.sock.listen(1)
        self.recv_sock,_=self.sock.accept()
        while True:

            readable,_,_=select.select([self.recv_sock],[],[])
            if(readable):
                # print("YP")
                data_size=self.recvall(self.header_struct.size)
                (data_size,)=self.header_struct.unpack(data_size)
                data=self.recvall(data_size)
                self.queue.put(data)
                time.sleep(1)
                # e.set()


    def connect(self,addr):
        self.sock.connect(addr)

    def send(self,message):
        self.sock.sendall(message)


    








