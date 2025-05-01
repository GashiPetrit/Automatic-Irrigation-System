<!-- Hero Demo Video -->
<p align="center">
  <video src="media/applicerar_fukt.mp4" controls width="75%">
    Sorry—your browser doesn’t support embedded video.
  </video>
</p>

<h1 align="center">🌱 Automatic Irrigation System</h1>

<p align="center"><em>
A Wi-Fi-enabled plant-watering controller that keeps your greens thriving while you work on bigger projects.
</em></p>

<div align="center">

![GitHub last commit](https://img.shields.io/github/last-commit/GashiPetrit/Automatic-Irrigation-System?style=flat-square)
![License](https://img.shields.io/github/license/GashiPetrit/Automatic-Irrigation-System?style=flat-square)
![Made with MicroPython](https://img.shields.io/badge/MicroPython-ESP8266-orange?style=flat-square)
![Responsive Web UI](https://img.shields.io/badge/Web_UI-Responsive-brightgreen?style=flat-square)

</div>

---

<!-- System Overview Diagram -->
<p align="center">
  <img src="media/system_overview.png" alt="System overview: Moisture Sensor → ESP8266 D1 Mini → Browser UI & Relay → Pump   |   12 V Adapter → 5 V Reg → ESP8266 & Relay" width="80%">
</p>

---

## ✨ Features at a Glance

| Capability | Details |
|------------|---------|
| 🌡 **Live moisture sensing** | Capacitive sensor logs soil %RH every 10 s |
| 💧 **Automatic pump control** | 12 V DC pump toggled via 5 V relay |
| 📶 **Wi-Fi + Web UI** | ESP8266 hosts a mobile-friendly dashboard |
| 🕒 **Scheduling & logging** | Time-based watering + CSV log download |
| 🔌 **Fail-safe manual mode** | Hardware button overrides automation |

---

## 🖼 Screenshot & Diagram Gallery

| | |
|---|---|
| ![Thought Process](media/ThoughtProcess_of_system_overview.png) | *Early design sketch* |
| ![Final System Diagram](media/system_overview.png) | *High-level wiring overview* |

---

## 🔧 Soldering Walk-through

<p align="center">
  <video src="media/petrit_loddar.mp4" controls width="65%">
    Sorry—your browser doesn’t support embedded video.
  </video>
</p>

---

## 🚀 Quick Start

```bash
git clone https://github.com/GashiPetrit/Automatic-Irrigation-System.git
cd Automatic-Irrigation-System

# Flash MicroPython (adjust COM port)
esptool.py --port COM3 erase_flash
esptool.py --port COM3 --baud 460800 write_flash -z 0x00000 esp8266-20231005-v1.20.0.bin

# Upload firmware
mpremote connect COM3 cp src/main.py :main.py
