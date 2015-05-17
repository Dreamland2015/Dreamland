import zmq
import time
import random
# import sys
from multiprocessing import Process


def ForwarderDevice():
    try:
        context = zmq.Context(1)
        # Socket facing clients
        frontend = context.socket(zmq.SUB)
        frontend.bind("tcp://*:5559")

        frontend.setsockopt(zmq.SUBSCRIBE, b"")

        # Socket facing services
        backend = context.socket(zmq.PUB)
        backend.bind("tcp://*:5560")

        print("Dreamland forwarder device has started")
        zmq.device(zmq.FORWARDER, frontend, backend)
    except Exception:
        print("bringing down zmq device")
    finally:
        pass
        frontend.close()
        backend.close()
        context.term()


def publisher(port="5559"):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://localhost:%s" % port)
    publisher_id = random.randrange(0, 9999)
    print("Publisher started")

    while True:
        topic = random.randrange(1, 10)
        messagedata = "server#%s" % publisher_id
        # print("%s %s" % (topic, messagedata))
        socket.send_string("%d %s" % (topic, messagedata))
        time.sleep(1)


def subscriber(subObject="9", port="5560"):
    dreamlandObject = subObject.encode("utf-8")

    # Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    print("Collecting updates from Dreamland servers...")

    socket.connect("tcp://localhost:%s" % port)

    socket.setsockopt(zmq.SUBSCRIBE, dreamlandObject)

    while True:
        recievedString = socket.recv()
        subscribed, command = recievedString.split()
        print(command)


if __name__ == "__main__":
    # start the Forwarder Device
    Process(target=ForwarderDevice).start()
    time.sleep(1)

    # Start the publisher
    Process(target=publisher).start()
    time.sleep(1)

    # Spawn a few subscribers
    Process(target=subscriber).start()
