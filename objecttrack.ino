#include <Array.h>
#include <Servo.h>
#include <PID_v1.h>

Servo pan;  // create servo object to control a servo
Servo tilt; 

String data;
String good_data; 
int pan_pos=90, tilt_pos=90; 

double x_diff = 0;
double y_diff = 0; 

int threshold = 50, rate = 3; 

int obj_posx = 0, obj_posy=0; 
int temp = 0; 
int last_obj_posx = 0, last_obj_posy = 0;

double setpoint, tilt_rate, pan_rate;
double xKp=0.02, xKi=0.005, xKd=0.0;
double yKp=0.02, yKi=0.005, yKd=0.0;

PID pan_PID(&x_diff, &pan_rate, &setpoint, xKp, xKi, xKd, DIRECT);
PID tilt_PID(&y_diff, &tilt_rate, &setpoint, yKp, yKi, yKd, DIRECT);
int calc_diff(int obj_x, int obj_y){
  x_diff = obj_x - 640;
  y_diff = obj_y - 360; 

}

int parse_data_x(String data){ 
  data.remove(data.indexOf("x"));
  return data.toInt(); 
}

int parse_data_y(String data){
  data.remove(0, data.indexOf("x")+1); 
  data.remove(data.indexOf("y"));
  return data.toInt(); 
}

void setup() {
  //turn the PID on
  pan_PID.SetMode(AUTOMATIC);
  pan_PID.SetOutputLimits(-50, 50);
  tilt_PID.SetMode(AUTOMATIC);
  tilt_PID.SetOutputLimits(-50, 50);
  setpoint = 0;

  pan.attach(3);  // attaches the servo on pin 9 to the servo object
  tilt.attach(5); 
  pinMode(LED_BUILTIN, OUTPUT); 
  pan.write(pan_pos);
  tilt.write(tilt_pos); 
  Serial.begin(500000);
  Serial.setTimeout(1);

}

void loop() {
  while (Serial.available() > 0) {
    data = Serial.readString();

    obj_posx = parse_data_x(data);
    obj_posy = parse_data_y(data);
    calc_diff(obj_posx, obj_posy);
    pan_PID.Compute();
    tilt_PID.Compute();

    if (x_diff > threshold || x_diff < 0){
      pan_pos += pan_rate;
    }

    if (y_diff > threshold || y_diff < 0){
      tilt_pos -= tilt_rate;
    }

    pan.write(pan_pos);
    tilt.write(tilt_pos); 
    Serial.print(tilt_rate); 
  }
}
