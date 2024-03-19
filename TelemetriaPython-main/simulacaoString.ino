int velocidade = 40;
int rpm = 2000;
int freio = 0;
int temperatura = 0;
int box = 0;

int sorteio_box;
int sorteio_temperatura;
int sorteio_freio;


// String: RxxxVxxTxFxBx

void setup() {
  Serial.begin(9600);
}

void loop() {

  velocidade += random(-2, 2);
  if(velocidade > 99)
    velocidade = 99;
  if(velocidade < 0)
    velocidade = 0;
  rpm += random(-100, 100);
  if(rpm > 4000)
    rpm = 4000;
  if(rpm < 0)
    rpm = 0;
  
  sorteio_box = random(1, 100);
  if(sorteio_box > 90){
    if(box)
      box = 0;
    else
      box = 1;
  }

  sorteio_temperatura = random(1, 100);
  if(sorteio_temperatura > 85){
    if(temperatura)
      temperatura = 0;
    else
      temperatura = 1;
  }

  sorteio_freio = random(1, 6);
  if(sorteio_freio > 4){
    if(freio)
      freio = 0;
    else
      freio = 1;
  }

  Serial.println("R" + String(rpm/10) + "V" + String(velocidade) + "T" + String(temperatura) + "F" + String(freio) + "B" + String(box));

    
  delay(950);
}
