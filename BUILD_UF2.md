# Building UF2 Files for iRackPilot Firmware

This guide explains how to create UF2 firmware files for Raspberry Pi Pico W and Pico 2 W.

## What is a UF2 File?

UF2 (USB Flashing Format) is a file format developed by Microsoft for flashing firmware to microcontrollers. It's designed to be simple and safe, with built-in error checking.

## Method 1: Using MicroPython (Recommended for Development)

MicroPython firmware already comes as a UF2 file. You just need to:
1. Flash MicroPython to your Pico
2. Copy your Python files to the Pico

### Steps:

1. **Download MicroPython UF2**
   - Pico W: https://micropython.org/download/rp2-pico-w/
   - Pico 2 W: https://micropython.org/download/rp2-pico-w/ (check for Pico 2 W version)

2. **Flash MicroPython**
   - Hold BOOTSEL button
   - Connect USB
   - Copy `.uf2` file to RPI-RP2 drive

3. **Upload Your Code**
   - Use Thonny, rshell, or ampy to upload your Python files
   - Files: `boot.py`, `main.py`, `http_server.py`, `ipmi_client.py`, `ipmi_protocol.py`, `script_engine.py`

## Method 2: Creating Custom UF2 from Binary

If you're building C/C++ firmware, you need to convert the binary to UF2 format.

### Prerequisites

```bash
# Install Python 3
# Install uf2conv tool
pip install uf2conv
```

### Using uf2conv

```bash
# Convert binary to UF2
uf2conv firmware.bin -o firmware.uf2 -f 0xe48bff56

# For Pico W
uf2conv firmware.bin -o pico_w_firmware.uf2 -f 0xe48bff56

# For Pico 2 W  
uf2conv firmware.bin -o pico_2_w_firmware.uf2 -f 0xe48bff56
```

### UF2 Family IDs

- **Pico W**: `0xe48bff56` (RP2040)
- **Pico 2 W**: `0xe48bff56` (RP2040 - same as Pico W)

## Method 3: Building with Raspberry Pi Pico SDK

For C/C++ firmware development:

### Setup SDK

```bash
# Clone Pico SDK
git clone https://github.com/raspberrypi/pico-sdk.git
cd pico-sdk
git submodule update --init

# Set environment variable
export PICO_SDK_PATH=/path/to/pico-sdk
```

### Build Firmware

```bash
# Create build directory
mkdir build
cd build

# Configure with CMake
cmake ..

# Build
make

# Output will be firmware.uf2 in build directory
```

### CMakeLists.txt Example

```cmake
cmake_minimum_required(VERSION 3.13)
include(pico_sdk_import.cmake)

project(iRackPilot)

pico_sdk_init()

add_executable(iRackPilot
    main.c
    http_server.c
    ipmi_client.c
)

target_link_libraries(iRackPilot pico_stdlib pico_wireless)

pico_enable_stdio_usb(iRackPilot 1)
pico_enable_stdio_uart(iRackPilot 1)

pico_add_extra_outputs(iRackPilot)
```

## Method 4: Creating UF2 with Python Script

Here's a Python script to create UF2 files:

```python
#!/usr/bin/env python3
"""
UF2 File Creator for iRackPilot Firmware
Converts binary files to UF2 format
"""

import struct
import sys

UF2_MAGIC_START0 = 0x0A324655  # "UF2\n"
UF2_MAGIC_START1 = 0x9E5D5157  # Random number
UF2_MAGIC_END = 0x0AB16F30     # "UF2\n" reversed

FAMILY_ID_RP2040 = 0xe48bff56

def create_uf2(data, family_id=FAMILY_ID_RP2040):
    """Convert binary data to UF2 format"""
    num_blocks = (len(data) + 255) // 256
    uf2_data = b''
    
    for block_num in range(num_blocks):
        block_data = data[block_num * 256:(block_num + 1) * 256]
        block_data = block_data.ljust(256, b'\x00')
        
        # UF2 Block Header (32 bytes)
        header = struct.pack('<IIIIIIII',
            UF2_MAGIC_START0,      # Magic Start 0
            UF2_MAGIC_START1,      # Magic Start 1
            0x00002000,            # Flags
            block_num * 256,       # Target Address
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

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 create_uf2.py <input.bin> <output.uf2>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Read input binary
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Create UF2
    uf2_data = create_uf2(data)
    
    # Write output
    with open(output_file, 'wb') as f:
        f.write(uf2_data)
    
    print(f"Created {output_file} ({len(uf2_data)} bytes)")
```

## Method 5: Automated Build Script

Create a build script to automate the process:

```bash
#!/bin/bash
# build_uf2.sh - Build UF2 firmware for iRackPilot

set -e

MODEL=${1:-"pico-w"}
OUTPUT_DIR="build"
FIRMWARE_NAME="irackpilot_${MODEL}"

echo "Building UF2 firmware for ${MODEL}..."

# Create output directory
mkdir -p ${OUTPUT_DIR}

# For MicroPython-based firmware
if [ "$MODEL" = "pico-w" ] || [ "$MODEL" = "pico-2-w" ]; then
    echo "Note: MicroPython firmware requires manual file upload"
    echo "1. Flash MicroPython .uf2 to your Pico"
    echo "2. Upload Python files using Thonny or rshell"
    echo ""
    echo "Files to upload:"
    ls -1 ${MODEL}/*.py
else
    echo "Building C/C++ firmware..."
    # Add your build commands here
fi

echo "Build complete!"
```

## Method 6: Using GitHub Actions (CI/CD)

Create `.github/workflows/build-firmware.yml`:

```yaml
name: Build Firmware

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install uf2conv
      
      - name: Build Pico W firmware
        run: |
          # Your build commands here
          # uf2conv firmware.bin -o pico_w_firmware.uf2 -f 0xe48bff56
      
      - name: Build Pico 2 W firmware
        run: |
          # Your build commands here
          # uf2conv firmware.bin -o pico_2_w_firmware.uf2 -f 0xe48bff56
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: firmware
          path: |
            *.uf2
```

## Verification

After creating a UF2 file, verify it:

```bash
# Check file size (should be multiple of 512 bytes)
ls -lh firmware.uf2

# Verify UF2 magic numbers
hexdump -C firmware.uf2 | head -n 5

# Should see:
# 00000000  55 46 32 0a 57 51 5d 9e  00 20 00 00 00 00 00 00  |UF2.WQ].. ......|
```

## Flashing UF2 Files

1. **Hold BOOTSEL button** on your Pico
2. **Connect USB cable** while holding BOOTSEL
3. **Release BOOTSEL** - RPI-RP2 drive should appear
4. **Copy UF2 file** to the RPI-RP2 drive
5. **Pico reboots** automatically with new firmware

## Troubleshooting

### UF2 File Not Recognized
- Verify file size is multiple of 512 bytes
- Check UF2 magic numbers with hexdump
- Ensure correct family ID for your Pico model

### Build Errors
- Verify SDK is properly installed
- Check CMake configuration
- Ensure all dependencies are installed

### Flashing Fails
- Try different USB cable (must be data-capable)
- Try different USB port
- Hold BOOTSEL longer before connecting
- Check Pico is in bootloader mode (RPI-RP2 drive visible)

## Resources

- [UF2 Specification](https://github.com/microsoft/uf2)
- [Raspberry Pi Pico SDK](https://github.com/raspberrypi/pico-sdk)
- [MicroPython for Pico](https://micropython.org/download/rp2-pico-w/)
- [uf2conv Tool](https://github.com/microsoft/uf2)

## Quick Reference

```bash
# Convert binary to UF2
uf2conv input.bin -o output.uf2 -f 0xe48bff56

# Flash to Pico
# 1. Hold BOOTSEL
# 2. Connect USB
# 3. Copy output.uf2 to RPI-RP2 drive
```

