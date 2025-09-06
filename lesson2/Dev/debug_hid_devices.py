#!/usr/bin/env python3
"""
Debug script to list all HID devices
"""

import hid

def list_hid_devices():
    """List all HID devices with detailed information"""
    print("HID Device Debug Information")
    print("=" * 50)
    
    try:
        devices = hid.enumerate()
        print(f"Found {len(devices)} HID devices:\n")
        
        for i, device in enumerate(devices):
            print(f"Device {i+1}:")
            print(f"  Manufacturer: {device.get('manufacturer_string', 'Unknown')}")
            print(f"  Product: {device.get('product_string', 'Unknown')}")
            print(f"  VID: 0x{device.get('vendor_id', 0):04X}")
            print(f"  PID: 0x{device.get('product_id', 0):04X}")
            print(f"  Usage Page: 0x{device.get('usage_page', 0):04X}")
            print(f"  Usage: 0x{device.get('usage', 0):04X}")
            print(f"  Interface Number: {device.get('interface_number', 'Unknown')}")
            print(f"  Path: {device.get('path', 'Unknown')}")
            print(f"  Serial Number: {device.get('serial_number', 'Unknown')}")
            print(f"  Release Number: 0x{device.get('release_number', 0):04X}")
            print(f"  Country Code: {device.get('country_code', 'Unknown')}")
            print()
            
            # Check if it might be a keyboard
            usage_page = device.get('usage_page', 0)
            usage = device.get('usage', 0)
            
            if usage_page == 7:  # Keyboard/Keypad Usage Page
                print(f"  *** This is a keyboard device! (Usage Page 7)")
                if usage == 6:  # Keyboard Usage
                    print(f"  *** Standard keyboard (Usage 6)")
                else:
                    print(f"  *** Keyboard-related device (Usage {usage})")
            elif usage_page == 1:  # Generic Desktop Usage Page
                if usage == 6:  # Keyboard
                    print(f"  *** This might be a keyboard! (Generic Desktop, Usage 6)")
            print("-" * 50)
            
    except Exception as e:
        print(f"Error enumerating devices: {e}")

if __name__ == "__main__":
    list_hid_devices()
