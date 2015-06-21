Dreamland
=========
## Testing zmq communication in python

A demo program that sets up communication between two server processes and one client process. Uses both PUSH/PULL and PUB/SUB messaging.

File: zmqtest4.py


### Demo program 1 for zmq

Starts two servers (a push server, and a publish server) using  multiprocessing. Then starts a client which listens to messages from the servers. 

The code was copied from 
[readthedocs.org](https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/multisocket/zmqpoller.html)
and modified so it works on python 3.

The main program runs two servers (one PUSH and one PUB server) and one client that listens to messages from both. Note that the main program exits before the servers and the clients are done. (It doesn't use join() to wait for them to finish)

Normally of course we would run these on different machines connected via ethernet, and this code allows the machines to communicate via zmq. Here we're running them from the same file for test purposes.

Note that in the latest zmq version (3.1) messages by default get sent in raw bytes. If the messages are strings, they need to be encoded into bytes first, using some chosen encoding scheme (ascii, unicode, etc). We could do that by hand first, but zmq now has a string version of the commands to simplify and do that for us. So we uses send_string() instead of send()

The issue with strings came up because there is no standard way to encode the strings (bytes? characters? unicode characters?) before sending them. We have to pick one. 
see: https://zeromq.github.io/pyzmq/unicode.html