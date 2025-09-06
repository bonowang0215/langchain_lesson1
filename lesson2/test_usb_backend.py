#!/usr/bin/env python3
"""
Test script to check USB backend availability
"""

import usb.core
import usb.backend.libusb1
import usb.backend.libusb0

def test_backends():
    """Test available USB backends"""
    print("Testing USB backends...")
    
    # Test libusb1 backend
    try:
        backend1 = usb.backend.libusb1.get_backend()
        if backend1:
            print("✓ libusb1 backend is available")
        else:
            print("✗ libusb1 backend not found")
    except Exception as e:
        print(f"✗ libusb1 backend error: {e}")
    
    # Test libusb0 backend
    try:
        backend0 = usb.backend.libusb0.get_backend()
        if backend0:
            print("✓ libusb0 backend is available")
        else:
            print("✗ libusb0 backend not found")
    except Exception as e:
        print(f"✗ libusb0 backend error: {e}")
    
    # Test with explicit backend
    try:
        backend = usb.backend.libusb1.get_backend()
        devices = usb.core.find(find_all=True, backend=backend)
        device_count = len(list(devices))
        print(f"✓ Found {device_count} USB devices with libusb1 backend")
    except Exception as e:
        print(f"✗ Error with libusb1 backend: {e}")
    
    # Test without explicit backend
    try:
        devices = usb.core.find(find_all=True)
        device_count = len(list(devices))
        print(f"✓ Found {device_count} USB devices without explicit backend")
    except Exception as e:
        print(f"✗ Error without explicit backend: {e}")

if __name__ == "__main__":
    test_backends()
