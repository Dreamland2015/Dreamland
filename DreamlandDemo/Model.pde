/* Build a simple model of Dreamlands LED layout 
*/
static class Model extends LXModel 
{
  
  public Model() 
  {
    super(new Fixture());
  }
  
  private static class Fixture extends LXAbstractFixture 
  {
    private static final int OFFSET = 2 * FEET;
    private static final int NUMBER_OF_LEGS = 9;
    private static final int NUMBER_OF_LEDS_PER_LEG = 16;
    
    private Fixture() 
    {
      // Here's the core loop where we generate the positions
      // of the points in our model
      // for (int n = 0; n < NUMBER_OF_LEGS; ++n)
      for (int ledPoint = 0; ledPoint < NUMBER_OF_LEDS_PER_LEG; ++ledPoint) 
      {
        int ledLocation = ledPoint * FEET + OFFSET;
        // for (int ledPoint = 0; ledPoint < NUMBER_OF_LEDS_PER_LEG; ++ledPoint) 
        for (int n = 0; n < NUMBER_OF_LEGS; ++n)
        {
          // int ledLocation = ledPoint * FEET + OFFSET;
          float rx = ledLocation * cos( 2 * PI * n / NUMBER_OF_LEGS);
          float ry = ledLocation * sin(2 * PI * n / NUMBER_OF_LEGS);
            // Add point to the fixtuure
            addPoint(new LXPoint(rx,ry));
        }
      }
    }
  }
}

