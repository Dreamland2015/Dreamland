import java.util.*;

public static class Bench extends LXModel 
{
  public Bench() 
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
          float rx = ledLocation * cos(2 * PI * n / NUMBER_OF_LEGS);
          float ry = ledLocation * sin(2 * PI * n / NUMBER_OF_LEGS);
          // Add point to the fixtuure
          addPoint(new LXPoint(rx,ry, 5));
        }
      }
    }
  }
}


public static class Carousel extends LXModel 
{
  public Carousel() 
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
          float rx = ledLocation * cos(2 * PI * n / NUMBER_OF_LEGS);
          float ry = ledLocation * sin(2 * PI * n / NUMBER_OF_LEGS);
          // Add point to the fixtuure
          addPoint(new LXPoint(rx, ry, 0));
        }
      }
    }
  }
}


public static class CarouselBench extends LXModel 
{
  public CarouselBench() 
  {
    super(new Fixture());
  }

  private static class Fixture extends LXAbstractFixture 
  {
    Carousel c;
    Bench b;

    private Fixture() 
    {
       c = new Carousel();
       b = new Bench();

       for (LXPoint point : c.points) { 
         addPoint(point); 
       }
       for (LXPoint point : b.points) { 
         addPoint(point); 
       }
    }
  }
}


public static class ModelFusion extends LXModel 
{

  public ModelFusion() 
  {
    super(new Fixture());
  }

  private static class Fixture extends LXAbstractFixture 
  {
    Carousel c;
    Bench b;
    private Fixture() 
    {
      b = new Bench();
      c = new Carousel();
      for (LXPoint pt : b.points)
      {
        addPoint(pt);
      }

      for (LXPoint pt : c.points)
      {
        addPoint(pt);
      } 
    }
  }
}
