import org.zeromq.ZMQ;

void zeromq_sub() {
    ZMQ.Context context = ZMQ.context(1);
    ZMQ.Socket subscriber = context.socket(ZMQ.SUB);
    subscriber.connect("tcp://localhost:6000");
    subscriber.subscribe("".getBytes());
    while (!Thread.currentThread ().isInterrupted ()) {
        // Parse message
        String full_message = subscriber.recvStr();
        //println(full_message);

        String []addr_tokens = full_message.split("[|]");
        //print(addr_tokens);
        String address = addr_tokens[0];
        println(address);
        if (address.equals("motion"))
            continue;
        String []action_tokens = addr_tokens[1].split("[#]");
        //print(action_tokens);
        String action = action_tokens[0];
        int value = Integer.parseInt(action_tokens[1]);

        //float number = Float.parseFloat(contents);
        //println();
        //println("addr", address);
        //println("act", action);
        //println("value", value);
        //println();

        //if (address.equals("thing") && action.equals("flame1")) {
        //    println("doing it...");
        //    fire1.setActive(value == 1);
        //} else {
        //    println("no?");
        //}


        //rotationPosition = number;

        //println();
        //println();
        //println();
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
