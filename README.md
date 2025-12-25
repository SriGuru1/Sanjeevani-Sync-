# Sanjeevani Sync – Smart Medicine Reminder System

Sanjeevani Sync is an IoT-based smart medicine reminder and monitoring system designed to help users take medicines on time and notify caregivers in case of missed doses.

The system integrates ESP32-based hardware with a Flask backend, a web interface, and a MySQL database to provide automated reminders and real-time alerts.

---

## Tech Stack

**Hardware**
- ESP32
- Servo Motor
- IR Sensor
- Buzzer
- 5V Power Supply

**Software**
- Backend: Flask (Python)
- Frontend: HTML, CSS
- Database: MySQL
- Communication: HTTP, Wi-Fi
- Alerts: Email via SMTP

---

## How the System Works

1. User logs into the web application and schedules medicine reminders.
2. The backend stores reminder details in a MySQL database.
3. At the scheduled time, the Flask server triggers the ESP32 over Wi-Fi.
4. The servo motor opens the medicine compartment.
5. An IR sensor checks whether the medicine is picked up.
6. If the medicine is not taken:
   - A buzzer alerts the user.
   - An email notification is sent to the registered caregiver.

---

## Key Features

- Remote medicine scheduling through a web interface
- Automated medicine dispensing using ESP32
- Physical verification of medicine intake
- Missed-dose alerts via buzzer and email
- Portable and suitable for elderly users

---


