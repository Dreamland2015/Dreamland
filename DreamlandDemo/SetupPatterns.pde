class LampPostBarIterator extends DLPattern
{
	private final BasicParameter num = new BasicParameter("num" ,0 ,0 ,6);
	private final SawLFO counter = new SawLFO(0, 6, 1000);

	public LampPostBarIterator(LX lx)
	{
		super(lx);
		addParameter(num);
		addModulator(counter).trigger();
	}

	public void run(double deltaMs) 
	{
		for (LampPost lp : model.lampPosts)
		{
			for(int i = 0; i < 7; i ++)
			{
				for(LXPoint p : lp.bars.get(i).points)
				{
					colors[p.index] = LXColor.BLACK;
				}
			}
			for (LXPoint p : lp.bars.get((int) num.getValuef()).points)
			{
				colors[p.index] = LXColor.WHITE;
			}
		}
	}
}

class CarouselBarIterator extends DLPattern
{
	private final BasicParameter num = new BasicParameter("num" ,0 ,0 ,17);

	public CarouselBarIterator(LX lx)
	{
		super(lx);
		addParameter(num);
	}

	public void run(double deltaMs) 
	{
		Carousel c = model.carousel;

		for(int i = 0; i < 18; i ++)
		{
			for(LXPoint p : c.bars.get(i).points)
			{
				colors[p.index] = LXColor.BLACK;
			}
		}
		for (LXPoint p : c.bars.get((int) num.getValuef()).points)
		{
			colors[p.index] = LXColor.WHITE;
		}
	}
}

class CarouselBarPointIterator extends DLPattern
{
	private final BasicParameter num = new BasicParameter("num" ,0 ,0 ,17);
	private final BasicParameter pointNum = new BasicParameter("point" ,0 ,0 ,33);

	public CarouselBarPointIterator(LX lx)
	{
		super(lx);
		addParameter(num);
		addParameter(pointNum);
	}

	public void run(double deltaMs) 
	{
		Carousel c = model.carousel;

		for(int i = 0; i < 18; i ++)
		{
			for(LXPoint p : c.bars.get(i).points)
			{
				colors[p.index] = LXColor.BLACK;
			}
		}
		List<LXPoint> bar = c.bars.get((int) num.getValuef()).points;

		for(int i = 0; i < 34; i ++)
		{
			for(LXPoint p : bar)
			{
				colors[p.index] = LXColor.BLACK;
			}
		colors[bar.get((int) pointNum.getValuef()).index] = LXColor.WHITE;
		}
	}
}

class CarouselArmIterator extends DLPattern
{
	private final BasicParameter num = new BasicParameter("num" ,0 ,0 ,8);

	public CarouselArmIterator(LX lx)
	{
		super(lx);
		addParameter(num);
	}

	public void run(double deltaMs) 
	{
		Carousel c = model.carousel;

		for(int i = 0; i < 9; i ++)
		{
			for(LXPoint p : c.arms.get(i).points)
			{
				colors[p.index] = LXColor.BLACK;
			}
		}
		for (LXPoint p : c.arms.get((int) num.getValuef()).points)
		{
			colors[p.index] = LXColor.WHITE;
		}
	}
}

class StructureIterator extends DLPattern
{
	private final BasicParameter num = new BasicParameter("num", 0, 0, 2);

	public StructureIterator(LX lx)
	{
		super(lx);
		addParameter(num);
	}

	public void run(double deltaMs)
	{
		for(int i = 0; i < 3; i ++)
		{
			for(LXPoint p : model.outerBenches.get(i).points)
			{
				colors[p.index] = LXColor.BLACK;
			}
			for(LXPoint p : model.innerBenches.get(i).points)
			{
				colors[p.index] = LXColor.BLACK;
			}
			for(LXPoint p : model.lampPosts.get(i).points)
			{
				colors[p.index] = LXColor.BLACK;
			}
			for(LXPoint p : model.kaleidoscopes.get(i).points)
			{
				colors[p.index] = LXColor.BLACK;
			}
		}
		for (LXPoint p : model.outerBenches.get((int) num.getValuef()).points)
		{
			colors[p.index] = LXColor.WHITE;
		}

		for (LXPoint p : model.innerBenches.get((int) num.getValuef()).points)
		{
			colors[p.index] = LXColor.WHITE;
		}

		for (LXPoint p : model.lampPosts.get((int) num.getValuef()).points)
		{
			colors[p.index] = LXColor.WHITE;
		}

		for (LXPoint p : model.kaleidoscopes.get((int) num.getValuef()).points)
		{
			colors[p.index] = LXColor.WHITE;
		}
	}
}

class LampPostBarPointIterator extends DLPattern
{
	private final BasicParameter num = new BasicParameter("num" ,0 ,0 ,6);
	private final BasicParameter pointNum = new BasicParameter("point" ,0 ,0 ,18);

	public LampPostBarPointIterator(LX lx)
	{
		super(lx);
		addParameter(num);
		addParameter(pointNum);
	}

	public void run(double deltaMs) 
	{
		// List<LampPost> c = model.lampPosts;

		for (LampPost c : model.lampPosts)
		{
			for(int i = 0; i < 6; i ++)
			{
				for(LXPoint p : c.bars.get(i).points)
				{
					colors[p.index] = LXColor.BLACK;
				}
			}
			List<LXPoint> bar = c.bars.get((int) num.getValuef()).points;

			// for(LXPoint bar : c.bars.get((int) num.getValuef()).points)
			// {
				for(int i = 0; i < 18; i ++)
				{
					for(LXPoint p : bar)
					{
						colors[p.index] = LXColor.BLACK;
					}
				colors[bar.get((int) pointNum.getValuef()).index] = LXColor.WHITE;
				// }
			}
		}
	}
}

class LampPostRing extends DLPattern
{
	private final BasicParameter ringNum = new BasicParameter("ringNum", 0, 0, 18);
	private final TriangleLFO triangle = new TriangleLFO(0, 18, 2000);

	public LampPostRing(LX lx)
	{
		super(lx);
		addParameter(ringNum);
		addModulator(triangle).trigger();
	}

	public void run(double deltaMs)
	{
		for(LampPost lp : model.lampPosts)
		{
			for(int i = 0; i < 6; i ++)
			{
				for(LXPoint p : lp.bars.get(i).points)
				{
					colors[p.index] = LXColor.BLACK;
				}
			}
		}

		for(LampPost lp : model.lampPosts)
			{
			for(int i = 0; i < 6; i ++)
			{
				List<LXPoint> bar = lp.bars.get(i).points;
				for(int ii = 0; ii < 18; ii ++)
				{
					for(LXPoint p : bar)
					{
						colors[p.index] = LXColor.BLACK;
					}
				// colors[bar.get((int) ringNum.getValuef()).index] = LXColor.WHITE;
				colors[bar.get((int) triangle.getValuef()).index] = LXColor.WHITE;
				}
			}
		}
	}
}