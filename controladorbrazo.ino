//-----------------------------------------------------------
//incluir las librerias a usar
//-----------------------------------------------------------
#include <Servo.h>
#include <Stepper.h>
#include <Math.h>

//-----------------------------------------------------------
//estas son las variables a usar para mover el brazo
//-----------------------------------------------------------
String arraycodigos[] = 
    {"8A", "8B", "8C", "8D", "8E", "8F", "8G", "8H",
     "7A", "7B", "7C", "7D", "7E", "7F", "7G", "7H",
     "6A", "6B", "6C", "6D", "6E", "6F", "6G", "6H",
     "5A", "5B", "5C", "5D", "5E", "5F", "5G", "5H",
     "4A", "4B", "4C", "4D", "4E", "4F", "4G", "4H",
     "3A", "3B", "3C", "3D", "3E", "3F", "3G", "3H",
     "2A", "2B", "2C", "2D", "2E", "2F", "2G", "2H",
     "1A", "1B", "1C", "1D", "1E", "1F", "1G", "1H", "FF"};

//valores de entrada
String pos1 = "2A";
String pos2 = "3A";

float precalc_brazo[] =
    {-200, 90, 160, //8A
     -55, 55, 140, //8B
     -28, 50, 135, //8C
     -5, 50, 135, //8D
     35, 50, 135, //8E
     63, 50, 135, //8F
     92, 55, 140, //8G
     120, 60, 145, //8H
     -80, 45, 125, //7A
     0, 0, 180, //7B
     0, 0, 180, //7C
     0, 0, 180, //7D
     0, 0, 180, //7E
     0, 0, 180, //7F
     0, 0, 180, //7G
     0, 0, 180, //7H
     -85, 40, 108, //6A
     0, 0, 180, //6B
     0, 0, 180, //6C
     0, 0, 180, //6D
     0, 0, 180, //6E
     0, 0, 180, //6F
     0, 0, 180, //6G
     0, 0, 180, //6H
     -100, 40, 98, //5A
     0, 0, 180, //5B
     0, 0, 180, //5C
     0, 0, 180, //5D
     0, 0, 180, //5E
     0, 0, 180, //5F
     0, 0, 180, //5G
     0, 0, 180, //5H
     -250, 78, 120, //4A
     0, 0, 180, //4B
     0, 0, 180, //4C
     0, 0, 180, //4D
     0, 0, 180, //4E
     0, 0, 180, //4F
     0, 0, 180, //4G
     0, 0, 180, //4H
     -270, 80, 110, //3A
     0, 0, 180, //3B
     0, 0, 180, //3C
     0, 0, 180, //3D
     0, 0, 180, //3E
     0, 0, 180, //3F
     0, 0, 180, //3G
     0, 0, 180, //3H
     -270, 80, 100, //2A
     0, 0, 180, //2B
     0, 0, 180, //2C
     0, 0, 180, //2D
     0, 0, 180, //2E
     0, 0, 180, //2F
     0, 0, 180, //2G
     0, 0, 180, //2H
     -90, 20, 38, //1A
     0, 0, 180, //1B
     0, 0, 180, //1C
     0, 0, 180, //1D
     0, 0, 180, //1E
     0, 0, 180, //1F
     0, 0, 180, //1G
     0, 0, 180, //1H
     0, 0, 180  //FF
    };

//Variables relacionadas al calculo de angulos
float motorang = 0;
float anghombro = 0;
float angante = 0;
float angpinza = 30;

//-----------------------------------------------------------
//creamos las variables de los componentes
//-----------------------------------------------------------
Servo servomotor1; //Hombro 1 - 0 a 180
Servo servomotor2; //Hombro 2 - 180 a 0
Servo servomotor3; //Antebrazo - 180 a 0
Servo servomotor4; //Pinza - 0 a 180
Stepper motor(2048, 9, 11, 10, 12);	//motor paso a paso

//-----------------------------------------------------------
void setup() {
  //asignar la velocidad del motor
  motor.setSpeed(5);
  //colocar los servos en sus posiciones por defecto
  //(todavia no los conectamos a sus respectivos PINs)
  servomotor1.write(0);
  servomotor2.write(180);
  servomotor3.write(180);
  servomotor4.write(angpinza);
}
//-----------------------------------------------------------
void loop() {
  //Esperamos 2 segundos
  delay(2000);
  //movemos el brazo a su primera posicion
  EnviarBrazo(pos1);
  //Cerramos la pinza
  servomotor4.attach(8);
  delay(500);
  for(int i = angpinza; i >= 0; i--){
    servomotor4.write(i);
    delay(40);
  }
  delay(1000);
  servomotor4.detach();
  delay(500);
  //regresamos el brazo a su pos. inicial
  RegresarBrazo();
  //movemos el brazo a su segunda posicion
  /*EnviarBrazo(pos2);
  //Abrimos la pinza
  servomotor4.attach(8);
  delay(500);
  for(int i = 0; i <= angpinza; i++){
    servomotor4.write(i);
    delay(40);
  }
  delay(1000);
  servomotor4.detach();
  delay(500);
  //regresamos el brazo a su pos. inicial
  RegresarBrazo();
  motor.setSpeed(0);*/
  //atrapar el programa en un loop infinito para no repetir
  int finloop = 1;
  do{
    delay(5000);
  } while (finloop = 1);
}
//-----------------------------------------------------------
void EnviarBrazo(String pos){
  //buscamos los angulos
  int fetch_nom = 0;
  int fetch_prec = 0;
  do{
    if (pos == arraycodigos[fetch_nom]){
      //Obtenemos los angulos precalculados
      motorang = precalc_brazo[fetch_prec];
      anghombro = precalc_brazo[fetch_prec + 1];
      angante = precalc_brazo[fetch_prec + 2];
      break;
    } else {
      fetch_nom += 1;
      fetch_prec += 3;
    }
  } while (fetch_nom < 66);
  //mover el motor a la posición hallada
  motor.step(motorang);
  delay(1000);
  //asignamos los motores a sus respectivos pines
  servomotor1.attach(5);
  servomotor2.attach(6);
  servomotor3.attach(7);
  servomotor4.attach(8);
  delay(500);
  servomotor4.detach();
  delay(2000);
  //mover el antebrazo
  for(int i = 180; i >= angante; i--){
    servomotor3.write(i);
    delay(40);
  }
  delay(1000);
  //mover el hombro
  for(int i = 0; i <= anghombro; i++){
    servomotor1.write(i);
    servomotor2.write(180 - i);
    delay(40);
  }
  delay(1000);
}
//-----------------------------------------------------------
void RegresarBrazo(){
  //Regresar el hombro
  for(int i = anghombro; i >= 0; i--){
    servomotor1.write(i);
    servomotor2.write(180 - i);
    delay(40);
  }
  delay(1000);
  //Regresar el antebrazo
  for(int i = angante; i <= 180; i++){
    servomotor3.write(i);
    delay(40);
  }
  delay(1000);
  //Al terminar, desconectamos los servos para no dejarlos esperando
  servomotor1.detach();
  servomotor2.detach();
  servomotor3.detach();
  delay(1000);
  //Regresar el motor
  motor.step(-motorang);
}