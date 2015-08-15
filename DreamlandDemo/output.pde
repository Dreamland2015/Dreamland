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
  // output.addChild(new DreamlandFadecandyOutput(lx, "localhost", 7890));
  output.addChild(new DreamlandFadecandyOutput(lx, "pi4.local", 7890));
}
