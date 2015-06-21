Dreamland
=========
## Testing zmq communication in python

Code copied from [readthedocs.org](https://learning-0mq-with-pyzmq.readthedocs.org/en/latest/pyzmq/multisocket/zmqpoller.html) and modified so it works on python 3

zmqtest4.py


Demo program for zmq
 
Tests zmq messaging between different processes.  
This works, but is only a genera demo. We need something more specific. Might need nonblocking socket calls.

Starts two servers (a push server, and a publish server) using  multiprocessing. Then starts a client which listens to messages from the servers.  
Normally of course we would run these on different machines connected via ethernet, and this code allows the machines to communicate via zmq. Here we're running them from the same file for test purposes.

One problem with sending string messages is that there is no standard way to encode the strings (bytes? characters? unicode characters?) before sending them.  
see: https://zeromq.github.io/pyzmq/unicode.html