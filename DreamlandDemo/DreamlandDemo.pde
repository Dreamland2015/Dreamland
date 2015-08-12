// Get all our imports out of the way
import heronarts.lx.*;
import heronarts.lx.audio.*;
import heronarts.lx.color.*;
import heronarts.lx.model.*;
import heronarts.lx.modulator.*;
import heronarts.lx.output.*;
import heronarts.lx.parameter.*;
import heronarts.lx.pattern.*;
import heronarts.lx.transition.*;
import heronarts.lx.transform.*;
import heronarts.p2lx.*;
import heronarts.p2lx.ui.*;
import heronarts.p2lx.ui.control.*;
import ddf.minim.*;
import processing.opengl.*;
import java.util.*;
import toxi.geom.Vec2D;
import toxi.math.noise.PerlinNoise;
import toxi.math.noise.SimplexNoise;


// Let's work in feet and inches
final static int INCHES = 1;
final static int FEET = 12 * INCHES;
float rotationPosition = 0f;

// Top-level, we have a model and a P2LX instance
Model           model;
P2LX 			lx;
LXPattern[]     patterns;
// Setup establishes the windowing and LX constructs
void setup() 
{
	// Dimension of the window
	size(1200, 800, OPENGL); 

    model = new Model();

	// Create the P2LX engine for Dreamland
	lx = new P2LX(this, model);


	// Patterns setup
	lx.setPatterns(new LXPattern[] {
		// new ControlProjectionSpeed(lx),
		new HelloWorldPattern(lx),
		new ProjectionLayerTest(lx),
		new TestXPattern(lx),
		new PythonProjection(lx),
		new IteratorTestPattern(lx).setTransition(new DissolveTransition(lx)),
		new AskewPlanes(lx),
		new MoveXPosition(lx),
		new TestHuePattern(lx),
		new TestProjectionPattern(lx),
		new TestYPattern(lx),
		new TestZPattern(lx),
		new Bouncing(lx),
		new Cascade(lx),
		new CrazyWaves(lx),
		new CrossSections(lx),
		new DFC(lx),
		new LayerDemoPattern(lx),
		new ParameterWave(lx),
		new Pulley(lx),
		new Pulse(lx),
		new RainbowInsanity(lx),
		new SeeSaw(lx),
		new ShiftingPlane(lx),
		new SparkleTakeOver(lx),
		new Stripes(lx),
		new Strobe(lx),
		new SweepPattern(lx),
		new Twinkle(lx),
		new block(lx),
		new candycloudstar(lx),
		new rainbowfade(lx),
		new rainbowfadeauto(lx),
		new um(lx),
		new um2(lx),
		new um3_lists(lx),
		new MultiSine(lx),
		new BarbershopLamppostsPattern(lx),
		new ColorBarbershopLamppostsPattern(lx),
	});


  buildOutputs();
  thread("psenvsub");



	// Add pieces of the UI
	lx.ui.addLayer(
		// Add a 3D scene with a camera. Mouse movements control the camera
		new UI3dContext(lx.ui){}

		// Look at center of model
		.setCenter(model.cx, model.cy, 0)

		// Position ourself some distance away from model
		.setRadius(40 * FEET)

		// Set how fast the UI can rotate rad/s
		.setRotationVelocity(12 * PI)

		// Set how fast the UI can rotational acceleration
		.setRotationAcceleration(3 * PI)

		// Add a point cloud representing the LEDs
		.addComponent(new UIPointCloud(lx,model).setPointSize(3))
	);

	// Basic 2-D contorol for channel with draggable windows
	
	// Grabs channel 0
	lx.ui.addLayer(new UIChannelControl(lx.ui, lx.engine.getChannel(0), 4, 4)); 
	
	// Threaded control and FPS
	lx.ui.addLayer(new UIEngineControl(lx.ui, 4, 326));

  // Output control
  lx.ui.addLayer(new UIOutputControl(lx.ui, 4, 426));

	
	// Various sliders, knobs and buttons
	// lx.ui.addLayer(new UIComponentsDemo(lx.ui, width-144, 4)); 

}

void draw() 
{
    background(#292929);
}


