"""
IPMI Protocol Implementation for iRackPilot
Implements IPMI 2.0 protocol for connecting to IPMI servers
"""

import struct
import hashlib
import os
import time

class IPMIProtocol:
    """IPMI 2.0 Protocol Handler"""
    
    # IPMI Constants
    RMCP_VERSION = 0x06
    RMCP_SEQ = 0x00
    IPMI_SESSION_HEADER = 0x00
    
    # Authentication Types
    AUTH_NONE = 0x00
    AUTH_MD5 = 0x01
    AUTH_PASSWORD = 0x02
    AUTH_MD2 = 0x04
    
    # Session States
    SESSION_STATE_INVALID = 0
    SESSION_STATE_OPEN = 1
    SESSION_STATE_ACTIVE = 2
    
    def __init__(self):
        self.session_id = 0
        self.session_seq = 0
        self.session_state = self.SESSION_STATE_INVALID
        self.auth_type = self.AUTH_PASSWORD
        self.username = None
        self.password = None
        self.bmc_session_id = 0
        self.bmc_session_seq = 0
        
    def create_rmcp_header(self, message_class=0x06, message_type=0x00):
        """Create RMCP header"""
        # RMCP Header: Version(1) + Reserved(1) + Sequence(1) + Class(1)
        return struct.pack('BBBB',
            self.RMCP_VERSION,  # Version
            0x00,              # Reserved
            self.RMCP_SEQ,     # Sequence
            message_class      # Message Class
        )
    
    def create_ipmi_session_header(self, session_id, sequence, auth_type):
        """Create IPMI session header"""
        # Session Header: Auth Type(1) + Session ID(4) + Sequence(4) + Auth Code(16)
        header = struct.pack('B', auth_type)
        header += struct.pack('<I', session_id)  # Little-endian
        header += struct.pack('<I', sequence)
        header += b'\x00' * 16  # Auth code (placeholder)
        return header
    
    def create_ipmi_request(self, netfn, lun, cmd, data=b''):
        """Create IPMI request message"""
        # IPMI Message: NetFn(1) + Cmd(1) + Data(n)
        rs_addr = 0x20  # Remote Session Address
        rq_addr = 0x81  # Requestor Address
        rq_seq = 0x00   # Requestor Sequence
        
        message = struct.pack('BBBB', rs_addr, netfn, rq_seq, rq_addr)
        message += struct.pack('B', cmd)
        message += data
        
        return message
    
    def calculate_auth_code(self, session_id, sequence, message):
        """Calculate authentication code (simplified)"""
        # In production, implement proper MD5/SHA1 authentication
        # For now, return placeholder
        return b'\x00' * 16
    
    def parse_ipmi_response(self, data):
        """Parse IPMI response message"""
        if len(data) < 20:
            return None
        
        # Parse RMCP header (4 bytes)
        rmcp_version = data[0]
        rmcp_seq = data[2]
        rmcp_class = data[3]
        
        # Parse IPMI session header (20 bytes)
        auth_type = data[4]
        session_id = struct.unpack('<I', data[5:9])[0]
        sequence = struct.unpack('<I', data[9:13])[0]
        
        # Parse IPMI message
        rs_addr = data[20]
        netfn = data[21]
        cmd = data[22]
        completion_code = data[23] if len(data) > 23 else 0
        response_data = data[24:] if len(data) > 24 else b''
        
        return {
            'completion_code': completion_code,
            'netfn': netfn,
            'cmd': cmd,
            'data': response_data,
            'session_id': session_id
        }
    
    def establish_session(self, username, password):
        """Establish IPMI session (simplified)"""
        self.username = username
        self.password = password
        self.session_id = int(time.time()) & 0xFFFFFFFF
        self.session_seq = 1
        self.session_state = self.SESSION_STATE_OPEN
        return True
    
    def send_command(self, netfn, cmd, data=b''):
        """Build IPMI command packet"""
        # Build complete IPMI packet
        rmcp_header = self.create_rmcp_header()
        session_header = self.create_ipmi_session_header(
            self.session_id,
            self.session_seq,
            self.auth_type
        )
        ipmi_message = self.create_ipmi_request(netfn, 0, cmd, data)
        
        # Increment sequence
        self.session_seq += 1
        
        # Combine all parts
        packet = rmcp_header + session_header + ipmi_message
        return packet
    
    def get_device_id(self):
        """Get Device ID command (NetFn 0x06, Cmd 0x01)"""
        return self.send_command(0x06, 0x01)
    
    def get_chassis_status(self):
        """Get Chassis Status command (NetFn 0x00, Cmd 0x01)"""
        return self.send_command(0x00, 0x01)
    
    def chassis_control(self, command):
        """Chassis Control command (NetFn 0x00, Cmd 0x02)"""
        # Command: 0x00=Power Off, 0x01=Power On, 0x02=Power Cycle, 0x03=Hard Reset, 0x05=Soft Shutdown
        return self.send_command(0x00, 0x02, struct.pack('B', command))
    
    def get_system_guid(self):
        """Get System GUID command (NetFn 0x06, Cmd 0x37)"""
        return self.send_command(0x06, 0x37)
    
    def get_sensor_reading(self, sensor_number):
        """Get Sensor Reading command (NetFn 0x04, Cmd 0x2D)"""
        return self.send_command(0x04, 0x2D, struct.pack('B', sensor_number))

