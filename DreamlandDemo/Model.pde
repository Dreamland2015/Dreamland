

public static class Model extends LXModel 
{
  public Model () 
  {
    super(new WorldFixture().toLxPoints());
  }

  private static class Point {
    private final float x, y, z;

    public Point(float x, float y, float z) {
      this.x = x;
      this.y = y;
      this.z = z;
    }

    public Point rotate(float theta) {
      return new Point(
        cos(theta) * x - sin(theta) * y,
        sin(theta) * x + cos(theta) * y,
        z
        );
    }

    public Point translate(float x, float y, float z) {
      return new Point(this.x + x, this.y + y, this.z + z);
    }

    public LXPoint toLxPoint() {
      return new LXPoint(x, y, z);
    }
  }

  private static class Component extends java.util.ArrayList/*<Point>*/ {

    public Component rotate(float theta) {
      Component out = new Component();
      for (int i = 0; i < size(); i++)
        out.addPoint(((Point)get(i)).rotate(theta));
      return out;
    }

    public Component translate(float x, float y, float z) {
      Component out = new Component();
      for (int i = 0; i < size(); i++)
        out.addPoint(((Point)get(i)).translate(x, y, z));
      return out;
    }

    protected void addPoint(Point p) {
      add(p);
    }

    protected void addComponent(Component c) {
      addAll(c);
    }

    public List/*<LXPoint>*/ toLxPoints() {
      List/*<LXPoint>*/ out = new ArrayList/*<LXPoint>*/();
      for (int i = 0; i < size(); i++)
        out.add(((Point)get(i)).toLxPoint());
      return out;
    }
  }

  private static class BarFixture extends Component {
    private static final int BAR_LENGTH = 10 * FEET;
    private static final int NUMBER_OF_LEDS_PER_LEG = 16;

    public BarFixture() {
      for (int i = 0; i < NUMBER_OF_LEDS_PER_LEG; i++)
        addPoint(new Point((i + 0.5) / NUMBER_OF_LEDS_PER_LEG * BAR_LENGTH, 0, 0));
    }
  }

  private static class CarouselFixture extends Component {
    public CarouselFixture(int nbars) {
      BarFixture prototype = new BarFixture();
      for (int i = 0; i < nbars; i++)
        addComponent(prototype.rotate(2*PI*i / nbars));
      // addPoint(new LXPoint(i, i, 0));
    }
  }

  private static class WingFixture extends Component {
    private static int WX = 5;
    private static int WY = 2;
    private static int NLEDS = 20;
    public WingFixture() {
      for (int i = 0; i < NLEDS; i++) {
        float x = WX * ((i + 0.5f) / NLEDS) * FEET;
        float y = WY * ((i + 0.5f) / NLEDS) * FEET;
        addPoint(new Point(x, y, 0));
        addPoint(new Point(-x, y, 0));
      }
    }
  }

  private static class BenchFixture extends Component {
    public BenchFixture() {
      WingFixture prototype = new WingFixture();
      for (int i = 0; i < 3; i++)
        addComponent(prototype.translate(0, 0, (i + 1) * FEET));
    }
  }

  private static class WorldFixture extends Component {
    public WorldFixture() {
      // carousel
      addComponent(new CarouselFixture(9));
      
      BenchFixture bench = new BenchFixture();
      // inner benches
      for (int i = 0; i < 3; i++) {
       addComponent(bench.translate(0, -15 * FEET, 0).rotate(2 * PI * i / 3f));
      }
      // outer benches
      for (int i = 0; i < 3; i++) {
        addComponent(bench.translate(0, -20 * FEET, 0).rotate(2 * PI * (i + 0.5) / 3f));
      }

    }
  }

  // private static class Fixture extends LXAbstractFixture 
  // {

  //   private Fixture() 
  //   {
  //   // Here's the core loop where we generate the positions
  //   // of the points in our model
  //   // for (int n = 0; n < NUMBER_OF_LEGS; ++n)
  //     for (int ledPoint = 0; ledPoint < NUMBER_OF_LEDS_PER_LEG; ++ledPoint) 
  //     {
  //       int ledLocation = ledPoint * FEET + OFFSET;
  //       // for (int ledPoint = 0; ledPoint < NUMBER_OF_LEDS_PER_LEG; ++ledPoint) 
  //       for (int n = 0; n < NUMBER_OF_LEGS; ++n)
  //       {
  //         // int ledLocation = ledPoint * FEET + OFFSET;
  //         float rx = ledLocation * cos(2 * PI * n / NUMBER_OF_LEGS);
  //         float ry = ledLocation * sin(2 * PI * n / NUMBER_OF_LEGS);
  //         // Add point to the fixtuure
  //         addPoint(new LXPoint(rx,ry, 5));
  //       }
  //     }
  //   }
  // }
}


// public static class Carousel extends LXModel 
// {
//   public Carousel() 
//   {
//     super(new Fixture());
//   }

//   private static class Fixture extends LXAbstractFixture 
//   {
//     private static final int OFFSET = 2 * FEET;
//     private static final int NUMBER_OF_LEGS = 9;
//     private static final int NUMBER_OF_LEDS_PER_LEG = 16;

//     private Fixture() 
//     {
//     // Here's the core loop where we generate the positions
//     // of the points in our model
//     // for (int n = 0; n < NUMBER_OF_LEGS; ++n)
//       for (int ledPoint = 0; ledPoint < NUMBER_OF_LEDS_PER_LEG; ++ledPoint) 
//       {
//         int ledLocation = ledPoint * FEET + OFFSET;
//         // for (int ledPoint = 0; ledPoint < NUMBER_OF_LEDS_PER_LEG; ++ledPoint) 
//         for (int n = 0; n < NUMBER_OF_LEGS; ++n)
//         {
//           // int ledLocation = ledPoint * FEET + OFFSET;
//           float rx = ledLocation * cos(2 * PI * n / NUMBER_OF_LEGS);
//           float ry = ledLocation * sin(2 * PI * n / NUMBER_OF_LEGS);
//           // Add point to the fixtuure
//           addPoint(new LXPoint(rx, ry, 0));
//         }
//       }
//     }
//   }
// }


// public static class CarouselBench extends LXModel 
// {
//   public CarouselBench() 
//   {
//     super(new Fixture());
//   }

//   private static class Fixture extends LXAbstractFixture 
//   {
//     Carousel c;
//     Bench b;

//     private Fixture() 
//     {
//        c = new Carousel();
//        b = new Bench();

//        for (LXPoint point : c.points) { 
//          addPoint(point); 
//        }
//        for (LXPoint point : b.points) { 
//          addPoint(point); 
//        }
//     }
//   }
// }


// public static class ModelFusion extends LXModel 
// {

//   public ModelFusion() 
//   {
//     super(new Fixture());
//   }

//   private static class Fixture extends LXAbstractFixture 
//   {
//     Carousel c;
//     Bench b;
//     private Fixture() 
//     {
//       b = new Bench();
//       c = new Carousel();
//       for (LXPoint pt : b.points)
//       {
//         addPoint(pt);
//       }

//       for (LXPoint pt : c.points)
//       {
//         addPoint(pt);
//       } 
//     }
//   }
// }
