import ddf.minim.*;
import heronarts.lx.*;

P2LX lx;

//private final int BG_COLOR = #292929;
private final int WARNING_RED_COLOR = #B33A3A;

class DreamlandFireEnablePanel extends UIWindow {

	private final int BG_COLOR = UI.get().theme.getControlBackgroundColor();
	protected int DEFAULT_ACTIVE_COLOR = UI.get().theme.getPrimaryColor();
	protected int DEFAULT_INACTIVE_COLOR = UI.get().theme.getControlBackgroundColor();
	
	protected String[] DISABLED_TEXT = {"DISABLED", "DISABLED"};
	protected String[] ENABLED_TEXT = {"Fire!", "Firing..."};

	private final int ELEMENT_WIDTH = 80;
	UIButton enable;
	UIButton fire;
	boolean fire_enabled;
	DreamlandFireEnablePanel(UI ui, String title, float panel_x, float panel_y) {
		super(ui, title, panel_x, panel_y, 100, 130);

		int y = 20;
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
			}
		};
		enable.setActiveLabel("Enabled!")
			.setInactiveLabel("Disabled")
			.addToContainer(this);
		y += 50;

		fire = new UIButton(5, y, ELEMENT_WIDTH, 45) {
			protected void onToggle(boolean enabled) {
				if (fire_enabled && enabled) {
					println("pressed!", enabled);
				}
			}
		};
		fire.setMomentary(true)	
			.addToContainer(this);
		// Hacky workaround
		enable.setActive(true);
		enable.setActive(false);
	}
}

class DreamlandControlPanelUI extends UIWindow {
	private final int ELEMENT_WIDTH = 80;

	DreamlandControlPanelUI(UI ui) {
		super(ui, "CtrlPanel", 0, 0, 100, 800);
		println("created!");
		new DreamlandFireEnablePanel(ui, "Fire1", 0, 30).addToContainer(this);
		new DreamlandFireEnablePanel(ui, "Fire2", 0, 160).addToContainer(this);
		new DreamlandFireEnablePanel(ui, "Fire3", 0, 290).addToContainer(this);
	}
}


void setup() 
{
	size(1200, 800); 
	//colorMode(RGB, );
	background(#292929);

	lx = new P2LX(this);
	lx.ui.addLayer(new DreamlandControlPanelUI(lx.ui)); 
}

void draw() 
{
	// Processing/P2LX needs this to process actions, even though it's a NOP.
}


