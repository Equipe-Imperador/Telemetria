#define BAUDRATE 115200

bool box = false;


void setup(){
  Serial.begin(BAUDRATE);

  Serial.println("Iniciando Teste");
}

void loop(){

  delay(1000);
  
  String mensagem = "";

  mensagem += "V";

  mensagem += "25";

  mensagem += "R";

  mensagem += "200";

  mensagem += "F1";

  mensagem += "T+73.1";

  mensagem += "B12.5";

  mensagem += "\n";

  Serial.print(mensagem);

  if(Serial.available()){
    String comando = Serial.readString();
    Serial.print("Mensagem recebida: ");
    Serial.println(comando);
    if(comando == "BOX"){
      if(box){
        Serial.println("BOX OFF");
        box = false;
      }else{
        Serial.println("BOX ON");
        box = true;
      }
    }
  }

}