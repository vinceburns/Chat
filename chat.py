import threading
import queue
our_queue = Queue.Queue()

class KeyboardThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = 'KeyboardThread'

    def run(self):
        while True:
            try:
                input = raw_input()
                if input:
                    self.parse_input(input)
            except EOFError:
                return
    def parse_input(self,input):
        our_queue.put(input)
        
def main():
    thread_pool =[KeyboardThread,SendingThread,ListeningThread]
    while True:
        for t in thread_pool:
            t.start()