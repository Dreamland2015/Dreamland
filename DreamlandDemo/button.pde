class Button {
	int counter;
	String topic;
	String master;
	String which;
	ZMQ_sub sub;

	public Button(String master, String topic, String which){
		sub = new ZMQ_sub(master, topic, which);
	}
}