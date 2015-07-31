class HelloWorldPattern extends DLPattern
{ 
	private final BasicParameter colorChangeSpeed = new BasicParameter("SPD",  5000, 0, 10000);
 	private final SinLFO whatColor = new SinLFO(0, 255, colorChangeSpeed);
    
	public HelloWorldPattern(LX lx)
	{
      super(lx);
      addParameter(colorChangeSpeed);
      addModulator(whatColor).trigger();
      // addLayer(new CylinderColor(lx));
      for(int i = 0; i < 3; i++)
      {
      	addLayer(new BenchColor(lx, i, 255 / 3 * i));
      }
    }

    public void run(double deltaMs) {
    // The layers run automatically
    }
    
    private class CylinderColor extends DLLayer
    {
    	private CylinderColor(LX lx)
    	{
    		super(lx);
    	}

		public void run(double deltaMs)
		{
			for (LXPoint p : model.carouselBottom.points) 
			{
				float h = whatColor.getValuef();
		    	int s = 100;
		    	int b = 100;
		    	colors[p.index]=lx.hsb(h, s, b);
			} 
		}	
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
