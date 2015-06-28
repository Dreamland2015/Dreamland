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


// Let's work in feet and inches
final static int INCHES = 1;
final static int FEET = 12 * INCHES;

// Top-level, we have a model and a P2LX instance
Model model;

P2LX lx;

// Setup establishes the windowing and LX constructs
void setup() 
{
	// Dimension of the window
	size(1200, 800, OPENGL); 

    model = new Model();

	// Create the P2LX engine for Dreamland
	lx = new P2LX(this, model);


	// Patterns setup
	lx.setPatterns(new LXPattern[] 
	{
		new TestHuePattern(lx),
		new TestXPattern(lx),
		new TestYPattern(lx),
		new TestZPattern(lx)
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
		.addComponent(new UIPointCloud(lx,model).setPointWeight(3))
	);

	// Basic 2-D contorol for channel with draggable windows
	
	// Grabs channel 0
	lx.ui.addLayer(new UIChannelControl(lx.ui, lx.engine.getChannel(0), 4, 4)); 
	
	// Threaded control and FPS
	lx.ui.addLayer(new UIEngineControl(lx.ui, 4, 326)); 
	
	// Various sliders, knobs and buttons
	// lx.ui.addLayer(new UIComponentsDemo(lx.ui, width-144, 4)); 

	// buildOutputs();
}

void draw() 
{
    background(#292929);
}


