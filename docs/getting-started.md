# Getting Started with Automatic Irrigation System

This guide walks you through flashing the firmware, wiring the hardware, and opening the web dashboard for your **Automatic Irrigation System** on Windows 11.

---

## 🛠️ Prerequisites

| Tool | Install command (PowerShell) | Notes |
|------|-----------------------------|-------|
| **Git** | `winget install --id Git.Git -e --source winget` | Clone & push updates |
| **Python ≥ 3.10** | `winget install --id Python.Python.3 -e --source winget` | Needed by *esptool* & *mpremote* |
| **esptool + mpremote** | `pip install esptool mpremote` | Flash ESP8266 & upload files |
| **MkDocs** *(optional)* | `pip install mkdocs-material` | Local docs preview |

> **Tip:** after installing with `winget`, close and reopen PowerShell so the new tools are in your `PATH`.

---

## 1️⃣ Clone the repository

```powershell
cd ~\Projects
git clone https://github.com/GashiPetrit/Automatic-Irrigation-System.git
cd Automatic-Irrigation-System
```

---

## 2️⃣ Flash MicroPython to the ESP8266

1. Download the latest MicroPython build for ESP8266—e.g. `esp8266-20231005-v1.20.0.bin`—and place it in the repo root.
2. Plug in the **ESP8266 D1 Mini** via USB.
3. Find the COM port in **Device Manager → Ports (COM & LPT)** (e.g. `COM3`).
4. Run:

```powershell
esptool.py --port COM3 erase_flash
esptool.py --port COM3 --baud 460800 ^
    write_flash -z 0x00000 esp8266-20231005-v1.20.0.bin
```

> Replace **`COM3`** with your actual port. If flashing fails, try a lower baud (e.g. `115200`).

---

## 3️⃣ Upload the project firmware

```powershell
mpremote connect COM3 cp src/main.py :main.py
mpremote connect COM3 cp src/web :/  # ← uploads the entire web UI folder
```

Reset the board (press **RST**) once the files are copied.

---

## 4️⃣ Wire the hardware

![Wiring schematic](../hardware/schema.png "ESP8266 ↔ Sensor ↔ Relay ↔ Pump wiring")

| Signal | ESP8266 Pin | Component lead |
|--------|-------------|----------------|
| Soil‑sensor VCC | 3V3 | VCC |
| Soil‑sensor OUT | A0 | SIG |
| Soil‑sensor GND | G | GND |
| Relay IN | D1 | IN |
| Relay VCC | 5 V | VCC |
| Relay GND | G | GND |
| Pump + | **COM** (relay) | — |
| Pump – | Power adapter – | — |

> Use a step‑down 5 V regulator if your supply exceeds 5 V for the relay.

---

## 5️⃣ First power‑up & Wi‑Fi configuration

1. Connect the 12 V power adapter.
2. The ESP creates a hotspot named **`Irrigation-AP`** (password `water1234`).
3. Join it from your phone/PC and browse to **http://192.168.4.1**.
4. Open **Settings** → enter your home‑Wi‑Fi SSID & password → **Save**.
5. After reboot, the device joins your LAN and prints its new IP on the serial console (or OLED, if attached).

---

## 6️⃣ Open the web dashboard

Open a browser to the device’s LAN IP.
You’ll see live moisture readings, pump status, and a manual **Water Now** button.

![Web UI](../media/Material_1.jpg "Responsive dashboard with real‑time moisture (%) and pump state")



Made with 💧, solder, and plenty of ☕. Happy watering! 🌿

