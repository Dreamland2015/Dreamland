import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import heronarts.lx.*; 
import heronarts.lx.audio.*; 
import heronarts.lx.color.*; 
import heronarts.lx.model.*; 
import heronarts.lx.modulator.*; 
import heronarts.lx.output.*; 
import heronarts.lx.parameter.*; 
import heronarts.lx.pattern.*; 
import heronarts.lx.transition.*; 
import heronarts.p2lx.*; 
import heronarts.p2lx.ui.*; 
import heronarts.p2lx.ui.control.*; 
import ddf.minim.*; 
import processing.opengl.*; 

import heronarts.p2lx.font.*; 
import heronarts.lx.transition.*; 
import heronarts.lx.transform.*; 
import heronarts.p2lx.ui.component.*; 
import heronarts.lx.pattern.*; 
import heronarts.lx.model.*; 
import heronarts.p2lx.*; 
import heronarts.lx.midi.device.*; 
import heronarts.p2lx.ui.control.*; 
import heronarts.lx.modulator.*; 
import heronarts.lx.output.*; 
import heronarts.lx.midi.*; 
import heronarts.lx.effect.*; 
import heronarts.lx.color.*; 
import heronarts.lx.parameter.*; 
import heronarts.p2lx.video.*; 
import heronarts.p2lx.ui.*; 
import heronarts.lx.*; 
import heronarts.lx.audio.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class DreamlandDemo extends PApplet {

// Get all our imports out of the way















// Let's work in feet and inches
final static int INCHES = 1;
final static int FEET = 12 * INCHES;

// Top-level, we have a model and a P2LX instance
Model model;
P2LX lx;

// Setup establishes the windowing and LX constructs
public void setup() 
{
	// Dimension of the window
	size(1200, 800, OPENGL); 

	//Create the model of Dreamland
	model = new Model();

	// Create the P2LX engine for Dreamland
	lx = new P2LX(this, model);

	// Patterns setup
	lx.setPatterns(new LXPattern[] 
	{
		new LayerDemoPattern(lx),
		new IteratorTestPattern(lx),
		new SolidColorPattern(lx, 100),
		new BaseHuePattern(lx)
	});

	// Add pieces of the UI
	lx.ui.addLayer(
		// Add a 3D scene with a camera. Mouse movements control the camera
		new UI3dContext(lx.ui){}

		// Look at center of model
		.setCenter(model.cx, model.cy, model.cz)

		// Position ourself some distance away from model
		.setRadius(40 * FEET)

		// Set how fast the UI can rotate rad/s
		.setRotateVelocity(12 * PI)

		// Set how fast the UI can rotational acceleration
		.setRotateAcceleration(3 * PI)

		// Add a point cloud representing the LEDs
		.addComponent(new UIPointCloud(lx,model).setPointWeight(10))
	);

	// Basic 2-D contorol for channel with draggable windows
	
	// Grabs channel 0
	lx.ui.addLayer(new UIChannelControl(lx.ui, lx.engine.getChannel(0), 4, 4)); 
	
	// Threaded control and FPS
	lx.ui.addLayer(new UIEngineControl(lx.ui, 4, 326)); 
	
	// Various sliders, knobs and buttons
	lx.ui.addLayer(new UIComponentsDemo(lx.ui, width-144, 4)); 

	buildOutputs();
}

public void draw() 
{
    background(0xff292929);
}


/* Build a simple model of Dreamlands LED layout 
*/
static class Model extends LXModel 
{
  
  public Model() 
  {
    super(new Fixture());
  }
  
  private static class Fixture extends LXAbstractFixture 
  {
    private static final int OFFSET = 2 * FEET;
    private static final int NUMBER_OF_LEGS = 9;
    private static final int NUMBER_OF_LEDS_PER_LEG = 16;
    
    private Fixture() 
    {
      // Here's the core loop where we generate the positions
      // of the points in our model
      // for (int n = 0; n < NUMBER_OF_LEGS; ++n)
      for (int ledPoint = 0; ledPoint < NUMBER_OF_LEDS_PER_LEG; ++ledPoint) 
      {
        int ledLocation = ledPoint * FEET + OFFSET;
        // for (int ledPoint = 0; ledPoint < NUMBER_OF_LEDS_PER_LEG; ++ledPoint) 
        for (int n = 0; n < NUMBER_OF_LEGS; ++n)
        {
          // int ledLocation = ledPoint * FEET + OFFSET;
          float rx = ledLocation * cos( 2 * PI * n / NUMBER_OF_LEGS);
          float ry = ledLocation * sin(2 * PI * n / NUMBER_OF_LEGS);
            // Add point to the fixtuure
            addPoint(new LXPoint(rx,ry));
        }
      }
    }
  }
}

/**
 * This file has a bunch of example patterns, each illustrating the key
 * concepts and tools of the LX framework.
 */
 
class LayerDemoPattern extends LXPattern {
  
  private final BasicParameter colorSpread = new BasicParameter("Clr", 3, 0, 3);
  private final BasicParameter stars = new BasicParameter("Stars", 100, 0, 100);
  private final BasicParameter sat = new BasicParameter("sat",100, 0, 100);
  private final BasicParameter brightPercent = new BasicParameter("Bright %", 1, 0, 1);
  private final BasicParameter sinPeriod = new BasicParameter("Period", 11000, 0, 1);

  
  public LayerDemoPattern(LX lx) 
  {
    super(lx);
    addParameter(colorSpread);
    addParameter(stars);
    addParameter(sat);
    addParameter(brightPercent);
    addParameter(sinPeriod);
    addLayer(new CircleLayer(lx));
    // addLayer(new RodLayer(lx));
    // for (int i = 0; i < 200; ++i) {
    //   addLayer(new StarLayer(lx));
    // }
  }
  
  public void run(double deltaMs) {
    // The layers run automatically
  }
  
  private class CircleLayer extends LXLayer {
    
    private final SinLFO xPeriod = new SinLFO(3400, 7900, 11000); 
    private final SinLFO brightnessX = new SinLFO(model.xMin, model.xMax, xPeriod);
  
    private CircleLayer(LX lx) {
      super(lx);
      addModulator(xPeriod).start();
      addModulator(brightnessX).start();
    }
    
    public void run(double deltaMs) {
      // The layers run automatically
      float falloff = 100 / (4*FEET);
      for (LXPoint p : model.points) {
        float yWave = model.yRange/2 * sin(p.x / model.xRange * PI); 
        float distanceFromCenter = dist(p.x, p.y, model.cx, model.cy);
        float distanceFromBrightness = dist(p.x, abs(p.y - model.cy), brightnessX.getValuef(), yWave);
        colors[p.index] = LXColor.hsb(
          lx.getBaseHuef() + colorSpread.getValuef() * distanceFromCenter,
          sat.getValuef(),
          max(0, 100 - falloff*distanceFromBrightness) * brightPercent.getValuef()
        );
      }
    }
  }
  
  // private class RodLayer extends LXLayer {
    
  //   private final SinLFO zPeriod = new SinLFO(2000, 5000, 9000);
  //   private final SinLFO zPos = new SinLFO(model.zMin, model.zMax, zPeriod);
    
  //   private RodLayer(LX lx) {
  //     super(lx);
  //     addModulator(zPeriod).start();
  //     addModulator(zPos).start();
  //   }
    
  //   public void run(double deltaMs) {
  //     for (LXPoint p : model.points) {
  //       float b = 100 - dist(p.x, p.y, model.cx, model.cy) - abs(p.z - zPos.getValuef());
  //       if (b > 0) {
  //         addColor(p.index, LXColor.hsb(
  //           lx.getBaseHuef() + p.z,
  //           sat.getValuef(),
  //           b * brightPercent.getValuef()
  //         ));
  //       }
  //     }
  //   }
  // }
  
  // private class StarLayer extends LXLayer {
    
  //   private final TriangleLFO maxBright = new TriangleLFO(0, stars, random(2000, 8000));
  //   private final SinLFO brightness = new SinLFO(-1, maxBright, random(3000, 9000)); 
    
  //   private int index = 0;
    
  //   private StarLayer(LX lx) { 
  //     super(lx);
  //     addModulator(maxBright).start();
  //     addModulator(brightness).start();
  //     pickStar();
  //   }
    
  //   private void pickStar() {
  //     index = (int) random(0, model.size-1);
  //   }
    
  //   public void run(double deltaMs) {
  //     if (brightness.getValuef() <= 0) {
  //       pickStar();
  //     } else {
  //       addColor(index, LXColor.hsb(lx.getBaseHuef(), 50, brightness.getValuef()));
  //     }
  //   }
  // }
}
/**
 * Here's a simple extension of a camera component. This will be
 * rendered inside the camera view context. We just override the
 * onDraw method and invoke Processing drawing methods directly.
 */

class UIEngineControl extends UIWindow {
  
  final UIKnob fpsKnob;
  
  UIEngineControl(UI ui, float x, float y) {
    super(ui, "THREADS AND FPS", x, y, UIChannelControl.WIDTH, 96);
        
    y = UIWindow.TITLE_LABEL_HEIGHT;
    new UIButton(4, y, width-8, 20) {
      protected void onToggle(boolean enabled) {
        lx.engine.setThreaded(enabled);
        fpsKnob.setEnabled(enabled);
      }
    }
    .setActiveLabel("Multi-Threaded")
    .setInactiveLabel("Single-Threaded")
    .addToContainer(this);
    
    y += 24;
    fpsKnob = new UIKnob(4, y);    
    fpsKnob
    .setParameter(lx.engine.framesPerSecond)
    .setEnabled(lx.engine.isThreaded())
    .addToContainer(this);
  }
}

class UIComponentsDemo extends UIWindow {
  
  static final int NUM_KNOBS = 4; 
  final BasicParameter[] knobParameters = new BasicParameter[NUM_KNOBS];  
  
  UIComponentsDemo(UI ui, float x, float y) {
    super(ui, "UI COMPONENTS", x, y, 140, 10);
    
    for (int i = 0; i < knobParameters.length; ++i) {
      knobParameters[i] = new BasicParameter("Knb" + (i+1), i+1, 0, 4);
      knobParameters[i].addListener(new LXParameterListener() {
        public void onParameterChanged(LXParameter p) {
          println(p.getLabel() + " value:" + p.getValue());
        }
      });
    }
    
    y = UIWindow.TITLE_LABEL_HEIGHT;
    
    new UIButton(4, y, width-8, 20)
    .setLabel("Toggle Button")
    .addToContainer(this);
    y += 24;
    
    new UIButton(4, y, width-8, 20)
    .setActiveLabel("Boop!")
    .setInactiveLabel("Momentary Button")
    .setMomentary(true)
    .addToContainer(this);
    y += 24;
    
    for (int i = 0; i < 4; ++i) {
      new UIKnob(4 + i*34, y)
      .setParameter(knobParameters[i])
      .setEnabled(i % 2 == 0)
      .addToContainer(this);
    }
    y += 48;
    
    for (int i = 0; i < 4; ++i) {
      new UISlider(UISlider.Direction.VERTICAL, 4 + i*34, y, 30, 60)
      .setParameter(new BasicParameter("VSl" + i, (i+1)*.25f))
      .setEnabled(i % 2 == 1)
      .addToContainer(this);
    }
    y += 64;
    
    for (int i = 0; i < 2; ++i) {
      new UISlider(4, y, width-8, 24)
      .setParameter(new BasicParameter("HSl" + i, (i + 1) * .25f))
      .setEnabled(i % 2 == 0)
      .addToContainer(this);
      y += 28;
    }
    
    new UIToggleSet(4, y, width-8, 24)
    .setParameter(new DiscreteParameter("Ltrs", new String[] { "A", "B", "C", "D" }))
    .addToContainer(this);
    y += 28;
    
    for (int i = 0; i < 4; ++i) {
      new UIIntegerBox(4 + i*34, y, 30, 22)
      .setParameter(new DiscreteParameter("Dcrt", 10))
      .addToContainer(this);
    }
    y += 26;
    
    new UILabel(4, y, width-8, 24)
    .setLabel("This is just a label.")
    .setAlignment(CENTER, CENTER)
    .setBorderColor(ui.theme.getControlDisabledColor())
    .addToContainer(this);
    y += 28;
    
    setSize(width, y);
  }
} 
/* Build FadeCandy output */

public void buildOutputs()
{
	lx.addOutput(new FadecandyOutput(lx, "192.168.2.2", 7890));
}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "DreamlandDemo" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
