import org.zeromq.ZMQ;

String subscribeTo = "testing";

void psenvsub () {
    // Prepare our context and subscriber
    ZMQ.Context context = ZMQ.context(1);
    ZMQ.Socket subscriber = context.socket(ZMQ.SUB);
    println("did a thing");

    subscriber.connect("tcp://localhost:6000");
    subscriber.subscribe(subscribeTo.getBytes());
    while (!Thread.currentThread ().isInterrupted ()) {
        // Read envelope with address
        String address = subscriber.recvStr ();
        // Read message contents
        String[] contents = subscriber.recvStr().split(",");
        println(contents);


        rotationPosition = Float.parseFloat(contents[1]);
        rotationVelocity = Float.parseFloat(contents[2]);

    }
    subscriber.close ();
    context.term ();
}

