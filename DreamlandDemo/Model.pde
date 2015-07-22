import java.util.*;

public static class Model extends LXModel {
  
  private final static int NUMBER_OF_LAMPPOSTS = 3;
  private final static int LAMPPOST_RADIUS = 20*FEET;
  private final static int NUMBER_OF_BENCHES = 3;
  private final static int INNER_BENCH_RADIUS = 10*FEET;
  private final static int OUTER_BENCH_RADIUS = 15*FEET;
  
  public final Carousel carousel; 
  public final List<LampPost> lampPosts;
  public final List<Bench> benches;
  
  public Model() {
    super(new Fixture());
    Fixture f = (Fixture) this.fixtures.get(0);
    this.carousel = f.carousel;
    this.lampPosts = Collections.unmodifiableList(f.lampPosts);
    this.benches = Collections.unmodifiableList(f.benches);
  }
  
  private static class Fixture extends LXAbstractFixture {
    
    private final Carousel carousel;
    private final List<LampPost> lampPosts = new ArrayList<LampPost>();
    private final List<Bench> benches = new ArrayList<Bench>();
    
    Fixture() {
      addPoints(this.carousel = new Carousel());
      for (int i = 0; i < NUMBER_OF_LAMPPOSTS; ++i) {
        float theta = TWO_PI * i / (float) NUMBER_OF_LAMPPOSTS;
        LampPost lampPost = new LampPost(LAMPPOST_RADIUS * cos(theta), LAMPPOST_RADIUS * sin(theta));
        addPoints(lampPost);
        this.lampPosts.add(lampPost);
      }
      for (int i = 0; i < NUMBER_OF_BENCHES; ++i) {
        Bench inner = new Bench(new LXTransform().rotateY(TWO_PI * i / (float)NUMBER_OF_BENCHES).translate(0, 0, -INNER_BENCH_RADIUS));
        addPoints(inner);
        this.benches.add(inner);
        
        Bench outer = new Bench(new LXTransform().rotateY(TWO_PI * (i+.5) / (float)NUMBER_OF_BENCHES).translate(0, 0, -OUTER_BENCH_RADIUS));
        addPoints(outer);
        this.benches.add(outer);
      }
    }
  }
}

private static class Carousel extends LXModel {
  
  private static final int CAROUSEL_HEIGHT = 10 * FEET;
  private static final int NUMBER_OF_BARS = 9;
  
  public final List<Bar> bars;
  
  Carousel() {
    super(new Fixture());
    Fixture f = (Fixture) this.fixtures.get(0);
    this.bars = Collections.unmodifiableList(f.bars);
  } 
  
  private static class Fixture extends LXAbstractFixture {
    
    private List<Bar> bars = new ArrayList<Bar>();
    
    Fixture() {
      LXTransform transform = new LXTransform();
      transform.translate(0, CAROUSEL_HEIGHT, 0);
      for (int i = 0; i < NUMBER_OF_BARS; ++i) {
        Bar bar = new Bar(transform);
        addPoints(bar);
        this.bars.add(bar);
        transform.rotateY(TWO_PI / NUMBER_OF_BARS);
      }
    }
  }
  
  private static class Bar extends LXModel {
  
    private static final int BAR_LENGTH = 10 * FEET;
    private static final int NUMBER_OF_LEDS_PER_LEG = 10;
  
    public Bar(LXTransform transform) {
      super(new Fixture(transform));
    }
    
    private static class Fixture extends LXAbstractFixture {
      Fixture(LXTransform transform) {
        final float spacing = BAR_LENGTH / NUMBER_OF_LEDS_PER_LEG;
        transform.push();
        transform.translate(spacing/2, 0, 0);
        for (int i = 0; i < NUMBER_OF_LEDS_PER_LEG; i++) {
          addPoint(new LXPoint(transform));
          transform.translate(spacing, 0, 0);
        }
        transform.pop();
      }
    }
  }
}

private static class LampPost extends LXModel {
  private static float HEIGHT_OF_POST = 10 * FEET;
  private static int NLEDS = 10;
  
  public LampPost(float x, float z) {
    super(new Fixture(x, z));
  }
  
  private static class Fixture extends LXAbstractFixture {
    Fixture(float x, float z) {    
      for (int i = 0; i < NLEDS; i++) {
        addPoint(new LXPoint(x, (i + 0.5f) / NLEDS * HEIGHT_OF_POST, z));
      }
    }
  }
}

private static class Bench extends LXModel {

  private final static float BENCH_LENGTH = 5;
  private final static float BENCH_ANGLE = 120;
  private final static float WX = BENCH_LENGTH * cos((BENCH_ANGLE - 90) * PI / 180);
  private final static float WZ = BENCH_LENGTH * sin((BENCH_ANGLE - 90) * PI / 180);
  private final static int NLEDS = 10;

  private final static int NUMBER_OF_WINGS = 3; 

  Bench(LXTransform transform) {
    super(new Fixture(transform));
  }
  
  private static class Fixture extends LXAbstractFixture {
    Fixture(LXTransform transform) {
      for (int i = 0; i < NUMBER_OF_WINGS; i++) {
        transform.translate(0, 1*FEET, 0); 
        addPoints(new Wing(transform));
      }
    }
  }
  
  private static class Wing extends LXModel {
    
    Wing(LXTransform transform) {
      super(new Fixture(transform));
    }
    
    private static class Fixture extends LXAbstractFixture {
      Fixture(LXTransform transform) {
        final float xStep = WX * FEET / NLEDS;
        final float zStep = WZ * FEET / NLEDS;
        
        transform.push();
        transform.translate(xStep*(NLEDS-0.5), 0, zStep*(NLEDS-0.5));
        for (int i = NLEDS; i > 0; i--) {
          addPoint(new LXPoint(transform));
          transform.translate(-xStep, 0, -zStep);
        }
        transform.pop();
        
        transform.push();
        transform.translate(-0.5*xStep, 0, 0.5*zStep);
        for (int i = 0; i < NLEDS; i++) {
          addPoint(new LXPoint(transform));
          transform.translate(-xStep, 0, zStep);
        }
        transform.pop();
      }
    }
  }
}

