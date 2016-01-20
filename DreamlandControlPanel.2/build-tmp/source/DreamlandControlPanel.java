import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import ddf.minim.*; 
import heronarts.lx.*; 
import heronarts.lx.transform.*; 
import org.zeromq.ZMQ; 

import heronarts.p2lx.ui.control.*; 
import ddf.minim.*; 
import heronarts.p2lx.font.*; 
import heronarts.p2lx.*; 
import toxi.math.waves.*; 
import zmq.*; 
import toxi.geom.mesh2d.*; 
import heronarts.lx.midi.device.*; 
import heronarts.lx.modulator.*; 
import com.google.gson.annotations.*; 
import heronarts.lx.output.*; 
import ddf.minim.signals.*; 
import toxi.util.datatypes.*; 
import heronarts.lx.audio.*; 
import toxi.math.conversion.*; 
import heronarts.lx.*; 
import org.zeromq.*; 
import toxi.math.*; 
import heronarts.lx.color.*; 
import com.google.gson.internal.*; 
import toxi.math.noise.*; 
import ddf.minim.ugens.*; 
import ddf.minim.effects.*; 
import com.google.gson.stream.*; 
import heronarts.lx.pattern.*; 
import toxi.geom.mesh.subdiv.*; 
import ddf.minim.analysis.*; 
import com.google.gson.internal.bind.*; 
import toxi.geom.mesh.*; 
import heronarts.lx.effect.*; 
import heronarts.lx.transform.*; 
import heronarts.p2lx.ui.*; 
import heronarts.lx.parameter.*; 
import com.google.gson.*; 
import heronarts.p2lx.video.*; 
import heronarts.p2lx.ui.component.*; 
import heronarts.lx.transition.*; 
import toxi.util.events.*; 
import heronarts.lx.midi.*; 
import com.google.gson.reflect.*; 
import heronarts.lx.model.*; 
import ddf.minim.spi.*; 
import toxi.util.*; 
import toxi.geom.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class DreamlandControlPanel extends PApplet {





String master = "localhost";

P2LX lx;

//private final int BG_COLOR = #292929;
private final int WARNING_RED_COLOR = 0xffB33A3A;

ControlPanelUI cpui;
public UIButton fire1;

class FireEnablePanel extends UIWindow {

	private final int BG_COLOR = UI.get().theme.getControlBackgroundColor();
	protected int DEFAULT_ACTIVE_COLOR = UI.get().theme.getPrimaryColor();
	protected int DEFAULT_INACTIVE_COLOR = UI.get().theme.getControlBackgroundColor();
	
	protected String[] DISABLED_TEXT = {"DISABLED", "DISABLED"};
	protected String[] ENABLED_TEXT = {"Fire!", "Firing..."};
	String topic;
	String which;
	private final int ELEMENT_WIDTH = 80;
	UIButton enable;
	UIButton fire;
	boolean fire_enabled;
	FireEnablePanel(UI ui, String myTopic, String myWhich, float panel_x, float panel_y) {
		super(ui, myTopic + " " + myWhich, panel_x, panel_y, 100, 130);
		this.topic = myTopic;
		this.which = myWhich;

		int y = 30;
		enable = new UIButton(5, y, ELEMENT_WIDTH, 45) {
			public void onToggle(boolean enabled) {
				int bgcol;
				int fgcol;
				int activeCol;
				int inactiveCol;
				String []bu_text;

				if (enabled){
					fire_enabled = true;
					activeCol = DEFAULT_ACTIVE_COLOR;
					inactiveCol = DEFAULT_INACTIVE_COLOR;
					bu_text = ENABLED_TEXT;
				} else {
					fire_enabled = false;
					activeCol = WARNING_RED_COLOR;
					inactiveCol = WARNING_RED_COLOR;
					bu_text = DISABLED_TEXT;
				}
				fire.setActiveColor(activeCol);
				fire.setInactiveColor(inactiveCol);
				fire.setBackgroundColor(inactiveCol);
				fire.setActiveLabel(bu_text[1]);
				fire.setInactiveLabel(bu_text[0]);
				fire.setActive(false);
			}
		};
		enable.setActiveLabel("Enabled!")
			.setInactiveLabel("Disabled")
			.addToContainer(this);
		y += 50;

		fire = new UIButton(5, y, ELEMENT_WIDTH, 45) {
			ZMQ_pub pub = new ZMQ_pub(master, topic, which);
			protected void onToggle(boolean enabled) {
				if (fire_enabled && enabled) {
					pub.sendMessage("0");
					println(topic + "|" + which + " on");
				} else {
					pub.sendMessage("1");
					println(topic + "|" + which + " off");
				}
			}
		};
		fire.setMomentary(true)	
			.addToContainer(this);
		// Hacky workaround by setting it true first.
		enable.setActive(true);
		enable.setActive(false);
	}
}

class ControlPanelUI extends UIWindow {
	// private final int ELEMENT_WIDTH = 80;

	ControlPanelUI(UI ui) {
		super(ui, "CtrlPanel", 0, 0, 230, 600);
		println("created!");
		int x = 10;
		int y = 30;
		int VERT_OFFSET = 140;
		// Fire on main Carousel (4)
		FireEnablePanel fpanel_c1 =
			new FireEnablePanel(ui, "carousel-top", "flame1", x, y);
		fpanel_c1.addToContainer(this);
		//fire1 = fpanel1.fire;
		y += VERT_OFFSET;
		FireEnablePanel fpanel2 =
			new FireEnablePanel(ui, "carousel-top", "flame2", x, y);
		fpanel2.addToContainer(this);
		y += VERT_OFFSET;
		FireEnablePanel fpanel3 =
			new FireEnablePanel(ui, "carousel-top", "flame3", x, y);
		fpanel3.addToContainer(this);
		y += VERT_OFFSET;
		FireEnablePanel fpanel4 =
			new FireEnablePanel(ui, "carousel-top", "center", x, y);
		fpanel4.addToContainer(this);

		x = 120;
		y = 30;
		// Fire on lanterns (3)
		FireEnablePanel fpanel5 =
			new FireEnablePanel(ui, "lampPost1", "flame", x, y);
		fpanel5.addToContainer(this);
		y += VERT_OFFSET;
		FireEnablePanel fpanel6 =
			new FireEnablePanel(ui, "lampPost2", "flame", x, y);
		fpanel6.addToContainer(this);
		y += VERT_OFFSET;
		FireEnablePanel fpanel7 =
			new FireEnablePanel(ui, "lampPost3", "flame", x, y);
		fpanel7.addToContainer(this);
		y += VERT_OFFSET;

	}
}


public void setup()
{
	size(230, 600);
	//colorMode(RGB, );
	background(0xff292929);

	lx = new P2LX(this);
	cpui = new ControlPanelUI(lx.ui);
	lx.ui.addLayer(cpui);

	thread("zeromq_sub");
}

public void draw()
{
    fire_off();
	// Processing/P2LX needs this to process actions, even though it's a NOP.
}

//ZMQ_pub pub = new ZMQ_pub(master, topic, which);
ZMQ_pub top1 = new ZMQ_pub(master, "center-top", "flame1");
int top1_off_millis = 0;

public void fire_off()
{
    //top1
    top1.sendMessage("0");
    println(topic + "|" + which + " off");
}

public void fire()
{
    top1.sendMessage("1");
    top1_off_millis = millis() + 20;
/** 
    if (fire_enabled && enabled) {
        top1.sendMessage("1");
        println(topic + "|" + which + " on");
    } else {
        pub.sendMessage("1");
        println(topic + "|" + which + " off");
    }
**/
}

public void keyPressed() {
  println("idx "+keyCode);
  if (keyCode >=112 && keyCode <= 8){
    switch(keyCode){
        case 112: fire(); break;
        case 113: break;
        case 114: break;
        case 115: break;
        case 116: break;
        case 117: break;
        case 118: break;
            
    }
  }
}


public void zeromq_sub() {
    ZMQ.Context context = ZMQ.context(1);
    ZMQ.Socket subscriber = context.socket(ZMQ.SUB);
    subscriber.connect("tcp://localhost:6000");
    subscriber.subscribe("".getBytes());
    while (!Thread.currentThread ().isInterrupted ()) {
	// Parse message
        String full_message = subscriber.recvStr();
        println(full_message);

	String []addr_tokens = full_message.split("[|]");
	print(addr_tokens);
	String address = addr_tokens[0];
	String []action_tokens = addr_tokens[1].split("[#]");
	print(action_tokens);
	String action = action_tokens[0];
	int value = Integer.parseInt(action_tokens[1]);

        //float number = Float.parseFloat(contents);
	println();
	println("addr", address);
	println("act", action);
	println("value", value);
	println();

	if (address.equals("thing") && action.equals("flame1")) {
		println("doing it...");
		fire1.setActive(value == 1);
	} else {
		println("no?");
	}


        //rotationPosition = number;

	println();
	println();
	println();
    }
    subscriber.close ();
    context.term ();
}


class ZMQ_pub {
	String message;
	String topic;
	String which;
	ZMQ.Socket publisher;

	public ZMQ_pub(String master, String topic, String which){
        ZMQ.Context context = ZMQ.context(1);
        this.publisher = context.socket(ZMQ.PUB);
        this.publisher.connect("tcp://" + master + ":6001");
		this.topic = topic;
		this.which = which;
	}

	public void sendMessage(String value){
		String sayWhat = this.topic + "|" + this.which + "#" + value;
        this.publisher.send(sayWhat);
	}
}
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "DreamlandControlPanel" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
