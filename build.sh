#!/bin/bash
# build.sh - Build script for iRackPilot firmware

set -e

MODEL=${1:-"pico-w"}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="${SCRIPT_DIR}/build"
FIRMWARE_DIR="${SCRIPT_DIR}/${MODEL}"

echo "========================================="
echo "iRackPilot Firmware Build Script"
echo "========================================="
echo "Model: ${MODEL}"
echo ""

# Validate model
if [ ! -d "$FIRMWARE_DIR" ]; then
    echo "Error: Firmware directory '${FIRMWARE_DIR}' not found"
    echo "Available models: pico-w, pico-2-w"
    exit 1
fi

# Create output directory
mkdir -p "${OUTPUT_DIR}"

echo "Building firmware for ${MODEL}..."
echo ""

# For MicroPython-based firmware, create a package
if [ "$MODEL" = "pico-w" ] || [ "$MODEL" = "pico-2-w" ]; then
    echo "Creating firmware package..."
    
    # Create archive of Python files
    PACKAGE_NAME="irackpilot_${MODEL}_v1.0.0"
    PACKAGE_DIR="${OUTPUT_DIR}/${PACKAGE_NAME}"
    
    mkdir -p "${PACKAGE_DIR}"
    
    # Copy firmware files
    cp "${FIRMWARE_DIR}"/*.py "${PACKAGE_DIR}/" 2>/dev/null || true
    
    # Create README
    cat > "${PACKAGE_DIR}/README.txt" << EOF
iRackPilot Firmware for ${MODEL}
Version 1.0.0

INSTALLATION:
1. Flash MicroPython to your Pico:
   - Download from: https://micropython.org/download/rp2-pico-w/
   - Hold BOOTSEL, connect USB, copy .uf2 to RPI-RP2 drive

2. Upload these files to your Pico:
   - Use Thonny: File > Save As > Raspberry Pi Pico
   - Or use rshell/ampy

3. Configure WiFi in main.py:
   - Edit WIFI_SSID and WIFI_PASSWORD

4. Restart Pico and check serial output for IP address

FILES:
$(ls -1 "${PACKAGE_DIR}"/*.py 2>/dev/null | xargs -n1 basename)

For more information, see BUILD_UF2.md
EOF
    
    # Create zip archive
    cd "${OUTPUT_DIR}"
    zip -r "${PACKAGE_NAME}.zip" "${PACKAGE_NAME}" > /dev/null
    
    echo "✓ Created package: ${OUTPUT_DIR}/${PACKAGE_NAME}.zip"
    echo ""
    echo "Next steps:"
    echo "1. Flash MicroPython .uf2 to your Pico"
    echo "2. Extract and upload Python files from the package"
    echo "3. Configure WiFi in main.py"
    echo ""
    
else
    echo "Building C/C++ firmware..."
    # Add C/C++ build commands here if needed
    echo "C/C++ build not yet implemented"
fi

echo "Build complete!"
echo "Output directory: ${OUTPUT_DIR}"

