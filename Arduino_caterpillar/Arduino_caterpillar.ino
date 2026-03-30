/*
 * Scooby-Bot - Firmware per Arduino Uno
 * Riceve comandi PWM per i motori via Seriale (115200 baud)
 * Formato messaggio: "L<valore>;R<valore>\n" (es: L200;R-200)
 */

#define ML_Ctrl 4
#define ML_PWM 6
#define MR_Ctrl 2
#define MR_PWM 5

// Definizione Pin Shield Motori (Configurazione standard Keyestudio/L298P)
const int M1 = 4; // Direzione Motore A (Sinistro) - ML_Ctrl
const int E1 = 6; // PWM Motore A (Sinistro)      - ML_PWM
const int M2 = 2; // Direzione Motore B (Destro)  - MR_Ctrl
const int E2 = 5; // PWM Motore B (Destro)        - MR_PWM

void setup() {
  Serial.begin(115200);
  
  pinMode(M1, OUTPUT);
  pinMode(M2, OUTPUT);
  pinMode(E1, OUTPUT);
  pinMode(E2, OUTPUT);

  // Stop motori all'avvio
  stopMotors();
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    parseAndDrive(input);
    delay(5);
  }
}

void parseAndDrive(String cmd) {
  // Esempio cmd: "L255;R-255"
  int delimiterIndex = cmd.indexOf(';');
  if (delimiterIndex == -1) return;

  // Estrazione sottostringhe e conversione in interi
  String leftStr = cmd.substring(1, delimiterIndex); // Salta la 'L'
  String rightStr = cmd.substring(delimiterIndex + 2); // Salta ';R'
  
  int pwmL = leftStr.toInt();
  int pwmR = rightStr.toInt();

  controlMotors(pwmL, pwmR);
  
 
}

void controlMotors(float leftSpeed, float rightSpeed) {
  int k = 5;

  // Controllo del motore sinistro
  if (leftSpeed - k > 0) {
    digitalWrite(ML_Ctrl, LOW);  // Direzione avanti
    analogWrite(ML_PWM, (int)leftSpeed);
  } else if (leftSpeed + k < 0) {
    digitalWrite(ML_Ctrl, HIGH);  // Direzione indietro
    analogWrite(ML_PWM, (int)leftSpeed);
  } else {
    digitalWrite(ML_Ctrl, LOW);
    analogWrite(ML_PWM, 0);  // Stop motore sinistro
  }

  // Controllo del motore destro
  if (rightSpeed - k > 0) {
    digitalWrite(MR_Ctrl, LOW);  // Direzione avanti
    analogWrite(MR_PWM, (int)rightSpeed);
  } else if (rightSpeed + k < 0) {
    digitalWrite(MR_Ctrl, HIGH);  // Direzione indietro
    analogWrite(MR_PWM, (int)rightSpeed);
  } else {
    digitalWrite(MR_Ctrl, LOW);
    analogWrite(MR_PWM, 0);  // Stop motore destro
  }
}

void stopMotors() {
  analogWrite(E1, 0);
  analogWrite(E2, 0);
}
