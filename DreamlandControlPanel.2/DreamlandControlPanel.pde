import ddf.minim.*;
import heronarts.lx.*;
import heronarts.lx.transform.*;

String master = "localhost";

P2LX lx;

//private final int BG_COLOR = #292929;
private final int WARNING_RED_COLOR = #B33A3A;

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


void setup()
{
	size(230, 600);
	//colorMode(RGB, );
	background(#292929);

	lx = new P2LX(this);
	cpui = new ControlPanelUI(lx.ui);
	lx.ui.addLayer(cpui);

	thread("zeromq_sub");
}

void draw()
{
    fire_off();
	// Processing/P2LX needs this to process actions, even though it's a NOP.
}

//ZMQ_pub pub = new ZMQ_pub(master, topic, which);
//ZMQ_pub top1 = new ZMQ_pub(master, "center-top", "flame1");
////int 
//int top1_off_millis = 0;

void fire_off()
{
    if (top1_off_millis > 
    //top1
    top1.sendMessage("0");
    println(topic + "|" + which + " off");
}

void fire()
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

void keyPressed() {
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
