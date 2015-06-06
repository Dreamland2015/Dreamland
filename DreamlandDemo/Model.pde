

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
    private static final int NUMBER_OF_LEDS_PER_LEG = 10;

    public BarFixture() {
      for (int i = 0; i < NUMBER_OF_LEDS_PER_LEG; i++)
        addPoint(new Point((i + 0.5) / NUMBER_OF_LEDS_PER_LEG * BAR_LENGTH, 0, 0));
    }
  }

  private static class CarouselFixture extends Component {
    private static final int HEIGHT_OF_CAROUSEL = -10 * FEET;

    public CarouselFixture(int nbars) {
      BarFixture prototype = new BarFixture();
      for (int i = 0; i < nbars; i++)
        addComponent(prototype.translate(0, 0, HEIGHT_OF_CAROUSEL).rotate(2 * PI * i / nbars));
    }
  }

  private static class WingFixture extends Component {
    private static float BENCH_LENGTH = 5;
    private static float BENCH_ANGLE = 120;
    private static float WX = BENCH_LENGTH * cos((BENCH_ANGLE - 90) * PI / 180);
    private static float WY = BENCH_LENGTH * sin((BENCH_ANGLE - 90) * PI / 180);
    private static int NLEDS = 10;

    public WingFixture() {
      for (int i = NLEDS; i > 0; i--) {
        float x = WX * ((i + 0.5f) / NLEDS) * FEET;
        float y = WY * ((i + 0.5f) / NLEDS) * FEET;
        addPoint(new Point(x, y, 0));
      }
      for (int i = 0; i < NLEDS; i++) {
        float x = WX * ((i + 0.5f) / NLEDS) * FEET;
        float y = WY * ((i + 0.5f) / NLEDS) * FEET;
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

  private static class LampPostFixture extends Component{
    private static float HEIGHT_OF_POST = -10 * FEET;
    private static int NLEDS = 10;
    
    public LampPostFixture(){
      for (int i = 0; i < NLEDS; i++)
        addPoint( new Point(0, 0, (i + 0.5f) / NLEDS * HEIGHT_OF_POST));
      
    }
  }

  private static class WorldFixture extends Component {
    public WorldFixture() {
      // carousel
      addComponent(new CarouselFixture(9));
      
      BenchFixture bench = new BenchFixture();
      // inner benches
      for (int i = 0; i < 3; i++) {
       addComponent(bench.translate(0, -10 * FEET, 0).rotate(2 * PI * i / 3f));
      }
      // outer benches
      for (int i = 0; i < 3; i++) {
        addComponent(bench.translate(0, -15 * FEET, 0).rotate(2 * PI * (i + 0.5) / 3f));
      }

      LampPostFixture post = new LampPostFixture();
      // lamp posts
      for (int i = 0; i <3; i++) {
        addComponent(post.translate(0, -20 * FEET, 0).rotate(2 * PI * i / 3f));
      }
    }
  }
}
