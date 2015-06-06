/**
 * This file has a bunch of example patterns, each illustrating the key
 * concepts and tools of the LX framework.
 */

 class MoveTheZPosition extends LXPattern{
  private final BasicParameter zPos = new BasicParameter("ZPos", model.zMax, model.zMin, 0);

  public MoveTheZPosition(LX lx) {
    super(lx);
    addParameter(zPos);
  }

  public void run(double deltaMs){
    float hueValue = lx.getBaseHuef();
    for (LXPoint p : model.points) 
    {
      // This is a common technique for modulating brightness.
      // You can use abs() to determine the distance between two
      // values. The further away this point is from an exact
      // point, the more we decrease its brightness
      float brightnessValue = max(0, 100 - abs(p.z - zPos.getValuef()));
      colors[p.index] = lx.hsb(hueValue, 100, brightnessValue);
    }
  }
 }
 
class LayerDemoPattern extends LXPattern {
  
  private final BasicParameter colorSpread = new BasicParameter("Clr", 2, 0, 3);
  private final BasicParameter stars = new BasicParameter("Stars", 100, 0, 100);
  
  public LayerDemoPattern(LX lx) {
    super(lx);
    addParameter(colorSpread);
    addParameter(stars);
    addLayer(new CircleLayer(lx));
    // addLayer(new RodLayer(lx));
    // for (int i = 0; i < 500; ++i) {
    //   addLayer(new StarLayer(lx));
    // }
  }
  
  public void run(double deltaMs) {
    // The layers run automatically
  }
  
  private class CircleLayer extends LXLayer {
    
    // private final SinLFO xPeriod = new SinLFO(10000,20000,100000); 
    private final double xPeriod = 10000;
    private final double yPeriod = 10000;
    private final double zPeriod = 10000;
    private final SinLFO brightnessX = new SinLFO(model.xMin, model.xMax, xPeriod);
    private final SinLFO brightnessY = new SinLFO(model.yMin, model.yMax, yPeriod);
  
    private CircleLayer(LX lx) {
      super(lx);
      // addModulator(xPeriod).start();
      addModulator(brightnessX).start();
      addModulator(brightnessY).start();
    }
    
    public void run(double deltaMs) {
      // The layers run automatically
      float falloff = 100 / 8 * FEET;
      for (LXPoint point : model.points) {
        float waveX = sin(point.x / model.xRange * PI); 
        float waveY = sin(point.y / model.yRange * PI); 
        float distanceFromCenter = dist(point.x, point.y, point.z, model.cx, model.cy, model.cz);
        float distanceFromBrightness = dist(waveX, waveY, brightnessX.getValuef(), brightnessY.getValuef());
        colors[point.index] = LXColor.hsb(
          lx.getBaseHuef() + distanceFromCenter,
          100,
          max(0, 100 - distanceFromBrightness * falloff)
        );
      }
    }
  }
  
  private class RodLayer extends LXLayer {
    
    private final SinLFO zPeriod = new SinLFO(2000, 5000, 9000);
    private final SinLFO zPos = new SinLFO(model.zMin, model.zMax, zPeriod);
    
    private RodLayer(LX lx) {
      super(lx);
      addModulator(zPeriod).start();
      addModulator(zPos).start();
    }
    
    public void run(double deltaMs) {
      for (LXPoint p : model.points) {
        float b = 100 - dist(p.x, p.y, model.cx, model.cy) - abs(p.z - zPos.getValuef());
        if (b > 0) {
          addColor(p.index, LXColor.hsb(
            lx.getBaseHuef() + p.z,
            100,
            b
          ));
        }
      }
    }
  }
  
  private class StarLayer extends LXLayer {
    
    private final TriangleLFO maxBright = new TriangleLFO(0, stars, random(2000, 8000));
    private final SinLFO brightness = new SinLFO(-1, maxBright, random(3000, 9000)); 
    
    private int index = 0;
    
    private StarLayer(LX lx) { 
      super(lx);
      addModulator(maxBright).start();
      addModulator(brightness).start();
      pickStar();
    }
    
    private void pickStar() {
      index = (int) random(0, model.size-100);
    }
    
    public void run(double deltaMs) {
      if (brightness.getValuef() <= 0) {
        pickStar();
      } else {
        addColor(index, LXColor.hsb(lx.getBaseHuef(), 50, brightness.getValuef()));
      }
    }
  }
}



class TestHuePattern extends LXPattern 
{
  public TestHuePattern(LX lx) 
  {
    super(lx);
  }
  
  public void run(double deltaMs) 
  {
    // Access the core master hue via this method call
    float hv = lx.getBaseHuef();
    for (int i = 0; i < colors.length; ++i) 
    {
      colors[i] = lx.hsb(hv, 100, 100);
    }
  } 
}


class TestXPattern extends LXPattern 
{
  private final SinLFO xPos = new SinLFO(model.xMin, model.xMax, 4000);
  public TestXPattern(LX lx) 
  {
    super(lx);
    addModulator(xPos).trigger();
  }
  public void run(double deltaMs) 
  {
    float hv = lx.getBaseHuef();
    for (LXPoint p : model.points) 
    {
      // This is a common technique for modulating brightness.
      // You can use abs() to determine the distance between two
      // values. The further away this point is from an exact
      // point, the more we decrease its brightness
      float bv = max(0, 100 - abs(p.x - xPos.getValuef()));
      colors[p.index] = lx.hsb(hv, 100, bv);
    }
  }
}


class TestYPattern extends LXPattern 
{
  private final SinLFO yPos = new SinLFO(model.yMin, model.yMax, 4000);
  public TestYPattern(LX lx) 
  {
    super(lx);
    addModulator(yPos).trigger();
  }
  public void run(double deltaMs) 
  {
    float hv = lx.getBaseHuef();
    for (LXPoint p : model.points) 
    {
      float bv = max(0, 100 - abs(p.y - yPos.getValuef()));
      colors[p.index] = lx.hsb(hv, 100, bv);
    }
  }
}


class TestZPattern extends LXPattern 
{
  private final SinLFO zPos = new SinLFO(model.zMin, model.zMax, 4000);
  public TestZPattern(LX lx) 
  {
    super(lx);
    addModulator(zPos).trigger();
  }
  public void run(double deltaMs) 
  {
    float hv = lx.getBaseHuef();
    for (LXPoint p : model.points) 
    {
      float bv = max(0, 100 - abs(p.z - zPos.getValuef()));
      colors[p.index] = lx.hsb(hv, 100, bv);
    }
  }
}

