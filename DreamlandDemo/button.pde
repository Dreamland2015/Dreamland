class Button {
	int counter;
	String topic;
	String master;
	String which;
	ZMQ_pub pub;

	public Button(String master, String topic, String which){
		sub = new ZMQ_pub(master, topic, which);
	}

	public isPressed(){
		
	}
}