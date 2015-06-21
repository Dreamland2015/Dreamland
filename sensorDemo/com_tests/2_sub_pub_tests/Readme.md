Dreamland
=========
## Testing zmq communication in python

Demo program for zmq publisher/subscriber model

Code from [stackoverflow](http://stackoverflow.com/questions/8092473/zeromq-high-water-mark-doesnt-work) and modified for testing.

Files:  
durasub.py  
durapub.py

 
This code highlights one of the issues that can come up with blocking socket calls (send / recv). Run both programs in separate shells. 

The publisher sends out data much faster than the subscriber reads in the data values. The publisher finishing sending all its values, and then exits. All the values the publisher sent are still in the zmq message queue, even though the publisher is already done and exited. The subscriber keeps reading from the queue, and doesn't know that the publisher process exited.

In a normal world, that's a good thing, because messages that have already been sent don't get lost. zmq takes care of that for us. 

However this doesn't work for us if we only want the most-recent fresh news, and throw all outdated data away. In our case, the client should get the newest value of the carousel rotation speed, not values from a while ago.

The fix would be to only send out values if a client requests them. But normally listening on a socket blocks the program, i.e. it waits around on that command until a message comes in. That's not good because the server had other things to do, like reading the actual data from the rotation sensor and processing it.

The solution to this is to use non-blocking sockets, or better, use polling (which is nonblocking and allows listening on multiple sockets). That's addressed in another demo.

