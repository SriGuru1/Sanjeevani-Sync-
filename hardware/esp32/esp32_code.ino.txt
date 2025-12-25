#include <WiFi.h>
#include <HTTPClient.h>
#include <ESP32Servo.h>

Servo servoMotor;

// WiFi credentials (replace locally, do NOT commit real values)
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// Backend server endpoint
const char* serverUrl = "http://<SERVER_IP>:5000/email";

// Pin configuration
#define SERVO_PIN 13
#define IR_SENSOR_PIN 14
#define BUZZER_PIN 27

bool medicineTaken = false;

void setup() {
  Serial.begin(115200);

  pinMode(IR_SENSOR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  servoMotor.attach(SERVO_PIN);
  servoMotor.write(0);  // Lid closed

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
}

void loop() {
  // Simulated trigger (replace with time-based trigger in production)
  delay(10000);

  openDispenser();
  checkMedicinePickup();
}

void openDispenser() {
  servoMotor.write(90);  // Open lid
  delay(1000);
}

void checkMedicinePickup() {
  unsigned long startTime = millis();
  medicineTaken = false;

  while (millis() - startTime < 30000) { // 30 seconds window
    if (digitalRead(IR_SENSOR_PIN) == HIGH) {
      medicineTaken = true;
      break;
    }

    // After 15 seconds, activate buzzer
    if (millis() - startTime > 15000) {
      digitalWrite(BUZZER_PIN, HIGH);
    }
  }

  digitalWrite(BUZZER_PIN, LOW);
  servoMotor.write(0);  // Close lid

  if (!medicineTaken) {
    sendMissedDoseAlert();
  }
}

void sendMissedDoseAlert() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String payload = "{\"email\":\"caregiver@example.com\", \"message\":\"Medicine dose missed\"}";
    int responseCode = http.POST(payload);

    Serial.print("HTTP Response code: ");
    Serial.println(responseCode);

    http.end();
  }
}
