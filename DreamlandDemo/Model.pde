// Overall dreamland dimensions
private static final int LAMPPOST_RADIUS = 17*FEET + 2*INCHES;
private static final int BENCH_LED_HEIGHT = 18*INCHES;                    // Height of leds in benches
private static final int INNER_BENCH_RADIUS = 8*FEET - 27*INCHES;
private static final int OUTER_BENCH_RADIUS = 17*FEET + 6*INCHES;

// Bench parameters
private static final float ANGLE = 150;                  // Large angle of the benches
private static final int DROWS_INNER = 5 * INCHES;       // Distance between rows
private static final int DROWS_OUTER = 7 * INCHES;       // Distance between rows
private static final int BENCH_LED_SPACING = 3 * INCHES;       // Spacing of the LED on benches
private static final int NUMBENCHES = 3;                 // Number of benches per ring
private static final int NUMBER_OF_BENCHES = 3;
private static final int[] NLEDS_INNER = {5, 6};         // Number of LEDs per row on inner benches
private static final int[] NLEDS_OUTER = {16, 17, 18};   // Number of LEDs per row on outer benches

// Lamp post parameters
private static final int NUMBER_OF_LAMPPOSTS = 3;
private static final int BOTTOM_OF_LP_LED = 54;
private static final float LP_BAR_HEIGHT = 45.5;
private static final float LP_BAR_RADIUS = 2.5;

// KScope parameters
private static final int KSCOPE_RADIUS = 30 * FEET;
private static final int KSCOPE_NLED = 12;


public static class Model extends LXModel {  
  public final Carousel carousel; 
  public final CarouselBottom carouselBottom;
  public final List<LampPost> lampPosts;
  public final List<Bench> outerBenches;
  public final List<Bench> innerBenches;
  public final List<Kaleidoscope> kaleidoscopes;
  
  public Model() {
    super(new Fixture());
    Fixture f = (Fixture) this.fixtures.get(0);
    this.carousel = f.carousel;
    this.carouselBottom = f.carouselBottom;
    this.outerBenches = Collections.unmodifiableList(f.outerBenches);
    this.innerBenches = Collections.unmodifiableList(f.innerBenches);
    this.lampPosts = Collections.unmodifiableList(f.lampPosts);
    this.kaleidoscopes = Collections.unmodifiableList(f.kaleidoscopes);
  }
  
  private static class Fixture extends LXAbstractFixture {
    
    private final Carousel carousel;
    private final CarouselBottom carouselBottom;
    private final List<LampPost> lampPosts = new ArrayList<LampPost>();
    private final List<Bench> outerBenches = new ArrayList<Bench>();
    private final List<Bench> innerBenches = new ArrayList<Bench>();
    private final List<Kaleidoscope> kaleidoscopes = new ArrayList<Kaleidoscope>();
    
    Fixture() {
      // Build carousel top
      addPoints(this.carousel = new Carousel());

      // Build carousel bottom
      addPoints(this.carouselBottom = new CarouselBottom());
      
      // Build inner benches
      for (int i = 0; i < NUMBER_OF_BENCHES; i++)
      {
        LXTransform transform = new LXTransform();
        transform.push();
        transform.rotateY(radians(120) * i);
        transform.translate(INNER_BENCH_RADIUS, 0, 0);
        Bench bench = new Bench(NLEDS_INNER ,DROWS_INNER, transform);
        addPoints(bench);
        this.innerBenches.add(bench);
      }

      // Build lamp posts
      for (int i = 0; i < NUMBER_OF_LAMPPOSTS; ++i) {
        LXTransform transform = new LXTransform();
        float theta = radians(120) * i;
        transform.push();
        transform.rotateY(radians(120) * i);
        transform.translate(LAMPPOST_RADIUS, 0, 0);
        LampPost lampPost = new LampPost(transform);
        addPoints(lampPost);
        this.lampPosts.add(lampPost);
      }

      // Build outer benches
      for (int i = 0; i < NUMBER_OF_BENCHES; i++)
      {
        LXTransform transform = new LXTransform();
        transform.push();
        transform.rotateY((radians(120) * i) + radians(60));
        transform.translate(OUTER_BENCH_RADIUS, 0, 0);
        Bench bench = new Bench(NLEDS_OUTER , DROWS_OUTER,transform);
        addPoints(bench);
        this.outerBenches.add(bench);
      }


      // Build Kaleidoscopes
      for (int i = 0; i <3; i++)
      {
        LXTransform transform = new LXTransform();
        transform.push();
        transform.rotateY((radians(120) * i) + radians(60));
        transform.translate(KSCOPE_RADIUS, 0, 0);
        Kaleidoscope kaleidoscope = new Kaleidoscope(KSCOPE_NLED, transform);
        addPoints(kaleidoscope);
        this.kaleidoscopes.add(kaleidoscope);
      }
    }
  }
}

private static class Carousel extends LXModel {
  
  private static final int CAROUSEL_HEIGHT = 9*FEET + 7*INCHES;
  private static final int NUMBER_OF_BARS = 9;
  private static final int NUMBER_OF_ARMS = 9;
  
  public final List<Bar> bars;
  public final List<Arm> arms;
  
  Carousel() {
    super(new Fixture());
    Fixture f = (Fixture) this.fixtures.get(0);
    this.bars = Collections.unmodifiableList(f.bars);
    this.arms = Collections.unmodifiableList(f.arms);
  } 
  
  private static class Fixture extends LXAbstractFixture {
    
    private List<Bar> bars = new ArrayList<Bar>();
    private List<Arm> arms = new ArrayList<Arm>();
    
    Fixture() 
    {
      for(int i = 0; i < NUMBER_OF_ARMS; i++)
      {
        LXTransform transform = new LXTransform();
        transform.push();
        transform.translate(0, CAROUSEL_HEIGHT, 0);
        transform.rotateY(TWO_PI / NUMBER_OF_ARMS * i);
        Arm arm = new Arm(transform);
        transform.pop();
        addPoints(arm);
        this.arms.add(arm);
        for(Bar b : arm.bars)
        {
          this.bars.add(b);
        }
      }
    }
  }

  private static class Arm extends LXModel
  {
    private List<Bar> bars;

    public Arm(LXTransform transform)
    {
      super(new Fixture(transform));
      Fixture f = (Fixture) this.fixtures.get(0);
      this.bars = Collections.unmodifiableList(f.bars);
    }

    private static class Fixture extends LXAbstractFixture
    {
      private List<Bar> bars = new ArrayList<Bar>();

      Fixture(LXTransform transform)
      {
        transform.push();
        transform.translate(0,0,-1);
        Bar bar = new Bar(transform);
        this.bars.add(bar);
        addPoints(bar);
        transform.pop();

        transform.push();
        transform.translate(0,0,1);
        Bar bar2 = new Bar(transform);
        this.bars.add(bar2);
        addPoints(bar2);
        transform.pop();
      }
    }
  }
  
  private static class Bar extends LXModel {
  
    private static final int NUMBER_OF_LEDS_PER_LEG = 34;
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

  public final List<Bar> bars;
  // public final List<LXPoint> rings;
  
  public LampPost(LXTransform transform) {
    super(new Fixture(transform));
    Fixture f = (Fixture) this.fixtures.get(0);
    this.bars = Collections.unmodifiableList(f.bars);
    // this.rings = Collections.unmodifiableList(f.rings);
  }
  
  private static class Fixture extends LXAbstractFixture {

    private List<Bar> bars = new ArrayList<Bar>();

    Fixture(LXTransform transform) { 
      for (int i = 0; i < NBARS; ++i) 
      {
        transform.push(); 
        transform.rotateY(TWO_PI / NBARS * i);
        Bar bar = new Bar(transform);
        addPoints(bar);
        this.bars.add(bar);
        transform.pop();
      }
    }
  }

  // private static class Ring extends LXModel
  // {
  //   public Ring(List<Bar> bars)
  //   {
  //     super(new Fixture());
  //   }
    
  // }

  private static class Bar extends LXModel {
  
    public Bar(LXTransform transform) {
      super(new Fixture(transform));
    }
    
    private static class Fixture extends LXAbstractFixture {
      Fixture(LXTransform transform) {
        final float spacing = LP_BAR_HEIGHT/ NLEDS;
        transform.push();
        transform.translate(-LP_BAR_RADIUS, BOTTOM_OF_LP_LED, 0);
        for (int i = 0; i < NLEDS; i++) {
          addPoint(new LXPoint(transform));
          transform.translate(0, spacing, 0);
        }
        transform.pop();
      }
    }
  }
}

private static class Bench extends LXModel {
  
  public final List<Wing> wings;
  public final List<Bar> bars;
  
  Bench(int[] NLEDS, int DROW, LXTransform transform) {
    super(new Fixture(NLEDS, DROW, transform));
    Fixture f = (Fixture) this.fixtures.get(0);
    this.wings = Collections.unmodifiableList(f.wings);
    this.bars = Collections.unmodifiableList(f.bars);
  } 
  
  private static class Fixture extends LXAbstractFixture {
    
    private List<Wing> wings = new ArrayList<Wing>();
    private List<Bar> bars = new ArrayList<Bar>();
    private int counter = 0;
    
    Fixture(int[] NLEDS, int DROW, LXTransform transform) 
    {
      int NROWS = NLEDS.length;
      for (int i = 0; i < NROWS; i ++)
      {
        transform.translate(DROW ,0 , 0);
        transform.push();
        transform.rotateY(radians(ANGLE / 2));
        Wing wing = new Wing(NLEDS[i], transform);
        this.wings.add(wing);
        addPoints(wing); 
        transform.pop();
        for(Bar b : wing.bars)
        {
          this.bars.add(b);
        }
      }
    }
  }

  private static class Wing extends LXModel
  {
    private List<Bar> bars;

    public Wing(int numLeds, LXTransform transform)
    {
      super(new Fixture(numLeds, transform));
      Fixture f = (Fixture) this.fixtures.get(0);
      this.bars = Collections.unmodifiableList(f.bars);
    }

    private static class Fixture extends LXAbstractFixture
    {
      private List<Bar> bars = new ArrayList<Bar>(); 

      Fixture(int numLeds, LXTransform transform)
      {
        transform.push();
        transform.translate(- numLeds * BENCH_LED_SPACING + BENCH_LED_SPACING ,0,0);
        Bar bar = new Bar(numLeds, transform);
        // Bar bar = new Bar(numLeds - 1, transform);
        this.bars.add(bar);
        addPoints(bar);
        transform.pop();

        transform.push();
        transform.translate(0 ,0, 0);
        transform.rotateY(radians(180 - ANGLE));
        Bar bar2 = new Bar(numLeds, transform);
        this.bars.add(bar2);
        addPoints(bar2);
        transform.pop();

      }
    }
  }
  
  private static class Bar extends LXModel {
  
  
    public Bar(int numLeds, LXTransform transform) {
      super(new Fixture(numLeds, transform));
    }
    
    private static class Fixture extends LXAbstractFixture {
      Fixture(int numLeds, LXTransform transform) {
        transform.translate(0, BENCH_LED_HEIGHT, 0);
        transform.push();
        for (int i = 0; i < numLeds; i++) {
          addPoint(new LXPoint(transform));
          transform.translate(BENCH_LED_SPACING, 0, 0);
        }
        transform.pop();
      }
    }
  }
}

private static class Kaleidoscope extends LXModel {
  
  
  Kaleidoscope(int NLEDS, LXTransform transform) {
    super(new Fixture(NLEDS, transform));
  } 
  
  private static class Fixture extends LXAbstractFixture {
    
    private int counter = 0;
    
    Fixture(int NLEDS, LXTransform transform) 
    {
      for (int i = 0; i < 1; i ++)
      {
        transform.push();
        transform.rotateY(radians(45));
        Wing wing = new Wing(NLEDS, transform);
        addPoints(wing); 
        transform.pop();
      }
    }
  }

  private static class Wing extends LXModel
  {

    public Wing(int numLeds, LXTransform transform)
    {
      super(new Fixture(numLeds, transform));
    }

    private static class Fixture extends LXAbstractFixture
    {
      private List<Bar> bars = new ArrayList<Bar>();  
      Fixture(int numLeds, LXTransform transform)
      {
        transform.push();
        transform.translate(- numLeds * BENCH_LED_SPACING + BENCH_LED_SPACING ,0,0);
        Bar bar = new Bar(numLeds - 1, transform);
        this.bars.add(bar);
        addPoints(bar);
        transform.pop();

        transform.push();
        transform.translate(0 ,0, 0);
        transform.rotateY(radians(90));
        Bar bar2 = new Bar(numLeds, transform);
        this.bars.add(bar2);
        addPoints(bar2);
        transform.pop();

      }
    }
  }
  
  private static class Bar extends LXModel {
  
  
    public Bar(int numLeds, LXTransform transform) {
      super(new Fixture(numLeds, transform));
    }
    
    private static class Fixture extends LXAbstractFixture {
      Fixture(int numLeds, LXTransform transform) {
        transform.translate(0, BENCH_LED_HEIGHT, 0);
        transform.push();
        for (int i = 0; i < numLeds; i++) {
          addPoint(new LXPoint(transform));
          transform.translate(BENCH_LED_SPACING, 0, 0);
        }
        transform.pop();
      }
    }
  }
}

private static class CarouselBottom extends LXModel {
  private static int NBARS = 6;
  private static int NLEDS_BOTTOM = 30;
  private static int NLEDS_TOP = 6;
  private static float LED_SPACING = 2.5;
  private static int CAROUSEL_RADIUS = 4;
  private static float CAROUSEL_EXT_HEIGHT = 82.5;
  private static float CAROUSEL_GROUND_OFFSET = 6.5 * INCHES;
  
  public CarouselBottom() {
    super(new Fixture());
  }
  
  private static class Fixture extends LXAbstractFixture {

    private List<Bar> bars = new ArrayList<Bar>();

    Fixture() { 
      // Build upper section of the carousel bottom
      LXTransform transform = new LXTransform(); 
      for (int i = 0; i < NBARS; ++i)
      {
        transform.push(); 
        transform.rotateY(TWO_PI / NBARS * i);
        BarTop barTop = new BarTop(NLEDS_TOP, transform);
        addPoints(barTop);
        transform.pop();
      }
      // Build lower section of the carousel bottom
      for (int i = 0; i < NBARS; ++i) {
        transform.push(); 
        transform.rotateY(TWO_PI / NBARS * i);
        BarBottom barBottom = new BarBottom(NLEDS_BOTTOM, transform);
        addPoints(barBottom);
        transform.pop();
      }

    }
  }

  private static class BarBottom extends LXModel
  {
    public BarBottom(int numLed, LXTransform transform)
    {
      super(new Fixture(numLed, transform));
    }

    private static class Fixture extends LXAbstractFixture
    {
      Fixture(int numLed, LXTransform transform)
      {
        transform.push();
        transform.translate(CAROUSEL_RADIUS, CAROUSEL_GROUND_OFFSET, 0);
        Bar bar = new Bar(numLed, transform);
        addPoints(bar);
        transform.pop();
      }
    }
  }

  private static class BarTop extends LXModel
  {
    public BarTop(int numLed, LXTransform transform)
    {
      super(new Fixture(numLed, transform));
    }

    private static class Fixture extends LXAbstractFixture
    {
      Fixture(int numLed, LXTransform transform)
      {
        transform.push();
        // transform.rotateZ(PI);
        // transform.translate(CAROUSEL_RADIUS, CAROUSEL_GROUND_OFFSET, 0);
        transform.translate(CAROUSEL_RADIUS, CAROUSEL_GROUND_OFFSET + CAROUSEL_EXT_HEIGHT , 0);
        Bar bar = new Bar(numLed, transform);
        addPoints(bar);
        transform.pop();
      }
    }
  }

  private static class Bar extends LXModel {
  
    public Bar(int numLed, LXTransform transform) {
      super(new Fixture(numLed, transform));
    }
    
    private static class Fixture extends LXAbstractFixture {
      Fixture(int numLed, LXTransform transform) {
        transform.push();
        for (int i = 0; i < numLed; i++) {
          addPoint(new LXPoint(transform));
          transform.translate(0, LED_SPACING, 0);
        }
        transform.pop();
      }
    }
  }
}