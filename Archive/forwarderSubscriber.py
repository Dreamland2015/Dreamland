import zmq

port = "1111"
# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
print("Collecting updates from server...")
socket.connect("tcp://localhost:" + port)
topicfilter = "9"
socket.setsockopt_string(zmq.SUBSCRIBE, "")
for update_nbr in range(10):
    string = socket.recv_string()
    topic, messagedata = string.split()
    print(topic, messagedata)
