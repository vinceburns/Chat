import threading
import os
import Queue
import socket
our_queue = Queue.Queue()
addr = ("192.168.0.105",7105)
class KeyboardThread(threading.Thread):
    def __init__(self, die):
        threading.Thread.__init__(self)
        self.name = 'KeyboardThread'
        self.die = die

    def run(self):
        while True:
            try:
                input = raw_input()
                if input == '***':
                    self.die.set()
                    return
                
            except EOFError:
                return
            except KeyboardInterrupt:
                raise
    def parse_input(self,input):
        our_queue.put(input)
        
        
class ListeningThread(threading.Thread):
    def __init__(self, our_socket, die):
        threading.Thread.__init__(self)
        self.name = 'ListeningThread'
        self.s = our_socket
        self.die = die
    def run(self):
        while not self.die.wait(.1):
            data,recv_addr = self.s.recvfrom(1024)
            #Limitation. only 1024 byte buffer. Wonder if we could do more? Never tried it
            """Sudo code for later?
            if addr !in self.future_dick:
                add it
            """
            print "[%s]:%s" % (str(recv_addr),data)
                
		
		
class SendingThread(threading.Thread):
    def __init__(self, our_socket, die):
        threading.Thread.__init__(self)
        self.name = 'SendingThread'
        self.s = our_socket
        self.die = die
    def run(self):
        while not self.die.wait(.1):
            job = our_queue.get()
            self.s.sendto(job,addr)
            our_queue.task_done()
            
		
        
def main():
    UDP_PORT = int(raw_input("Please enter port that you have forwarding set up on: "))
    gnightbiatch = threading.Event()
    try:
        our_sock = socket.socket(socket.AF_INET,
                                 socket.SOCK_DGRAM)
        #taking it as raw should implement as an argument.
        
        our_sock.bind(("",UDP_PORT))
        #sock.bind takes a Tuple of (Host,Port), "" takes all available hosts (for us i think its just Internal/external IP.)
        print "Socket open! Listening..."
    except:
        print "Couldn't open socket. Probably have a different server running on that port. Program Exit."
        return 0
    #we finna pass this socket around to send and receive data on. We should eventually pass a log file around/ Dictionary of addresses joining our chat???
    thread_pool =[KeyboardThread(gnightbiatch),SendingThread(our_sock, gnightbiatch),ListeningThread(our_sock, gnightbiatch)]    
    for t in thread_pool:
        t.start()
    while True:
        for t in thread_pool:
            try:
                if not t.is_alive():
                    os._exit(1)
            except KeyboardInterrupt:
                os._exit(1)
main()
            
