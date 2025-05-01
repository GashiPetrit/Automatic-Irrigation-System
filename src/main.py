{\rtf1\ansi\ansicpg1252\deff0\nouicompat\deflang1033{\fonttbl{\f0\fnil\fcharset0 Courier New;}{\f1\fnil\fcharset0 Calibri;}}
{\*\generator Riched20 10.0.22621}\viewkind4\uc1 
\pard\f0\fs22 import network\par
import socket\par
from machine import Pin, ADC\par
import time\par
\par
# WiFi settings\par
SSID = "Zyxel_D67B"\par
PASSWORD = "A7RX7GN87R"\par
\par
# Connect to WiFi\par
wifi = network.WLAN(network.STA_IF)\par
wifi.active(True)\par
wifi.connect(SSID, PASSWORD)\par
\par
print("Connecting to WiFi...")\par
while not wifi.isconnected():\par
    pass  # Wait for connection\par
\par
print("Connected! IP Address:", wifi.ifconfig()[0])\par
\par
# Define pins\par
sensor = ADC(0)  # Soil moisture sensor on A0\par
relay = Pin(5, Pin.OUT)  # Relay connected to D1 (GPIO5)\par
relay.value(0)  # Start in OFF state\par
\par
# Moisture thresholds\par
DRY_THRESHOLD = 600  # Dry soil (Pump ON)\par
WET_THRESHOLD = 400  # Wet soil (Pump OFF)\par
\par
# Control variables\par
mode = "manual"  # Default mode: manual\par
moisture_log = []  # Stores moisture values\par
last_log_time = time.time()\par
\par
# Create web server\par
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\par
server.bind(("", 80))\par
server.listen(5)\par
\par
print("Web server running...")\par
\par
while True:\par
    conn, addr = server.accept()\par
    print("Connection from", addr)\par
    request = conn.recv(1024).decode("utf-8")\par
    \par
    # Check which mode is selected\par
    if "/on" in request:\par
        print("Manual: Water pump ON!")\par
        relay.value(1)\par
        mode = "manual"\par
    elif "/off" in request:\par
        print("Manual: Water pump OFF!")\par
        relay.value(0)\par
        mode = "manual"\par
    elif "/auto" in request:\par
        print("Mode: Automatic")\par
        mode = "auto"\par
\par
    # Read soil moisture level\par
    moisture_value = sensor.read()\par
    print("Moisture value:", moisture_value)\par
    \par
    # Determine if soil is dry or wet\par
    if moisture_value > DRY_THRESHOLD:\par
        moisture_status = "Dry"\par
        moisture_color = "red"\par
    else:\par
        moisture_status = "Wet"\par
        moisture_color = "green"\par
\par
    # Automatic pump control\par
    if mode == "auto":\par
        if moisture_value > DRY_THRESHOLD:\par
            relay.value(1)  # Turn ON pump\par
        elif moisture_value < WET_THRESHOLD:\par
            relay.value(0)  # Turn OFF pump\par
\par
    # Log moisture data every 8 hours\par
    if time.time() - last_log_time >= 8 * 60 * 60:  # 8 hours in seconds\par
        if len(moisture_log) >= 30:  # Max 30 logged values\par
            moisture_log.pop(0)\par
        moisture_log.append(moisture_value)\par
        last_log_time = time.time()\par
\par
    # Create log for the graph\par
    log_data = ",".join(map(str, moisture_log))\par
\par
    # HTML for the webpage\par
    html = f"""<!DOCTYPE html>\par
<html>\par
<head>\par
    <title>Irrigation Control</title>\par
    <meta name="viewport" content="width=device-width, initial-scale=1">\par
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\par
    <style>\par
        body \{\{ font-family: Arial; text-align: center; \}\}\par
        button \{\{ font-size: 20px; padding: 10px; margin: 10px; width: 120px; \}\}\par
        .on \{\{ background-color: green; color: white; \}\}\par
        .off \{\{ background-color: red; color: white; \}\}\par
        .auto \{\{ background-color: blue; color: white; \}\}\par
        canvas \{\{ max-width: 90%; height: auto; \}\}\par
    </style>\par
</head>\par
<body>\par
    <h1>Irrigation Control</h1>\par
    <p>Soil Status: <span style="color:\{moisture_color\}; font-size: 24px; font-weight: bold;">\{moisture_status\}</span></p>\par
    <p>Current Mode: <strong>\{mode.upper()\}</strong></p>\par
    <p><a href="/on"><button class="on">ON</button></a></p>\par
    <p><a href="/off"><button class="off">OFF</button></a></p>\par
    <p><a href="/auto"><button class="auto">AUTO</button></a></p>\par
\par
    <h2>Soil Moisture Log (Last 30 readings, 8-hour intervals)</h2>\par
    <canvas id="moistureChart"></canvas>\par
\par
    <script>\par
        var ctx = document.getElementById('moistureChart').getContext('2d');\par
        var chart = new Chart(ctx, \{\{\par
            type: 'line',\par
            data: \{\{\par
                labels: Array.from(\{log_data\}.split(','), (_, i) => i + 1),\par
                datasets: [\{\{\par
                    label: 'Moisture Level',\par
                    data: [\{log_data\}],\par
                    borderColor: 'blue',\par
                    borderWidth: 2,\par
                    fill: false\par
                \}\}]\par
            \}\},\par
            options: \{\{\par
                responsive: true,\par
                scales: \{\{\par
                    y: \{\{\par
                        beginAtZero: true,\par
                        suggestedMax: 1024\par
                    \}\}\par
                \}\}\par
            \}\}\par
        \}\});\par
    </script>\par
</body>\par
</html>\par
"""\par
\par
    # Send the webpage as a response\par
    conn.send("HTTP/1.1 200 OK\\nContent-Type: text/html\\n\\n")\par
    conn.send(html)\par
    conn.close()\par
    time.sleep(1)  # Wait a bit before the next reading\par

\pard\sa200\sl276\slmult1\f1\lang9\par
}
 