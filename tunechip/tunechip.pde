import processing.sound.*;
/*
//further idees
Reverb reverb;
AudioIn in;
Amplitude amp;
*/
ArrayList<Osc> osc = new ArrayList();
final float freqMax = 800;
final float freqMin = 20;
final float freqRoot = 440;
final int numRatios = 6;
final float timeCinit = 10*44000; //in samples
float timeC = timeCinit;
float ratios[] = new float[numRatios];
final float randomness = 0.001;
final int exponent = 4; //how much the correct ratio is emphasist (only even numbers)
tunechip surounding = this; //filename is tunechip.pdm

class Osc extends TriOsc{
  float freq;
  float time=0;
  void setFreq(float freq){
    this.freq = freq;
    this.freq(freq);
    this.time = 0;
  }
  Osc(){
    super(surounding);
    while(!jump(this));
    this.play();
  }
  Osc(float freq){
    super(surounding);
    this.setFreq(freq);
    this.play();
  }
}

float matchFunc(float x){
  if(x>1)
    x=1./x;
  while(x<0.5)
    x*=2;
  int k = 1;
  while(x>ratios[k])
    k++;
  return pow((x-(ratios[k]+ratios[k-1])/2.)*2./(ratios[k-1]-ratios[k]),exponent);
}

void setup(){
  size(400,400);
  /*
  reverb = new Reverb(this);
  in = new AudioIn(this, 0);
  reverb.process(osc.get(0));
  */
  for(int i = 0; i<numRatios-1; i++) //fill ratios[]
    ratios[i] = i/(i+1.); // generates: 1/2, 2/3, 3/4, 5/6, ..., 1
  ratios[numRatios-1] = 1;
  Osc temp = new Osc(440);
  osc.add(temp);
}

void draw(){
  timeC = timeCinit;
    
  String info[] = loadStrings("audio");
  String blank[] = {"b"};
  try{
  if (info!=null){
  if (info[0].equals("+")){
    Osc temp = new Osc();
    osc.add(temp);
    normalize();
    saveStrings("audio",blank);
  }
  if (info[0].equals("-")){
    remove();
  }
  if (info[0].equals("c")){
    timeC = 0.5*44000.;
  }
  }
  }catch(Exception e){};

  background(0);
  int i=0;
  text("freq in Hz",10,40);
  text("freq/440Hz",100,40);
  text("+/- key to add and remove voices",10,20);
  for(Osc x : osc){
    text(x.freq,10,60+20*i);
    text(x.freq/440.,100,60+20*i++);

    if(osc.size()>1)
      jump(x);
  }
  
  
}

void normalize(){
   for(Osc x : osc){
    x.amp(1/((float) osc.size()));
    x.time++;
  } 
}

boolean jump(Osc selected){
   float random = random(0,1+0.01*osc.size()+selected.time/timeC);
   float randomFreq = random(freqMin,freqMax);
    for(Osc x : osc){
      if(x != selected)
        random*=matchFunc(randomFreq/x.freq);
    }
    if(random>1-randomness){
      selected.setFreq(randomFreq);
      return true;
    }
    return false;
}

void remove(){
   if(!osc.isEmpty()){
      Osc toRemove = osc.get((int) random(0,osc.size()));
      toRemove.stop();
      osc.remove(toRemove);
      normalize();
    } 
}

void keyReleased(){
  if(key == '+'){
    Osc temp = new Osc();
    osc.add(temp);
    normalize();
  }
  if(key == '-'){
    remove();
  }
}