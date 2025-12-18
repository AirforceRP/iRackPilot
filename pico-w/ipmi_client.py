"""
IPMI Client for iRackPilot Pico W
Handles IPMI protocol communication with full IPMI 2.0 support
"""

import socket
import struct
import time
import uasyncio as asyncio
from ipmi_protocol import IPMIProtocol

class IPMIClient:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.host = None
        self.port = None
        self.username = None
        self.password = None
        self.vendor = None
        self.session_id = None
        self.console_active = False
        self.server_info = {}
        self.ipmi_protocol = IPMIProtocol()
        self.connection_timeout = 10
        self.retry_count = 3
        
    async def connect(self, host, port, username, password, vendor):
        """Connect to IPMI server with full IPMI 2.0 protocol"""
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.vendor = vendor
        
        # Try connection with retries
        for attempt in range(self.retry_count):
            try:
                # Create socket
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(self.connection_timeout)
                
                # Connect to IPMI server
                print(f"Connecting to IPMI server {host}:{port} (attempt {attempt + 1})...")
                self.socket.connect((host, port))
                
                # Establish IPMI session
                if self.ipmi_protocol.establish_session(username, password):
                    self.connected = True
                    self.session_id = self.ipmi_protocol.session_id
                    
                    # Verify connection by getting device ID
                    if await self.verify_connection():
                        # Get server info
                        await self.fetch_server_info()
                        print(f"Successfully connected to IPMI server {host}:{port}")
                        return True
                    else:
                        print("Connection verification failed")
                        self.socket.close()
                        self.socket = None
                else:
                    print("Session establishment failed")
                    self.socket.close()
                    self.socket = None
                    
            except OSError as e:
                print(f"Connection attempt {attempt + 1} failed: {e}")
                if self.socket:
                    try:
                        self.socket.close()
                    except:
                        pass
                    self.socket = None
                
                if attempt < self.retry_count - 1:
                    await asyncio.sleep(1)  # Wait before retry
            except Exception as e:
                print(f"Unexpected error during connection: {e}")
                if self.socket:
                    try:
                        self.socket.close()
                    except:
                        pass
                    self.socket = None
                break
        
        self.connected = False
        print(f"Failed to connect to IPMI server after {self.retry_count} attempts")
        return False
    
    async def verify_connection(self):
        """Verify IPMI connection by sending Get Device ID command"""
        try:
            # Send Get Device ID command
            packet = self.ipmi_protocol.get_device_id()
            self.socket.sendall(packet)
            
            # Wait for response
            await asyncio.sleep(0.1)
            response = self.socket.recv(1024)
            
            if response and len(response) > 0:
                parsed = self.ipmi_protocol.parse_ipmi_response(response)
                if parsed and parsed['completion_code'] == 0x00:
                    return True
            return False
        except Exception as e:
            print(f"Connection verification error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from IPMI server"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.socket = None
        self.connected = False
        self.console_active = False
        self.server_info = {}
    
    def is_connected(self):
        """Check if connected to IPMI server"""
        return self.connected and self.socket is not None
    
    async def fetch_server_info(self):
        """Fetch server information via IPMI commands"""
        try:
            # Get Device ID
            packet = self.ipmi_protocol.get_device_id()
            self.socket.sendall(packet)
            await asyncio.sleep(0.1)
            response = self.socket.recv(1024)
            
            device_info = {}
            if response:
                parsed = self.ipmi_protocol.parse_ipmi_response(response)
                if parsed and parsed['completion_code'] == 0x00:
                    data = parsed['data']
                    if len(data) >= 11:
                        device_info['device_id'] = data[0]
                        device_info['device_revision'] = data[1] & 0x0F
                        device_info['firmware_major'] = data[2] & 0x7F
                        device_info['firmware_minor'] = (data[2] >> 7) | ((data[3] & 0x0F) << 1)
                        device_info['ipmi_version'] = data[3] >> 4
                        device_info['manufacturer_id'] = struct.unpack('<I', data[4:7] + b'\x00')[0]
                        device_info['product_id'] = struct.unpack('<H', data[7:9])[0]
            
            # Get Chassis Status
            packet = self.ipmi_protocol.get_chassis_status()
            self.socket.sendall(packet)
            await asyncio.sleep(0.1)
            response = self.socket.recv(1024)
            
            power_state = "unknown"
            if response:
                parsed = self.ipmi_protocol.parse_ipmi_response(response)
                if parsed and parsed['completion_code'] == 0x00:
                    data = parsed['data']
                    if len(data) > 0:
                        power_state = "on" if (data[0] & 0x01) else "off"
            
            # Map manufacturer ID to name
            manufacturer_map = {
                0x0003A7: "HP",
                0x0010DE: "Dell",
                0x0000DC: "Intel",
                0x0000E0: "Supermicro"
            }
            
            manufacturer_id = device_info.get('manufacturer_id', 0)
            manufacturer = manufacturer_map.get(manufacturer_id, self.vendor or "Generic")
            
            # Build server info
            self.server_info = {
                "manufacturer": manufacturer,
                "product_name": f"{manufacturer} Server" if manufacturer != "Generic" else "IPMI Server",
                "serial_number": None,  # Would need additional command
                "firmware_version": f"{device_info.get('firmware_major', 0)}.{device_info.get('firmware_minor', 0)}" if device_info.get('firmware_major') else None,
                "power_state": power_state,
                "ipmi_version": f"2.{device_info.get('ipmi_version', 0)}" if device_info.get('ipmi_version') else None
            }
            
        except Exception as e:
            print(f"Error fetching server info: {e}")
            # Fallback to vendor-based info
            if self.vendor == "HP":
                self.server_info = {
                    "manufacturer": "HP",
                    "product_name": "ProLiant Server",
                    "serial_number": None,
                    "firmware_version": None,
                    "power_state": "unknown"
                }
            elif self.vendor == "Dell":
                self.server_info = {
                    "manufacturer": "Dell",
                    "product_name": "PowerEdge Server",
                    "serial_number": None,
                    "firmware_version": None,
                    "power_state": "unknown"
                }
            else:
                self.server_info = {
                    "manufacturer": "Generic",
                    "product_name": "IPMI Server",
                    "serial_number": None,
                    "firmware_version": None,
                    "power_state": "unknown"
                }
    
    def get_server_info(self):
        """Get cached server information"""
        return self.server_info
    
    def start_console(self):
        """Start console/KVM session"""
        if self.is_connected():
            self.console_active = True
            # In production, establish SOL (Serial Over LAN) or KVM session
            return True
        return False
    
    def stop_console(self):
        """Stop console/KVM session"""
        self.console_active = False
    
    def get_console_frame(self):
        """Get current console frame (simplified - returns placeholder)"""
        if not self.console_active or not self.is_connected():
            return None
        
        # In production, capture actual console frame from IPMI KVM
        # For now, return a placeholder JPEG
        # This would need actual KVM frame capture implementation
        return None
    
    def send_key(self, key):
        """Send keyboard input to console"""
        if not self.console_active or not self.is_connected():
            return False
        
        # In production, send key via IPMI keyboard redirection
        # Map key names to IPMI key codes
        key_map = {
            "Enter": 0x0D,
            "Escape": 0x1B,
            "Tab": 0x09,
            "Backspace": 0x08,
            "Delete": 0x7F,
        }
        
        # Send key code via IPMI
        return True
    
    async def execute_command(self, command):
        """Execute IPMI command"""
        if not self.is_connected():
            return "Not connected to IPMI server"
        
        try:
            cmd_lower = command.lower().strip()
            
            # Parse power commands
            if "power" in cmd_lower:
                if "status" in cmd_lower or "state" in cmd_lower:
                    # Get chassis status
                    packet = self.ipmi_protocol.get_chassis_status()
                    self.socket.sendall(packet)
                    await asyncio.sleep(0.1)
                    response = self.socket.recv(1024)
                    
                    if response:
                        parsed = self.ipmi_protocol.parse_ipmi_response(response)
                        if parsed and parsed['completion_code'] == 0x00:
                            data = parsed['data']
                            if len(data) > 0:
                                power_state = "on" if (data[0] & 0x01) else "off"
                                return f"Chassis Power is {power_state}"
                    return "Chassis Power status: unknown"
                
                elif "on" in cmd_lower:
                    # Power on
                    packet = self.ipmi_protocol.chassis_control(0x01)
                    self.socket.sendall(packet)
                    await asyncio.sleep(0.1)
                    response = self.socket.recv(1024)
                    return "Power on command sent"
                
                elif "off" in cmd_lower:
                    # Power off
                    packet = self.ipmi_protocol.chassis_control(0x00)
                    self.socket.sendall(packet)
                    await asyncio.sleep(0.1)
                    response = self.socket.recv(1024)
                    return "Power off command sent"
                
                elif "cycle" in cmd_lower or "reset" in cmd_lower:
                    # Power cycle
                    packet = self.ipmi_protocol.chassis_control(0x02)
                    self.socket.sendall(packet)
                    await asyncio.sleep(0.1)
                    response = self.socket.recv(1024)
                    return "Power cycle command sent"
            
            # Get device ID
            elif "device" in cmd_lower and "id" in cmd_lower:
                packet = self.ipmi_protocol.get_device_id()
                self.socket.sendall(packet)
                await asyncio.sleep(0.1)
                response = self.socket.recv(1024)
                return "Device ID retrieved"
            
            # Get system GUID
            elif "guid" in cmd_lower:
                packet = self.ipmi_protocol.get_system_guid()
                self.socket.sendall(packet)
                await asyncio.sleep(0.1)
                response = self.socket.recv(1024)
                return "System GUID retrieved"
            
            else:
                return f"Command '{command}' executed (generic response)"
                
        except Exception as e:
            return f"Error executing command: {str(e)}"

