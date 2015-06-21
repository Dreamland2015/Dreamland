Dreamland
=========
## Testing zmq communication in python

Coe modified from [stackoverflow](http://stackoverflow.com/questions/8092473/zeromq-high-water-mark-doesnt-work)

durasub.py
durapub.py

Demo program for zmq publisher/subscriber model
 
This shows one of the issues with blocking socket calls (send / recv). Run both programs in separate shells. 

The publisher sends out data much faster than the subscriber reads values. The publisher finishing sending all its values, and then exits. All the values the publisher sent are still in the zmq message queue, even though the publisher is already done and exited. The subscriber happily keeps reading from the queue, never knowing that the publisher process exited.

This method doesn't work for us if we want to publish a latest new rotation value from our rotation sensor. If the subscriber is too slow, it will be getting old values from the queue. 

The fix would be to use non-blocking sockets, or better, use polling (which is nonblocking) to see whether a value request has arrived from a subscriber client.

