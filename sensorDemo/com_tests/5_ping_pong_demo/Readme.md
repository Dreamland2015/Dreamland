Dreamland
=========
## Testing zmq communication in python

Demo program for zmq publisher/subscriber model

This is example code from [here.](http://stefan.sofa-rockers.org/2012/02/01/designing-and-testing-pyzmq-applications-part-1/)  
Basically, I used parts of the web site to learn about polling and nonblocking messaging.

The web site itself goes into much greater detail than that. It even shows how to set up zmq ioloops that scale to a very large number of servers and clients. We don't need that here.

Files:  
pingpongdemo1.py  

Demo for multiprocess communication with zmq using REQ/REP sockets, using blocking calls.

pingpongdemo2.py  

Demo for multiprocess communication with zmq using REQ/REP sockets, using nonblocking polling.
 
