Dreamland
=========
## Testing zmq communication in python

Demo programs for interprocess shared variables.

Example code from ([this website](http://eli.thegreenplace.net/2012/01/04/shared-counter-with-pythons-multiprocessing))

When we fork several processes, they can't by default share information. If they need to exchange data, we can set up explicit messaging between them. That's often the right approach, we use the zmq package for that.

However, we can also set up shared variables that both processes can access. zmq also provides for a system to do that.

This is demo code trying that out.
