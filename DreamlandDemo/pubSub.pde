import org.zeromq.ZMQ;

String subscribeTo = "motion";

void psenvsub () {
    // Prepare our context and subscriber
    ZMQ.Context context = ZMQ.context(1);
    ZMQ.Socket subscriber = context.socket(ZMQ.SUB);
    println("did a thing");

    subscriber.connect("tcp://localhost:6000");
    subscriber.subscribe(subscribeTo.getBytes());
    while (!Thread.currentThread ().isInterrupted ()) {
        // Read message contents
        String[] message = subscriber.recvStr().split("\\|");
        String[] contents= message[1].split(",");

        println(contents[1]);
        rotationPosition = Float.parseFloat(contents[0]);
        rotationVelocity = Float.parseFloat(contents[1]);

    }
    subscriber.close ();
    context.term ();
}

class ZMQ_pub {
    String message;
    String topic;
    String which;
    ZMQ.Socket publisher;

    public ZMQ_pub(String master, String topic, String which){
        ZMQ.Context context = ZMQ.context(1);
        this.publisher = context.socket(ZMQ.PUB);
        this.publisher.connect("tcp://" + master + ":6001");
        this.topic = topic;
        this.which = which;
    }

    void sendMessage(String value){
        String sayWhat = this.topic + "|" + this.which + "#" + value;
        this.publisher.send(sayWhat);
    }
}

class ZMQ_sub {
    String message;
    String topic;
    String which;
    String subscribeTo;
    ZMQ.Socket subscriber;

    public ZMQ_sub(String master, String topic, String which){
        this.subscribeTo = topic + "|" + which;

        ZMQ.Context context = ZMQ.context(1);
        this.subscriber = context.socket(ZMQ.SUB);
        this.subscriber.connect("tcp://" + master + ":6001");
        this.subscriber.subscribe(this.subscribeTo.getBytes());
        this.topic = topic;
        this.which = which;
    }

    // private recvMessage(){
    //     String message = subscriber.recvStr();
    //     // String[] contents = messa

    // }
}