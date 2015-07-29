import heronarts.lx.LX;
import heronarts.lx.LXChannel;
import heronarts.lx.pattern.LXPattern;
import heronarts.lx.parameter.BasicParameter;
import heronarts.lx.parameter.LXParameter;
import heronarts.lx.parameter.LXParameterListener;

abstract class DLPattern extends LXPattern {
  protected final Model model;

  DLPattern(LX lx) {
    super(lx);
    model = (Model)lx.model;
  }
}

abstract class DLLayer extends LXLayer{
  protected final Model model;

  DLLayer(LX lx) {
    super(lx);
    model = (Model)lx.model;
  }
}