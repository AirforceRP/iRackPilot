# iRackPilot Firmware Quick Start

Get up and running in 5 minutes!

## Prerequisites

- Raspberry Pi Pico W or Pico 2 W
- USB cable (data-capable)
- WiFi credentials
- Computer with USB port

## Quick Installation

### 1. Flash MicroPython (2 minutes)

1. Download MicroPython: https://micropython.org/download/rp2-pico-w/
2. Hold **BOOTSEL** button, connect USB
3. Copy `.uf2` file to **RPI-RP2** drive
4. Pico reboots automatically ✅

### 2. Upload Firmware (2 minutes)

**Using Thonny (Easiest):**

1. Install Thonny: https://thonny.org/
2. Connect Pico (no BOOTSEL needed)
3. In Thonny: **Tools > Options > Interpreter > MicroPython (Raspberry Pi Pico)**
4. Upload these files from `firmware/pico-w/` (or `pico-2-w/`):
   - `boot.py`
   - `main.py`
   - `http_server.py`
   - `ipmi_client.py`
   - `ipmi_protocol.py`
   - `script_engine.py`

   **How:** Open each file, then **File > Save As > Raspberry Pi Pico**

### 3. Configure WiFi (1 minute)

1. Open `main.py` on Pico in Thonny
2. Edit these lines:
   ```python
   WIFI_SSID = "YourWiFiNetwork"
   WIFI_PASSWORD = "YourPassword"
   ```
3. Save to Pico
4. Restart Pico (unplug/replug USB)

### 4. Verify (30 seconds)

1. Check Thonny Shell/REPL - you should see:
   ```
   Connected to WiFi. IP: 192.168.1.XXX
   HTTP server listening on 192.168.1.XXX:8080
   ```
2. Note the IP address!

### 5. Connect from iOS App

1. Open iRackPilot app
2. **Devices tab > + button**
3. Enter:
   - **Name:** `My Pico`
   - **IP Address:** `192.168.1.XXX` (from step 4)
   - **Port:** `8080`
   - **Model:** `Pico W` or `Pico 2 W`
4. Tap **Connect** ✅

## Test Connection

In browser or curl:
```bash
curl http://192.168.1.XXX:8080/status
```

Should return JSON with device status.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| RPI-RP2 not appearing | Try different USB cable/port, hold BOOTSEL longer |
| WiFi won't connect | Check 2.4GHz network (not 5GHz), verify credentials |
| HTTP not responding | Check IP address, ensure same network, check firewall |
| Import errors | Verify all 6 files uploaded, restart Pico |

## Need More Help?

- 📖 Full guide: [INSTALLATION.md](INSTALLATION.md)
- 💬 Support: [Support Page](../../support/index.html)
- 🐙 GitHub: [Repository](https://github.com/airforcerp/iRackPilot)

## File Checklist

- [ ] MicroPython flashed
- [ ] All 6 Python files uploaded
- [ ] WiFi configured in `main.py`
- [ ] HTTP server responding
- [ ] iOS app connected

**Done!** 🎉 Your Pico is ready to manage IPMI servers!

