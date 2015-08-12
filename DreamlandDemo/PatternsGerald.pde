class HelloWorldPattern extends DLPattern
{ 
	private final BasicParameter colorChangeSpeed = new BasicParameter("SPD",  5000, 0, 10000);
 	private final SawLFO whatColor = new SawLFO(0, 360, colorChangeSpeed);
 	private  int counter = 1;
    
	public HelloWorldPattern(LX lx)
	{
      super(lx);
      addParameter(colorChangeSpeed);
      addModulator(whatColor).trigger();
      // addLayer(new CylinderColor(lx));
      for(int i = 0; i < 3; i++)
      {
      	addLayer(new BenchColor(lx, i, 255 / 3 * counter));
      	counter += 1;
      }
    }

    public void run(double deltaMs) {
    // The layers run automatically
    }

    private class BenchColor extends DLLayer
    {
    	int benchNum;
    	int modifier;
    	private BenchColor(LX lx, int n, int m)
    	{
    		super(lx);
    		this.benchNum = n;
    		this.modifier = m;
    	}

		public void run(double deltaMs)
		{
			for (LXPoint p : model.innerBenches.get(benchNum).points) 
			{
				float h = whatColor.getValuef();
		    	int s = 100;
		    	int b = 100;
		    	colors[p.index]=lx.hsb(h + modifier, s, b);
			} 

			for (LXPoint p : model.outerBenches.get(benchNum).points) 
			{
				float h = 255 - whatColor.getValuef();
		    	int s = 100;
		    	int b = 100;
		    	colors[p.index]=lx.hsb(h + modifier, s, b);
			} 
		}		
    } 
}

// BarbershopLamppostsPattern is a white pole with a red line that looks like it's rotating.
class ColorBarbershopLamppostsPattern extends DLPattern
{
	private final BasicParameter rotationalSpeed = new BasicParameter("SPD",  10000, 1000);
	private final SawLFO saw_var = new SawLFO(0, 6, 5000);
	final BasicParameter user_var = new BasicParameter("HUE", 0, 0, 255);

	public ColorBarbershopLamppostsPattern(LX lx)
	{
		super(lx);
		saw_var.setPeriod(rotationalSpeed);
		addParameter(rotationalSpeed);
		addParameter(user_var);
		addModulator(saw_var).trigger();
		addLayer(new CylinderColor(lx));
	}

	public void run(double deltaMs) {
	}

	private class CylinderColor extends DLLayer
	{
		List <HashMap<Float,Integer>> height_map_list = new ArrayList();
		List <HashMap<Float,Integer>> theta_map_list = new ArrayList();
		private CylinderColor(LX lx)
		{
			super(lx);
			for (LampPost m : model.lampPosts) {
				HashMap <Float,Integer> heights = new HashMap <Float,Integer>();
				HashMap <Float,Integer> theta_poses = new HashMap <Float,Integer>();
				for (LXPoint p : m.points) {
					heights.put(p.y, 1);
					theta_poses.put(atan2(p.z - m.cz, p.x - m.cx), 1);
				}
				FloatList height_set = new FloatList(heights.keySet());
				FloatList theta_set = new FloatList(theta_poses.keySet());
				height_set.sort();
				theta_set.sort();
				HashMap <Float,Integer> height_map = new HashMap <Float,Integer>();
				int i = 0;
				for (float f : height_set) {
					height_map.put(f,i);
					++i;
				}
				HashMap <Float,Integer> theta_map = new HashMap <Float,Integer>();
				i = 0;
				for (float f : theta_set) {
					theta_map.put(f,i);
					++i;
				}
				height_map_list.add(height_map);
				theta_map_list.add(theta_map);
			}
		}

		public void run(double deltaMs)
		{
			for (int i = 0; i < 3; ++i) {
				LampPost m = model.lampPosts.get(i);
				HashMap <Float,Integer> height_map = height_map_list.get(i);
				HashMap <Float,Integer> theta_map = theta_map_list.get(i);
				for (LXPoint p : m.points) {
					int theta = theta_map.get(atan2(p.z - m.cz, p.x - m.cx));
					int osc = int(saw_var.getValuef());
					int h = height_map.get(p.y);
					if (
						((theta + osc) % 7 == h % 7) ||
						((theta + osc + 4) % 7 == h % 7)
					) {
						colors[p.index] = lx.hsb(
							user_var.getValuef(),
							100,
							100);
					} else {
						colors[p.index] = lx.hsb(
							100,
							100,
							0);
					}
				}
			}
		}
	}
}

class PythonProjection extends DLPattern 
{
  private final LXProjection rotation;
  private final BasicParameter thick = new BasicParameter("thick", 1, 0, 200);

  public PythonProjection(LX lx) 
  {
    super(lx);
    rotation = new LXProjection(model.carousel);
    addParameter(thick);
  }

  public void run(double deltaMs) 
  {
    rotation.reset();
    rotation.center(); // assuming you want to rotate about the center of your model?
    rotation.rotateZ(rotationPosition); // or whatever is appropriate
    float hv = lx.getBaseHuef();
    for (LXVector c : rotation) {
      float d = max(0, abs(c.y) - thick.getValuef() + .1f*abs(c.z) + .02f*abs(c.x)); // plane / spear thing
      colors[c.index] = lx.hsb(
        100,
        100,
        constrain(140 - 40*d, 0, 100)
      );
    }
  }
} 
