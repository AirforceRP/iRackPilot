# iRackPilot Firmware

Complete firmware implementation for Raspberry Pi Pico W and Pico 2 W to enable IPMI server management through the iRackPilot iOS app.

## Overview

The firmware provides:
- **HTTP REST API** for iOS app communication
- **Full IPMI 2.0 Protocol** support for server management
- **WiFi Connectivity** with automatic fallback to AP mode
- **Remote Console/KVM** framework
- **Script Execution Engine** for multiple languages
- **Connection Management** with retry and error handling

## Quick Start

**New to iRackPilot?** Start here:

1. **Flash MicroPython** to your Pico device
2. **Upload firmware files** using Thonny or rshell
3. **Configure WiFi** in `main.py`
4. **Connect** from iOS app

**📖 Installation Guides:**
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[INSTALLATION.md](INSTALLATION.md)** - Complete step-by-step guide with troubleshooting

## Firmware Versions

- **Pico W**: `firmware/pico-w/` - For Raspberry Pi Pico W
- **Pico 2 W**: `firmware/pico-2-w/` - For Raspberry Pi Pico 2 W

## Features

### ✅ Implemented

- HTTP REST API server
- WiFi connectivity (STA and AP modes)
- IPMI 2.0 protocol implementation
- Session establishment and authentication
- Device information retrieval
- Chassis power control
- Command execution
- Script execution (Python, DuckyScript)
- Connection retry logic
- Error handling

### 🚧 In Progress

- Full KVM console frame capture
- JavaScript engine integration
- Enhanced script sandboxing

### 📋 Planned

- Web-based configuration interface
- OTA firmware updates
- Advanced IPMI features
- Performance optimizations

## IPMI Protocol Support

The firmware implements the full IPMI 2.0 protocol:

- **RMCP** (Remote Management Control Protocol)
- **Session Management** with authentication
- **Device Commands**:
  - Get Device ID
  - Get Chassis Status
  - Chassis Control (Power On/Off/Cycle)
  - Get System GUID
  - Sensor Reading
- **Vendor Support**: HP, Dell, Generic IPMI servers

## Building UF2 Files

For instructions on creating UF2 firmware files, see [BUILD_UF2.md](BUILD_UF2.md).

Quick reference:
```bash
# Build firmware package
./build.sh pico-w

# Create UF2 from binary (if using C/C++)
python3 create_uf2.py firmware.bin firmware.uf2
```

## API Reference

See [PICO_FIRMWARE_REFERENCE.md](../PICO_FIRMWARE_REFERENCE.md) for complete API documentation.

## File Structure

```
firmware/
├── pico-w/              # Pico W firmware
│   ├── main.py          # Main entry point
│   ├── boot.py          # Boot script
│   ├── http_server.py   # HTTP server
│   ├── ipmi_client.py   # IPMI client
│   ├── ipmi_protocol.py # IPMI protocol
│   └── script_engine.py # Script execution
├── pico-2-w/            # Pico 2 W firmware (same structure)
├── build.sh             # Build script
├── create_uf2.py        # UF2 file creator
├── BUILD_UF2.md         # UF2 build guide
├── INSTALLATION.md      # Installation guide
└── README.md            # This file
```

## Configuration

Edit `main.py` in your firmware directory:

```python
# WiFi Configuration
WIFI_SSID = "YourWiFiNetwork"
WIFI_PASSWORD = "YourPassword"

# Server Configuration
HTTP_PORT = 8080  # Default: 8080
```

## Troubleshooting

### Connection Issues
- Verify WiFi credentials
- Check network connectivity
- Ensure port 8080 is accessible
- Check serial output for errors

### IPMI Connection Fails
- Verify IPMI server credentials
- Check network connectivity between Pico and IPMI server
- Ensure IPMI is enabled on server
- Check firewall settings

### Script Execution Errors
- Verify script syntax
- Check language support
- Review execution output

See [INSTALLATION.md](INSTALLATION.md) for more troubleshooting tips.

## Development

### Requirements
- MicroPython for Pico W/Pico 2 W
- Python 3.x (for build tools)
- Thonny IDE or rshell (for file upload)

### Testing
1. Flash MicroPython to Pico
2. Upload firmware files
3. Test HTTP endpoints:
   ```bash
   curl http://<pico_ip>:8080/status
   ```
4. Test IPMI connection from iOS app

## Contributing

When contributing firmware changes:
1. Test on both Pico W and Pico 2 W
2. Update documentation
3. Follow MicroPython coding standards
4. Add error handling for network operations

## License

See main repository license.

## Resources

- [MicroPython Documentation](https://docs.micropython.org/)
- [Raspberry Pi Pico SDK](https://github.com/raspberrypi/pico-sdk)
- [IPMI 2.0 Specification](https://www.intel.com/content/www/us/en/products/docs/servers/ipmi/ipmi-second-gen-interface-spec-v2-rev1-1.html)
- [UF2 Format Specification](https://github.com/microsoft/uf2)

## Support

For support and questions:
- See [Support Page](../../support/index.html)
- Check [Firmware Page](../../firmware/index.html)
- Visit [GitHub Repository](https://github.com/airforcerp/iRackPilot)

