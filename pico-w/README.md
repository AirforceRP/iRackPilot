# iRackPilot Firmware for Raspberry Pi Pico W

This firmware enables the Raspberry Pi Pico W to act as a bridge between the iRackPilot iOS app and IPMI servers.

## Features

- HTTP REST API server
- WiFi connectivity (STA and AP modes)
- IPMI client implementation
- Remote console/KVM support
- Script execution engine
- Real-time status monitoring

## Installation

1. **Flash MicroPython to Pico W**
   - Download MicroPython for Pico W from [micropython.org](https://micropython.org/download/rp2-pico-w/)
   - Hold BOOTSEL button and connect USB
   - Copy the .uf2 file to RPI-RP2 drive

2. **Upload Firmware Files**
   - Copy all files from this directory to your Pico W
   - Use Thonny, rshell, or similar tool

3. **Configure WiFi**
   - Edit `main.py` and set `WIFI_SSID` and `WIFI_PASSWORD`
   - Or connect via AP mode (default SSID: iRackPilot-XXXX)

4. **Run Firmware**
   - The firmware will start automatically on boot
   - Check serial output for IP address

## File Structure

- `main.py` - Main application entry point
- `boot.py` - Boot script (runs on startup)
- `http_server.py` - HTTP server implementation
- `ipmi_client.py` - IPMI protocol client with full IPMI 2.0 support
- `ipmi_protocol.py` - IPMI 2.0 protocol implementation
- `script_engine.py` - Script execution engine

## Configuration

Edit `main.py` to configure:

```python
WIFI_SSID = "YourWiFiNetwork"
WIFI_PASSWORD = "YourPassword"
HTTP_PORT = 8080  # Default: 8080
```

## API Endpoints

See [PICO_FIRMWARE_REFERENCE.md](../../PICO_FIRMWARE_REFERENCE.md) for complete API documentation.

## IPMI Protocol Support

The firmware includes full IPMI 2.0 protocol implementation:
- RMCP (Remote Management Control Protocol)
- Session establishment and authentication
- Device ID retrieval
- Chassis control (power on/off/cycle)
- Server information queries
- Command execution

## Building UF2 Files

See [BUILD_UF2.md](../BUILD_UF2.md) for detailed instructions on creating UF2 firmware files.

## Requirements

- MicroPython for Pico W
- Network connectivity
- IPMI-enabled server

## Troubleshooting

- Check serial output for error messages
- Verify WiFi credentials
- Ensure port 8080 is accessible
- Check IPMI server connectivity

## License

See main repository license.

