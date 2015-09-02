import ddf.minim.*;
import heronarts.lx.*;
import heronarts.lx.transform.*;

String master = "localhost";

P2LX lx;

//private final int BG_COLOR = #292929;
private final int WARNING_RED_COLOR = #B33A3A;

private final int UI_HEIGHT = 740;

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
	public UIButton fire;
	boolean fire_enabled;
	FireEnablePanel(UI ui, String myTopic, String myWhich, float panel_x, float panel_y) {
		super(ui, myTopic + " " + myWhich, panel_x, panel_y, 100, 130);
        print(myTopic + " " + myWhich);
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

        if (which == "allcenterside") {
            fire = new UIButton(5, y, ELEMENT_WIDTH, 45) {
                ZMQ_pub pub1 = new ZMQ_pub(master, topic, "flame1");
                ZMQ_pub pub2 = new ZMQ_pub(master, topic, "flame2");
                ZMQ_pub pub3 = new ZMQ_pub(master, topic, "flame3");
                protected void onToggle(boolean enabled) {
                    if (fire_enabled && enabled) {
                        pub1.sendMessage("0");
                        pub2.sendMessage("0");
                        pub3.sendMessage("0");
                        println(topic + "|" + which + " on");
                    } else {
                        pub1.sendMessage("1");
                        pub2.sendMessage("1");
                        pub3.sendMessage("1");
                        println(topic + "|" + which + " off");
                    }
                }
            };
        } else {
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
        }
		fire.setMomentary(true)	
			.addToContainer(this);
		// Hacky workaround by setting it true first.
		enable.setActive(true);
		enable.setActive(false);
	}
}

FireEnablePanel fpanel1;
FireEnablePanel fpanel2;
FireEnablePanel fpanel3;
FireEnablePanel fpanel4;
FireEnablePanel fpanel5;
FireEnablePanel fpanel6;
FireEnablePanel fpanel7;
FireEnablePanel fpanel8;

class ControlPanelUI extends UIWindow {
	// private final int ELEMENT_WIDTH = 80;

	ControlPanelUI(UI ui) {
		super(ui, "CtrlPanel", 0, 0, 230, UI_HEIGHT);
		println("created!");
		int x = 10;
		int y = 30;
		int VERT_OFFSET = 140;
		// Fire on main Carousel (4)
		fpanel1 =
			new FireEnablePanel(ui, "carousel-top", "flame1", x, y);
		fpanel1.addToContainer(this);
		//fire1 = fpanel1.fire;
		y += VERT_OFFSET;
		fpanel2 =
			new FireEnablePanel(ui, "carousel-top", "flame2", x, y);
		fpanel2.addToContainer(this);
		y += VERT_OFFSET;
		fpanel3 =
			new FireEnablePanel(ui, "carousel-top", "flame3", x, y);
		fpanel3.addToContainer(this);
		y += VERT_OFFSET;
		fpanel4 =
			new FireEnablePanel(ui, "carousel-top", "center", x, y);
		fpanel4.addToContainer(this);
		y += VERT_OFFSET;

        int y_last = y;
		x = 120;
		y = 30;
		// Fire on lanterns (3)
		fpanel5 =
			new FireEnablePanel(ui, "lampPost1", "flame", x, y);
		fpanel5.addToContainer(this);
		y += VERT_OFFSET;
		fpanel6 =
			new FireEnablePanel(ui, "lampPost2", "flame", x, y);
		fpanel6.addToContainer(this);
		y += VERT_OFFSET;
		//FireEnablePanel fpanel7 =
		fpanel7 =
			new FireEnablePanel(ui, "lampPost3", "flame", x, y);
		fpanel7.addToContainer(this);
		y += VERT_OFFSET;

		fpanel8 =
			new FireEnablePanel(ui, "carousel-top", "allcenterside", 10, y_last);
		fpanel8.addToContainer(this);
	}
}


void setup()
{
	size(230, UI_HEIGHT);
	//colorMode(RGB, );
	background(#292929);

	lx = new P2LX(this);
	cpui = new ControlPanelUI(lx.ui);
	lx.ui.addLayer(cpui);

	thread("zeromq_sub");
}

void draw()
{
	// Processing/P2LX needs this to process actions, even though it's a NOP.
}

void keyboardfire(FireEnablePanel bu, boolean level)
{
    bu.fire.setActive(level);
}

void keyPressed()
{
    //println("kcp" + keyCode);
    FireEnablePanel bu;// = NULL;
    switch(keyCode){
        case 116: bu = fpanel5; keyboardfire(bu, true); break;
        case 117: bu = fpanel6; keyboardfire(bu, true); break;
        case 118: bu = fpanel7; keyboardfire(bu, true); break;
        case 112: bu = fpanel1; keyboardfire(bu, true); break;
        case 113: bu = fpanel2; keyboardfire(bu, true); break;
        case 114: bu = fpanel3; keyboardfire(bu, true); break;
        case 115: bu = fpanel4; keyboardfire(bu, true); break;
    }
}

void keyReleased()
{
    FireEnablePanel bu;// = NULL;
    switch(keyCode){
        case 116: bu = fpanel5; keyboardfire(bu, false); break;
        case 117: bu = fpanel6; keyboardfire(bu, false); break;
        case 118: bu = fpanel7; keyboardfire(bu, false); break;
        case 112: bu = fpanel1; keyboardfire(bu, false); break;
        case 113: bu = fpanel2; keyboardfire(bu, false); break;
        case 114: bu = fpanel3; keyboardfire(bu, false); break;
        case 115: bu = fpanel4; keyboardfire(bu, false); break;
    }
}
