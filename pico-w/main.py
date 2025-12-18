"""
iRackPilot Firmware for Raspberry Pi Pico W
Main application entry point
"""

import network
import socket
import json
import time
from machine import Pin
import uasyncio as asyncio
from http_server import HTTPServer
from ipmi_client import IPMIClient
from script_engine import ScriptEngine

# WiFi Configuration
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
AP_MODE_SSID = "iRackPilot-{}"
AP_MODE_PASSWORD = "iRackPilot123"

# Server Configuration
HTTP_PORT = 8080
FIRMWARE_VERSION = "1.0.0"

# Global instances
wlan = None
http_server = None
ipmi_client = None
script_engine = None

def setup_wifi():
    """Setup WiFi connection"""
    global wlan
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Try to connect to WiFi
    if WIFI_SSID and WIFI_PASSWORD:
        print(f"Connecting to {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Wait for connection
        max_wait = 20
        while max_wait > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)
        
        if wlan.status() != 3:
            print("Failed to connect to WiFi, starting AP mode...")
            start_ap_mode()
        else:
            ip = wlan.ifconfig()[0]
            print(f'Connected to WiFi. IP: {ip}')
            return ip
    else:
        print("No WiFi credentials, starting AP mode...")
        start_ap_mode()
        return None

def start_ap_mode():
    """Start Access Point mode for configuration"""
    global wlan
    
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    
    # Generate unique SSID
    import ubinascii
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    ssid = AP_MODE_SSID.format(mac[-4:])
    
    ap.config(essid=ssid, password=AP_MODE_PASSWORD)
    ap.config(authmode=3)  # WPA2
    
    ip = ap.ifconfig()[0]
    print(f'AP Mode started. SSID: {ssid}, IP: {ip}')
    return ip

def get_status():
    """Get device status"""
    wifi_connected = wlan and wlan.isconnected() if wlan else False
    ip = wlan.ifconfig()[0] if wifi_connected else "192.168.4.1"
    
    return {
        "status": "ready" if wifi_connected else "ap_mode",
        "firmware_version": FIRMWARE_VERSION,
        "wifi_connected": wifi_connected,
        "ip_address": ip,
        "model": "Pico W"
    }

async def main():
    """Main application loop"""
    global http_server, ipmi_client, script_engine
    
    # Setup WiFi
    ip = setup_wifi()
    
    # Initialize components
    ipmi_client = IPMIClient()
    script_engine = ScriptEngine()
    
    # Start HTTP server
    http_server = HTTPServer(ip or "192.168.4.1", HTTP_PORT)
    http_server.setup_routes(ipmi_client, script_engine, get_status)
    
    print(f"iRackPilot firmware v{FIRMWARE_VERSION} started")
    print(f"HTTP server running on port {HTTP_PORT}")
    
    # Run HTTP server
    await http_server.start()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception as e:
        print(f"Error: {e}")
        import sys
        sys.print_exception(e)

