# iRackPilot Firmware Installation Guide

Complete step-by-step guide for installing iRackPilot firmware on Raspberry Pi Pico W and Pico 2 W.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Install MicroPython](#step-1-install-micropython)
3. [Step 2: Upload Firmware Files](#step-2-upload-firmware-files)
4. [Step 3: Configure WiFi](#step-3-configure-wifi)
5. [Step 4: Verify Installation](#step-4-verify-installation)
6. [Step 5: Connect from iOS App](#step-5-connect-from-ios-app)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Configuration](#advanced-configuration)

---

## Prerequisites

Before you begin, ensure you have:

- ✅ **Raspberry Pi Pico W** or **Pico 2 W** device
- ✅ **USB cable** (data-capable, not charge-only)
- ✅ **Computer** with USB port (Windows, Mac, or Linux)
- ✅ **WiFi network** credentials (SSID and password)
- ✅ **Internet connection** (for downloading MicroPython)
- ✅ **IPMI-enabled server** (for testing after installation)

### Software Requirements

- **MicroPython** (will be downloaded in Step 1)
- **Thonny IDE** (recommended) or alternative:
  - [Thonny](https://thonny.org/) - Easiest option
  - `rshell` - Command-line tool
  - `ampy` - Adafruit MicroPython tool

---

## Step 1: Install MicroPython

MicroPython is the Python runtime that runs on the Pico. We need to flash it first.

### 1.1 Download MicroPython

**For Raspberry Pi Pico W:**
1. Visit: https://micropython.org/download/rp2-pico-w/
2. Download the latest `.uf2` file (e.g., `rp2-pico-w-20231005-v1.21.0.uf2`)

**For Raspberry Pi Pico 2 W:**
1. Visit: https://micropython.org/download/rp2-pico-w/
2. Look for Pico 2 W specific version or use the latest Pico W version
3. Download the `.uf2` file

> **Note:** The file will be named something like `rp2-pico-w-YYYYMMDD-vX.XX.X.uf2`

### 1.2 Enter Bootloader Mode

1. **Locate the BOOTSEL button** on your Pico (usually on the side)
2. **Hold down the BOOTSEL button** (don't release yet)
3. **While holding BOOTSEL**, connect the USB cable to your computer
4. **Release the BOOTSEL button** after connecting
5. A drive named **RPI-RP2** should appear on your computer

> **Troubleshooting:** If RPI-RP2 doesn't appear:
> - Try a different USB cable (must support data transfer)
> - Try a different USB port
> - Hold BOOTSEL longer before connecting
> - On Windows, check Device Manager for unrecognized devices

### 1.3 Flash MicroPython

1. **Open the RPI-RP2 drive** (it should be empty or contain `INDEX.HTM` and `INFO_UF2.TXT`)
2. **Drag and drop** the downloaded `.uf2` file into the RPI-RP2 drive
3. The Pico will **automatically reboot** and the RPI-RP2 drive will disappear
4. MicroPython is now installed! ✅

> **Note:** The RPI-RP2 drive disappearing is normal - it means MicroPython is running.

---

## Step 2: Upload Firmware Files

Now we'll upload the iRackPilot firmware files to your Pico.

### Method A: Using Thonny (Recommended for Beginners)

#### 2A.1 Install Thonny

1. **Download Thonny:**
   - Visit: https://thonny.org/
   - Download for your operating system (Windows/Mac/Linux)
   - Install Thonny

2. **Open Thonny**

#### 2A.2 Connect to Pico

1. **Connect your Pico** to the computer via USB (no need to hold BOOTSEL this time)
2. In Thonny, go to **Tools > Options > Interpreter**
3. Select **"MicroPython (Raspberry Pi Pico)"** from the dropdown
4. Select the correct **Port** (usually auto-detected):
   - **Windows:** `COM3`, `COM4`, etc.
   - **Mac/Linux:** `/dev/tty.usbmodem*` or `/dev/ttyACM0`
5. Click **OK**

6. **Test connection:**
   - In the Shell/REPL at the bottom, type: `print("Hello Pico!")`
   - Press Enter
   - You should see `Hello Pico!` printed

#### 2A.3 Upload Firmware Files

1. **Navigate to firmware directory:**
   - For Pico W: `firmware/pico-w/`
   - For Pico 2 W: `firmware/pico-2-w/`

2. **Upload each file:**
   - Open `boot.py` in Thonny
   - Go to **File > Save As...**
   - Select **"Raspberry Pi Pico"** from the location dropdown
   - Save as `boot.py`
   - Repeat for these files:
     - ✅ `boot.py`
     - ✅ `main.py`
     - ✅ `http_server.py`
     - ✅ `ipmi_client.py`
     - ✅ `ipmi_protocol.py`
     - ✅ `script_engine.py`

3. **Verify files uploaded:**
   - In Thonny, go to **View > Files**
   - You should see all 6 files listed

### Method B: Using rshell (Command Line)

#### 2B.1 Install rshell

```bash
# Install rshell
pip install rshell
```

#### 2B.2 Connect to Pico

```bash
# Linux/Mac
rshell -p /dev/ttyACM0

# Windows
rshell -p COM3

# Auto-detect port
rshell
```

#### 2B.3 Upload Files

```bash
# Navigate to firmware directory
cd firmware/pico-w  # or pico-2-w

# Copy files to Pico
cp boot.py /pyboard/
cp main.py /pyboard/
cp http_server.py /pyboard/
cp ipmi_client.py /pyboard/
cp ipmi_protocol.py /pyboard/
cp script_engine.py /pyboard/

# Verify files
ls /pyboard/
```

### Method C: Using ampy

#### 2C.1 Install ampy

```bash
pip install adafruit-ampy
```

#### 2C.2 Upload Files

```bash
# Upload each file
ampy --port /dev/ttyACM0 put boot.py
ampy --port /dev/ttyACM0 put main.py
ampy --port /dev/ttyACM0 put http_server.py
ampy --port /dev/ttyACM0 put ipmi_client.py
ampy --port /dev/ttyACM0 put ipmi_protocol.py
ampy --port /dev/ttyACM0 put script_engine.py

# Windows users: replace /dev/ttyACM0 with COM3 (or your port)
```

---

## Step 3: Configure WiFi

Your Pico needs WiFi credentials to connect to your network.

### Method 1: Edit main.py (Recommended)

1. **Open `main.py` on your Pico** (using Thonny or your editor)
2. **Find these lines:**
   ```python
   WIFI_SSID = "YOUR_WIFI_SSID"
   WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
   ```
3. **Replace with your WiFi credentials:**
   ```python
   WIFI_SSID = "MyWiFiNetwork"
   WIFI_PASSWORD = "MyPassword123"
   ```
4. **Save the file** to your Pico
5. **Restart the Pico** (unplug and replug USB, or press reset button)

### Method 2: Use AP Mode (No WiFi Config Needed)

If you don't want to edit files, the Pico will create its own WiFi network:

1. **Don't set WiFi credentials** in `main.py` (leave as `YOUR_WIFI_SSID`)
2. **Power on the Pico**
3. **Look for WiFi network:** `iRackPilot-XXXX` (where XXXX is last 4 digits of MAC address)
4. **Connect with password:** `iRackPilot123`
5. **Pico IP address:** `192.168.4.1`
6. **Note:** In AP mode, your iOS device must connect to the Pico's network to communicate

> **Tip:** AP mode is useful for initial setup, but STA mode (Method 1) is better for regular use.

---

## Step 4: Verify Installation

Let's make sure everything is working!

### 4.1 Check Serial Output

1. **Open Thonny** (or your serial monitor)
2. **Connect to Pico** (if not already connected)
3. **Look at the Shell/REPL output**

You should see:
```
iRackPilot Firmware Booting...
Connecting to MyWiFiNetwork...
Connected to WiFi. IP: 192.168.1.100
iRackPilot firmware v1.0.0 started
HTTP server listening on 192.168.1.100:8080
```

> **Important:** Note the IP address shown (e.g., `192.168.1.100`) - you'll need this!

### 4.2 Test HTTP Server

**Option A: Using Browser**
1. Open a web browser
2. Navigate to: `http://[PICO_IP]:8080/status`
   - Replace `[PICO_IP]` with the IP from Step 4.1
   - Example: `http://192.168.1.100:8080/status`
3. You should see JSON response:
   ```json
   {
     "status": "ready",
     "firmware_version": "1.0.0",
     "wifi_connected": true,
     "ip_address": "192.168.1.100",
     "model": "Pico W"
   }
   ```

**Option B: Using curl (Command Line)**
```bash
curl http://192.168.1.100:8080/status
```

**Option C: Using Thonny**
```python
import urequests
response = urequests.get("http://192.168.1.100:8080/status")
print(response.text)
```

### 4.3 Verify All Files

In Thonny, check that all files are present:
- Go to **View > Files**
- You should see:
  - ✅ `boot.py`
  - ✅ `main.py`
  - ✅ `http_server.py`
  - ✅ `ipmi_client.py`
  - ✅ `ipmi_protocol.py`
  - ✅ `script_engine.py`

---

## Step 5: Connect from iOS App

Now connect your iOS app to the Pico!

### 5.1 Get Pico IP Address

From Step 4.1, you should have the IP address. If you missed it:
1. Check serial output in Thonny
2. Or test the status endpoint (Step 4.2) - it shows the IP

### 5.2 Add Device in iOS App

1. **Open iRackPilot app** on your iPhone/iPad
2. **Go to Devices tab**
3. **Tap the + button**
4. **Enter device information:**
   - **Name:** `My Pico Device` (or any name)
   - **IP Address:** `192.168.1.100` (your Pico's IP)
   - **Port:** `8080` (default)
   - **Model:** Select `Pico W` or `Pico 2 W`
5. **Tap Connect** or **Save**

### 5.3 Test Connection

1. **Tap on your device** in the Devices list
2. **Connection status** should change to "Connected"
3. **Device details** should be displayed

### 5.4 Connect to IPMI Server

1. **Go to Servers tab** in the app
2. **Add an IPMI server:**
   - **Name:** `My Server`
   - **Host:** IPMI server IP (e.g., `192.168.1.50`)
   - **Port:** `623` (default IPMI port)
   - **Username:** Your IPMI username
   - **Password:** Your IPMI password
   - **Vendor:** Select `HP`, `Dell`, or `Generic`
3. **Tap Connect**
4. **Server should connect** through your Pico device

---

## Troubleshooting

### Pico Not Appearing as RPI-RP2 Drive

**Symptoms:** RPI-RP2 drive doesn't appear when holding BOOTSEL

**Solutions:**
- ✅ Try a different USB cable (must support data, not charge-only)
- ✅ Try a different USB port (prefer USB 2.0 ports)
- ✅ Hold BOOTSEL longer (2-3 seconds) before connecting
- ✅ On Windows: Check Device Manager for unrecognized devices
- ✅ Try a different computer
- ✅ Ensure Pico is getting power (LED should light up)

### MicroPython Not Flashing

**Symptoms:** UF2 file doesn't flash, or Pico doesn't reboot

**Solutions:**
- ✅ Ensure you're using the correct UF2 file for your Pico model
- ✅ Try downloading MicroPython again (file might be corrupted)
- ✅ Check file size (should be several MB)
- ✅ Try a different USB cable
- ✅ Format RPI-RP2 drive if it appears but flashing fails

### WiFi Connection Fails

**Symptoms:** Pico doesn't connect to WiFi, or shows "Failed to connect"

**Solutions:**
- ✅ **Verify SSID and password** are correct (case-sensitive!)
- ✅ **Check WiFi frequency:** Pico W only supports 2.4GHz (not 5GHz)
- ✅ **Check router settings:**
  - MAC address filtering (disable or add Pico's MAC)
  - Hidden SSID (Pico can't connect to hidden networks)
  - WPA3 (use WPA2 instead)
- ✅ **Move closer to router** (weak signal)
- ✅ **Try AP mode** to verify Pico WiFi is working
- ✅ **Check serial output** for specific error messages

### HTTP Server Not Responding

**Symptoms:** Can't access `http://[IP]:8080/status`

**Solutions:**
- ✅ **Verify IP address** is correct (check serial output)
- ✅ **Check firewall settings** on your computer/router
- ✅ **Ensure Pico and computer are on same network**
- ✅ **Try different port** (edit `HTTP_PORT` in `main.py`)
- ✅ **Check serial output** for errors
- ✅ **Restart Pico** (unplug/replug USB)
- ✅ **Test with curl** instead of browser

### Import Errors

**Symptoms:** Errors like "ModuleNotFoundError" or "ImportError"

**Solutions:**
- ✅ **Verify all files uploaded** (check file list in Thonny)
- ✅ **Check file names** match exactly (case-sensitive)
- ✅ **Ensure files are in root directory** (not in subfolders)
- ✅ **Restart Pico** after uploading files
- ✅ **Re-upload missing files**

### IPMI Connection Fails

**Symptoms:** Can't connect to IPMI server through Pico

**Solutions:**
- ✅ **Verify Pico is connected first** (check Devices tab)
- ✅ **Check IPMI server credentials** (username/password)
- ✅ **Verify IPMI server IP and port** are correct
- ✅ **Ensure IPMI is enabled** on the server
- ✅ **Check network connectivity** between Pico and IPMI server
- ✅ **Verify firewall** allows port 623 (IPMI port)
- ✅ **Test IPMI server** with another tool (e.g., `ipmitool`)
- ✅ **Check serial output** for specific error messages

### Script Execution Errors

**Symptoms:** Scripts fail to execute

**Solutions:**
- ✅ **Verify script syntax** is correct
- ✅ **Check language support** (Python works, JS needs engine)
- ✅ **Ensure Pico is connected** before executing
- ✅ **Check script size** (Pico has limited memory)
- ✅ **Review execution output** for specific errors

### Device Not Found in iOS App

**Symptoms:** Can't find or connect to Pico from app

**Solutions:**
- ✅ **Verify Pico and iOS device are on same WiFi network**
- ✅ **Check IP address** is correct
- ✅ **Ensure HTTP server is running** (check serial output)
- ✅ **Test status endpoint** from browser first
- ✅ **Check iOS device firewall/VPN** settings
- ✅ **Try AP mode** if networks are different

---

## Advanced Configuration

### Change HTTP Port

Edit `main.py`:
```python
HTTP_PORT = 8080  # Change to any port (e.g., 9000)
```

### Enable Debug Mode

Add to `main.py`:
```python
DEBUG = True
```

Then add debug prints throughout code for troubleshooting.

### Custom AP Mode Settings

Edit `main.py`:
```python
AP_MODE_SSID = "MyCustomName"
AP_MODE_PASSWORD = "MyCustomPassword"
```

### Connection Timeout Settings

Edit `ipmi_client.py`:
```python
self.connection_timeout = 10  # Seconds
self.retry_count = 3  # Number of retry attempts
```

### Static IP Address (Advanced)

For advanced users, you can configure static IP in `main.py`:
```python
import network

wlan = network.WLAN(network.STA_IF)
wlan.ifconfig(('192.168.1.100', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
```

---

## Next Steps

After successful installation:

1. ✅ **Test IPMI Connection**
   - Add IPMI server in iOS app
   - Connect through Pico
   - Verify server information displays

2. ✅ **Test Console/KVM**
   - Start console session
   - View remote screen
   - Test keyboard input

3. ✅ **Execute Scripts**
   - Create test script
   - Execute via iOS app
   - Review output

4. ✅ **Monitor Status**
   - Check connection statistics
   - View uptime/downtime
   - Monitor notifications

---

## Additional Resources

- 📖 [Firmware Reference](../../PICO_FIRMWARE_REFERENCE.md) - Complete API documentation
- 🔧 [Build UF2 Guide](BUILD_UF2.md) - Creating custom UF2 files
- 💬 [Support Page](../../support/index.html) - Help and troubleshooting
- 📱 [Firmware Page](../../firmware/index.html) - Firmware information
- 🐙 [GitHub Repository](https://github.com/airforcerp/iRackPilot) - Source code

---

## Quick Reference

### Essential Commands

```bash
# Test HTTP server
curl http://[PICO_IP]:8080/status

# Check Pico files (rshell)
rshell -p /dev/ttyACM0
ls /pyboard/

# Upload file (ampy)
ampy --port /dev/ttyACM0 put main.py
```

### File Checklist

- [ ] `boot.py` uploaded
- [ ] `main.py` uploaded and configured
- [ ] `http_server.py` uploaded
- [ ] `ipmi_client.py` uploaded
- [ ] `ipmi_protocol.py` uploaded
- [ ] `script_engine.py` uploaded
- [ ] WiFi credentials configured
- [ ] HTTP server responding
- [ ] iOS app can connect

### Default Settings

- **HTTP Port:** 8080
- **AP Mode SSID:** `iRackPilot-XXXX`
- **AP Mode Password:** `iRackPilot123`
- **AP Mode IP:** 192.168.4.1
- **IPMI Port:** 623

---

## Support

If you encounter issues not covered in this guide:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review [Support Page](../../support/index.html)
3. Check serial output for error messages
4. Open an issue on [GitHub](https://github.com/airforcerp/iRackPilot)

---

**Congratulations!** 🎉 You've successfully installed iRackPilot firmware on your Pico device!
