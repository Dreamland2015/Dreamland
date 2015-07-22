from __future__ import print_function

import signal
import time

from threading import Thread

import zmq
from zmq.devices import monitored_queue

import util

ctx = zmq.Context.instance()

def listen():
    sub = util.SubClient('localhost')

    while True:
        try:
            data = sub.recv(raw=True)
            print('Recieved:', data)
        except zmq.ContextTerminated:
            return

def main():
    l_thread = Thread(target=listen)
    l_thread.start()

    proxy = util.PubSubProxy()
    proxy.run()
    
if __name__ == '__main__':
    main()
