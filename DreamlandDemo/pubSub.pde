import org.zeromq.ZMQ;

void psenvsub () {
    // Prepare our context and subscriber
    ZMQ.Context context = ZMQ.context(1);
    ZMQ.Socket subscriber = context.socket(ZMQ.SUB);
    println("did a thing");

    subscriber.connect("tcp://localhost:6000");
    subscriber.subscribe("".getBytes());
    while (!Thread.currentThread ().isInterrupted ()) {
        // Read envelope with address
        String address = subscriber.recvStr ();
        // Read message contents
        String contents = subscriber.recvStr ();
        float number = Float.parseFloat(contents);
        println(contents);

        rotationPosition = number;

    }
    subscriber.close ();
    context.term ();
}
