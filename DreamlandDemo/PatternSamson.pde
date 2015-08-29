import heronarts.lx.color.LXColor;

// BarbershopLamppostsPattern is a white pole with a red line that looks like it's rotating.
class BarbershopLamppostsPattern extends DLPattern
{
	private final BasicParameter rotationalSpeed = new BasicParameter("SPD",  10000, 1000);
	private final SawLFO saw_var = new SawLFO(0, 6, 5000);
	final BasicParameter user_var = new BasicParameter("HUE", 0, 0, 6);

	public BarbershopLamppostsPattern(LX lx)
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
					if ((theta + osc) % 7 == h % 7) {
						colors[p.index] = LXColor.RED;
					} else {
						colors[p.index] = LXColor.WHITE;
					}
				}
			}
		}
	}
}

class SamPattern extends DLPattern
{
	private final BasicParameter rotationalSpeed = new BasicParameter("SPD",  10000, 1000);
	private final SawLFO saw_var = new SawLFO(0, 6, 5000);
	private final SinLFO sin_var = new SinLFO(0, 6, 5000);
	final BasicParameter user_var = new BasicParameter("HUE", 0.5, 0.5, 60);
	double xMid;
	double yMid;
	double zMid;

	public SamPattern(LX lx)
	{
		super(lx);
		saw_var.setPeriod(rotationalSpeed);
		addParameter(rotationalSpeed);
		addParameter(user_var);
		addModulator(saw_var).trigger();
		addModulator(sin_var).trigger();
		addLayer(new CylinderColor(lx));

		Model m = (DreamlandDemo.Model)lx.model;

		this.xMid = m.carousel.cx; //lx.model.xMin + (lx.model.xRange / 2);
		this.yMid = m.carousel.cy; //lx.model.yMin + (lx.model.yRange / 2);
		this.zMid = m.carousel.cz; //lx.model.zMin + (lx.model.zRange / 2);

		println("xrange: " + lx.model.xRange + "xmin: " + lx.model.xMin + "xmax: " + lx.model.xMax);
		println("yrange: " + lx.model.yRange);
	}

	public void run(double deltaMs) {
		for (int i = 0; i < 3; ++i) {
			for (LXPoint p : model.points) {
				//double bright = p.theta / 2 * 256;
				//colors[p.index] = LXColor.RED;/a//t/hsb(200, 200, p.theta);

				double bright = sin_var.getValuef() * sqrt(pow((float)(p.x - this.xMid), 2.0) + pow((float)(p.z - this.zMid), 2.0));
				colors[p.index] = LXColor.hsb(200, 200, bright);
			}
		}
	}
}
