# -*- coding: utf-8 -*-
"""
Example code from
http://stefan.sofa-rockers.org/2012/02/01/designing-and-testing-pyzmq-applications-part-1/

The original demo code had an error in pong.py resulting in
"zmq.error.ZMQError: Address in use"
in pong on the "sock.bind(addr)" line in pong().
This should be replaced by "sock.connect(addr)"
"""

import multiprocessing
import zmq
import signal


signal.signal(signal.SIGINT, signal.SIG_DFL)    # so we can interrupt w ctrl-C
addr = 'tcp://127.0.0.1:5680'


def ping():
    """Sends ping requests and waits for replies."""
    context = zmq.Context()
    sock = context.socket(zmq.REQ)
    sock.bind(addr)

    for i in range(5):
        sock.send_unicode('ping %s' % i)
        rep = sock.recv_unicode()  # This blocks until we get something
        print('Ping got reply:', rep)


# polling.py
def pong():
    """Waits for ping requests and replies with a pong."""
    context = zmq.Context()
    sock = context.socket(zmq.REP)
    sock.connect(addr)

    # Create a poller and register the events we want to poll
    poller = zmq.Poller()
    poller.register(sock, zmq.POLLIN|zmq.POLLOUT)

    for i in range(10):
        # Get all sockets that can do something
        socks = dict(poller.poll())
        # Check if we can receive something
        if sock in socks and socks[sock] == zmq.POLLIN:
            req = sock.recv_unicode()
            print('Pong got request:', req)
        # Check if we cann send something
        if sock in socks and socks[sock] == zmq.POLLOUT:
            sock.send_unicode('pong %s' % (i // 2))

    poller.unregister(sock)


if __name__ == '__main__':
    print("multiprocess communication with zmq using polling")
    pong_proc = multiprocessing.Process(target=pong)
    pong_proc.start()

    ping()

    # wait until all pong processes have finished
    pong_proc.join()
