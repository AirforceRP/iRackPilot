# Firmware Changelog

All notable changes to the iRackPilot firmware will be documented in this file.

## [1.0.0] - 2025-01-XX

### Added
- Initial firmware release for Pico W and Pico 2 W
- HTTP REST API server
- WiFi connectivity (STA and AP modes)
- IPMI client implementation
- Remote console/KVM support framework
- Script execution engine
- Status monitoring endpoint
- Boot script with LED indication

### Features
- Automatic WiFi connection with fallback to AP mode
- HTTP server on configurable port (default: 8080)
- IPMI connection management
- Console frame capture (placeholder)
- Script execution for multiple languages
- Device status reporting

### Known Limitations
- IPMI protocol implementation is simplified (needs full IPMI 2.0 support)
- Console frame capture returns placeholder (needs actual KVM implementation)
- JavaScript execution requires JS engine (not yet integrated)
- C++ execution requires compilation (not yet supported)
- Bash execution not available on MicroPython

### Future Enhancements
- Full IPMI 2.0 protocol implementation
- Actual KVM console frame capture
- JavaScript engine integration (Duktape/QuickJS)
- Enhanced script sandboxing
- Web-based configuration interface
- OTA firmware updates
- Enhanced error handling and logging

