#!/usr/bin/env python3
"""
UF2 File Creator for iRackPilot Firmware
Converts binary files to UF2 format for Raspberry Pi Pico
"""

import struct
import sys
import os

# UF2 Magic Numbers
UF2_MAGIC_START0 = 0x0A324655  # "UF2\n"
UF2_MAGIC_START1 = 0x9E5D5157  # Random number
UF2_MAGIC_END = 0x0AB16F30     # "UF2\n" reversed

# Family IDs
FAMILY_ID_RP2040 = 0xe48bff56  # Raspberry Pi Pico W and Pico 2 W

def create_uf2(data, family_id=FAMILY_ID_RP2040, base_address=0x10000000):
    """
    Convert binary data to UF2 format
    
    Args:
        data: Binary data to convert
        family_id: UF2 family ID (default: RP2040)
        base_address: Base address in flash memory
    
    Returns:
        UF2 formatted binary data
    """
    num_blocks = (len(data) + 255) // 256
    uf2_data = b''
    
    for block_num in range(num_blocks):
        block_data = data[block_num * 256:(block_num + 1) * 256]
        block_data = block_data.ljust(256, b'\x00')
        
        # Calculate target address
        target_addr = base_address + (block_num * 256)
        
        # UF2 Block Header (32 bytes)
        header = struct.pack('<IIIIIIII',
            UF2_MAGIC_START0,      # Magic Start 0
            UF2_MAGIC_START1,      # Magic Start 1
            0x00002000,            # Flags (file container)
            target_addr,           # Target Address
            256,                   # Payload Size
            block_num,             # Block Number
            num_blocks,            # Total Blocks
            family_id              # Family ID
        )
        
        # Block Data (256 bytes)
        # Magic End (4 bytes)
        footer = struct.pack('<I', UF2_MAGIC_END)
        
        uf2_data += header + block_data + footer
    
    return uf2_data

def verify_uf2(filename):
    """Verify a UF2 file is valid"""
    with open(filename, 'rb') as f:
        data = f.read()
    
    if len(data) % 512 != 0:
        return False, "File size must be multiple of 512 bytes"
    
    num_blocks = len(data) // 512
    
    for i in range(num_blocks):
        block = data[i * 512:(i + 1) * 512]
        
        # Check magic numbers
        magic0 = struct.unpack('<I', block[0:4])[0]
        magic1 = struct.unpack('<I', block[4:8])[0]
        magic_end = struct.unpack('<I', block[508:512])[0]
        
        if magic0 != UF2_MAGIC_START0:
            return False, f"Invalid magic start0 in block {i}"
        if magic1 != UF2_MAGIC_START1:
            return False, f"Invalid magic start1 in block {i}"
        if magic_end != UF2_MAGIC_END:
            return False, f"Invalid magic end in block {i}"
    
    return True, "UF2 file is valid"

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 create_uf2.py <input.bin> <output.uf2> [family_id] [base_address]")
        print("\nFamily IDs:")
        print(f"  RP2040 (Pico W/Pico 2 W): 0x{FAMILY_ID_RP2040:08x}")
        print("\nExample:")
        print("  python3 create_uf2.py firmware.bin firmware.uf2")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Parse optional arguments
    family_id = FAMILY_ID_RP2040
    base_address = 0x10000000
    
    if len(sys.argv) > 3:
        family_id = int(sys.argv[3], 0)  # Allow hex (0x...) or decimal
    
    if len(sys.argv) > 4:
        base_address = int(sys.argv[4], 0)
    
    # Check input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    # Read input binary
    print(f"Reading {input_file}...")
    with open(input_file, 'rb') as f:
        data = f.read()
    
    print(f"Input size: {len(data)} bytes")
    
    # Create UF2
    print(f"Creating UF2 file (family_id=0x{family_id:08x}, base=0x{base_address:08x})...")
    uf2_data = create_uf2(data, family_id, base_address)
    
    # Write output
    print(f"Writing {output_file}...")
    with open(output_file, 'wb') as f:
        f.write(uf2_data)
    
    print(f"Created {output_file} ({len(uf2_data)} bytes, {len(uf2_data) // 512} blocks)")
    
    # Verify
    print("Verifying UF2 file...")
    valid, message = verify_uf2(output_file)
    if valid:
        print("✓ UF2 file is valid")
    else:
        print(f"✗ Verification failed: {message}")
        sys.exit(1)

if __name__ == '__main__':
    main()

