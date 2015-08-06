import java.util.*;

public static class Model extends LXModel {
  
  private final static int NUMBER_OF_LAMPPOSTS = 3;
  private final static int LAMPPOST_RADIUS = 17*FEET + 2*INCHES;
  private final static int NUMBER_OF_BENCHES = 3;
  private final static int INNER_BENCH_RADIUS = 8*FEET;
  private final static int OUTER_BENCH_RADIUS = 16*FEET;
  
  public final Carousel carousel; 
  public final CarouselBottom carouselBottom;
  public final List<LampPost> lampPosts;
  public final List<Bench> outerBenches;
  public final List<Bench> innerBenches;
  
  public Model() {
    super(new Fixture());
    Fixture f = (Fixture) this.fixtures.get(0);
    this.carousel = f.carousel;
    this.carouselBottom = f.carouselBottom;
    this.lampPosts = Collections.unmodifiableList(f.lampPosts);
    this.outerBenches = Collections.unmodifiableList(f.outerBenches);
    this.innerBenches = Collections.unmodifiableList(f.innerBenches);
  }
  
  private static class Fixture extends LXAbstractFixture {
    
    private final Carousel carousel;
    private final CarouselBottom carouselBottom;
    private final List<LampPost> lampPosts = new ArrayList<LampPost>();
    private final List<Bench> outerBenches = new ArrayList<Bench>();
    private final List<Bench> innerBenches = new ArrayList<Bench>();
    
    Fixture() {
      addPoints(this.carousel = new Carousel());
      addPoints(this.carouselBottom = new CarouselBottom(0,0));
      for (int i = 0; i < NUMBER_OF_LAMPPOSTS; ++i) {
        float theta = TWO_PI * i / (float) NUMBER_OF_LAMPPOSTS + TWO_PI / 12;
        LampPost lampPost = new LampPost(LAMPPOST_RADIUS * cos(theta), LAMPPOST_RADIUS * sin(theta));
        addPoints(lampPost);
        this.lampPosts.add(lampPost);
      }
      for (int i = 0; i < NUMBER_OF_BENCHES; ++i) {
        Bench inner = new Bench(new LXTransform().rotateY(TWO_PI * i / (float)NUMBER_OF_BENCHES).translate(0, 0, -INNER_BENCH_RADIUS));
        addPoints(inner);
        this.innerBenches.add(inner);
        
        Bench outer = new Bench(new LXTransform().rotateY(TWO_PI * (i+.5) / (float)NUMBER_OF_BENCHES).translate(0, 0, -OUTER_BENCH_RADIUS));
        addPoints(outer);
        this.outerBenches.add(outer);
      }
    }
  }
}

private static class Carousel extends LXModel {
  
  private static final int CAROUSEL_HEIGHT = 9*FEET + 7*INCHES;
  private static final int NUMBER_OF_BARS = 7;
  
  public final List<Bar> bars;
  
  Carousel() {
    super(new Fixture());
    Fixture f = (Fixture) this.fixtures.get(0);
    this.bars = Collections.unmodifiableList(f.bars);
  } 
  
  private static class Fixture extends LXAbstractFixture {
    
    private List<Bar> bars = new ArrayList<Bar>();
    
    Fixture() {
      LXTransform transform1 = new LXTransform();
      LXTransform transform2 = new LXTransform();
      transform1.translate(0, CAROUSEL_HEIGHT, 0);
      transform2.translate(0, CAROUSEL_HEIGHT, 0);
      for (int i = 0; i < NUMBER_OF_BARS; ++i) {
        Bar bar1 = new Bar(transform1);
        Bar bar2 = new Bar(transform2);
        addPoints(bar1);
        addPoints(bar2);
        this.bars.add(bar1);
        this.bars.add(bar2);
        transform1.rotateY(TWO_PI / NUMBER_OF_BARS);
        transform2.rotateY(TWO_PI / (NUMBER_OF_BARS - 0.01));
      }
    }
  }
  
  private static class Bar extends LXModel {
  
    private static final int NUMBER_OF_LEDS_PER_LEG = 30;
    private static final int INNER_RADIUS_OF_HUB = 14 * INCHES;
    private static final int BAR_LENGTH = (15*FEET + 7*INCHES)/2 - INNER_RADIUS_OF_HUB;
  
    public Bar(LXTransform transform) {
      super(new Fixture(transform));
    }
    
    private static class Fixture extends LXAbstractFixture {
      Fixture(LXTransform transform) {
        final float spacing = BAR_LENGTH / NUMBER_OF_LEDS_PER_LEG;
        transform.push();
        transform.translate(INNER_RADIUS_OF_HUB, 0, 0);
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
  private static int NBARS = 7;
  private static int NLEDS = 19;
  
  public LampPost(float x, float z) {
    super(new Fixture(x, z));
  }
  
  private static class Fixture extends LXAbstractFixture {

    private List<Bar> bars = new ArrayList<Bar>();

    Fixture(float x, float z) { 
      LXTransform transform = new LXTransform(); 
      transform.translate(x, 0, z); 
      for (int i = 0; i < NBARS; ++i) {
        Bar bar = new Bar(transform);
        addPoints(bar);
        this.bars.add(bar);
        // transform.translate(0, 0, 0);
        transform.rotateY(TWO_PI / NBARS);
      }
    }
  }

  private static class Bar extends LXModel {
  
    private static final int BAR_HEIGHT = 7 * FEET;
    private static final int BOTTOM_OF_LIGHTS = 2 * FEET;
    private static final int NUMBER_OF_LEDS_PER_LEG = 19;
  
    public Bar(LXTransform transform) {
      super(new Fixture(transform));
    }
    
    private static class Fixture extends LXAbstractFixture {
      Fixture(LXTransform transform) {
        final float spacing = BAR_HEIGHT/ NUMBER_OF_LEDS_PER_LEG;
        transform.push();
        transform.translate(2, BOTTOM_OF_LIGHTS, 0);
        for (int i = 0; i < NUMBER_OF_LEDS_PER_LEG; i++) {
          addPoint(new LXPoint(transform));
          transform.translate(0, spacing, 0);
        }
        transform.pop();
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
        transform.translate(0, 6, 0); 
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

private static class CarouselBottom extends LXModel {
  private static int NBARS = 6;
  private static int NLEDS = 19;
  
  public CarouselBottom(float x, float z) {
    super(new Fixture(x, z));
  }
  
  private static class Fixture extends LXAbstractFixture {

    private List<Bar> bars = new ArrayList<Bar>();

    Fixture(float x, float z) { 
      LXTransform transform = new LXTransform(); 
      transform.translate(x, 0, z); 
      for (int i = 0; i < NBARS; ++i) {
        Bar bar = new Bar(transform);
        addPoints(bar);
        this.bars.add(bar);
        // transform.translate(0, 0, 0);
        transform.rotateY(TWO_PI / NBARS);
      }
    }
  }

  private static class Bar extends LXModel {
  
    private static final int BAR_HEIGHT = 9*FEET + 7*INCHES;
    private static final int NUMBER_OF_LEDS_PER_LEG = 19;
  
    public Bar(LXTransform transform) {
      super(new Fixture(transform));
    }
    
    private static class Fixture extends LXAbstractFixture {
      Fixture(LXTransform transform) {
        final float spacing = BAR_HEIGHT/ NUMBER_OF_LEDS_PER_LEG;
        transform.push();
        transform.translate(3, 0, 0);
        for (int i = 0; i < NUMBER_OF_LEDS_PER_LEG; i++) {
          addPoint(new LXPoint(transform));
          transform.translate(0, spacing, 0);
        }
        transform.pop();
      }
    }
  }
}
