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
  output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.61", 7890));
  output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.55", 7890));
  output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.59", 7890));
  output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.53", 7890));
  output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.57", 7890));
  output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.60", 7890));
  output.addChild(new DreamlandFadecandyOutput(lx, "192.168.2.54", 7890));
}
