# -*- coding: utf-8 -*-
"""
 Demo program for zmq

 Tests zmq messaging between different processes.
 This works, but is only a genera demo. We need something more specific.
 Might need nonblocking socket calls.

 Starts two servers (a push server, and a publish server) using
 multiprocessing. Then starts a client which listens to messages
 from the servers.
 Normally of course we would run these on different machines connected via
 ethernet, and this code allows the machines to communicate via zmq. Here
 we're running them from the same file for test purposes.

 Code copied from
 https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/multisocket/zmqpoller.html
 and modified so it works on python 3

 One problem with sending string messages is that there is no standard
 way to encode the strings (bytes? characters? unicode characters?)
 before sending them.
 see: https://zeromq.github.io/pyzmq/unicode.html
"""

import zmq
import time
import random
from  multiprocessing import Process
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)    # so we can interrupt w ctrl-C

def server_push(port="5556"):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://*:%s" % port)
    print("Running PUSH server on port: ", port, flush=True)
    # serves only 5 request and dies
    for reqnum in range(10):
        if reqnum < 6:
            print("PUSH server is sending: Continue", flush=True)
            socket.send_string("Continue")
        else:
            print("PUSH server is sending: Exit", flush=True)
            socket.send_string("Exit")
            break
        time.sleep (1)
    print("push server is done", flush=True)

def server_pub(port="5558"):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    publisher_id = random.randrange(0,9999)
    print("Running PUB server on port: ", port, flush=True)
    # serves only 5 request and dies
    for reqnum in range(5):
        # Wait for next request from client
        topic = random.randrange(8,10)
        messagedata = "server#%s" % publisher_id
        print("PUB server is sending: %s %s" % (topic, messagedata), flush=True)
        socket.send_string("%d %s" % (topic, messagedata))
        time.sleep(1)
    print("pub server is done")

def client(port_push, port_sub):
    context = zmq.Context()
    socket_pull = context.socket(zmq.PULL)
    socket_pull.connect ("tcp://localhost:%s" % port_push)
    print("Client -- Connected to push server with port %s" % port_push, flush=True)
    socket_sub = context.socket(zmq.SUB)
    socket_sub.connect ("tcp://localhost:%s" % port_sub)
    socket_sub.setsockopt_string(zmq.SUBSCRIBE, "9")
    print("Client -- Connected to pub server with port %s" % port_sub, flush=True)
    # Initialize poll set
    poller = zmq.Poller()
    poller.register(socket_pull, zmq.POLLIN)
    poller.register(socket_sub, zmq.POLLIN)

    # Work on requests from both server and publisher
    should_continue = True
    while should_continue:
        print("Client -- starting polling", flush=True)
        socks = dict(poller.poll())
        print("Client -- done polling", flush=True)
        if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
            print("Client -- PULL: msg from push server", flush=True)
            message = socket_pull.recv_string()
            print("Client -- PULL: Recieved control command: %s" % message, flush=True)
            if message == 'Exit':
                print("Recieved exit command, client will stop recieving messages", flush=True)
                should_continue = False
            else:
                print("          message %s isn't Exit" % message, flush=True)

        if socket_sub in socks and socks[socket_sub] == zmq.POLLIN:
            print("Client -- SUB: got pub msg from pub server", flush=True)
            string = socket_sub.recv_string()
            topic, messagedata = string.split()
            print("Client -- Processing ... ", topic, messagedata, flush=True)
    print("Client is done", flush=True)


if __name__ == "__main__":
    # Now we can run a few servers
    print("*** Starting main")
    server_push_port = "5556"
    server_pub_port = "5558"
    Process(target=server_push, args=(server_push_port,)).start()
    Process(target=server_pub, args=(server_pub_port,)).start()
    Process(target=client, args=(server_push_port,server_pub_port,)).start()
    print("*** main is done", flush=True)
    # notice that main exits before the servers/clients are done
