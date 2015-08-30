/* Build FadeCandy output */

LXOutput output;

class DreamlandFadecandyOutput extends FadecandyOutput {
  DreamlandFadecandyOutput(LX lx, String host, int port) {
    super(lx, host, port);
  }
  
  protected void didDispose(Exception x) {
    println("Fadecandy connection failure: " + host + ":" + port + " - " + x.toString());  
  }
}

void buildOutputs()
{
  output = new LXOutputGroup(lx);
  output.enabled.setValue(false);
  lx.addOutput(output);

  // output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.115", 7890));  // carousel-top
  // output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.110", 7890));  // carousel-bottom
  // output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.116", 7890));  // lamppost 1
  // output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.108", 7890));  // lamppost 2
  // output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.104", 7890));  // lamppost 3
  // output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.107", 7890));  // outerbench 1
  // output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.106", 7890));  // outerbench 2
  // output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.105", 7890));  // outerbench 2

  output.addChild(new DreamlandFadecandyOutput(lx, "pi15.local", 7890));  // carousel-top
  output.addChild(new DreamlandFadecandyOutput(lx, "pi10.local", 7890));  // carousel-bottom
  output.addChild(new DreamlandFadecandyOutput(lx, "pi16.local", 7890));  // lamppost 1
  output.addChild(new DreamlandFadecandyOutput(lx, "pi8.local", 7890));  // lamppost 2
  output.addChild(new DreamlandFadecandyOutput(lx, "pi4.local", 7890));  // lamppost 3
  output.addChild(new DreamlandFadecandyOutput(lx, "pi7.local", 7890));  // outerbench 1
  output.addChild(new DreamlandFadecandyOutput(lx, "pi5.local", 7890));  // outerbench 2
  output.addChild(new DreamlandFadecandyOutput(lx, "pi6.local", 7890));  // outerbench 2

}
