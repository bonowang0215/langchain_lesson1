#!/usr/bin/env python3
"""
USB Keyboard Host Application using HIDAPI
Alternative implementation for better Windows compatibility
"""

try:
    import hid
    HIDAPI_AVAILABLE = True
except ImportError:
    HIDAPI_AVAILABLE = False

import time
import sys
from typing import List, Dict, Optional

class USBKeyboardHostHIDAPI:
    def __init__(self):
        self.device = None
        self.keyboard_found = False
        
        # Key mapping for common keys
        self.key_codes = {
            0x04: 'A', 0x05: 'B', 0x06: 'C', 0x07: 'D', 0x08: 'E', 0x09: 'F',
            0x0A: 'G', 0x0B: 'H', 0x0C: 'I', 0x0D: 'J', 0x0E: 'K', 0x0F: 'L',
            0x10: 'M', 0x11: 'N', 0x12: 'O', 0x13: 'P', 0x14: 'Q', 0x15: 'R',
            0x16: 'S', 0x17: 'T', 0x18: 'U', 0x19: 'V', 0x20: 'W', 0x21: 'X',
            0x22: 'Y', 0x23: 'Z', 0x24: '1', 0x25: '2', 0x26: '3', 0x27: '4',
            0x28: '5', 0x29: '6', 0x2A: '7', 0x2B: '8', 0x2C: '9', 0x2D: '0',
            0x2E: 'Enter', 0x2F: 'Esc', 0x30: 'Backspace', 0x31: 'Tab',
            0x32: 'Space', 0x33: '-', 0x34: '=', 0x35: '[', 0x36: ']',
            0x37: '\\', 0x38: ';', 0x39: "'", 0x3A: '`', 0x3B: ',', 0x3C: '.',
            0x3D: '/', 0x3E: 'Caps Lock', 0x3F: 'F1', 0x40: 'F2', 0x41: 'F3',
            0x42: 'F4', 0x43: 'F5', 0x44: 'F6', 0x45: 'F7', 0x46: 'F8',
            0x47: 'F9', 0x48: 'F10', 0x49: 'F11', 0x4A: 'F12', 0x4B: 'Print Screen',
            0x4C: 'Scroll Lock', 0x4D: 'Pause', 0x4E: 'Insert', 0x4F: 'Home',
            0x50: 'Page Up', 0x51: 'Delete', 0x52: 'End', 0x53: 'Page Down',
            0x54: 'Right Arrow', 0x55: 'Left Arrow', 0x56: 'Down Arrow', 0x57: 'Up Arrow',
            0x58: 'Num Lock', 0x59: 'Keypad /', 0x5A: 'Keypad *', 0x5B: 'Keypad -',
            0x5C: 'Keypad +', 0x5D: 'Keypad Enter', 0x5E: 'Keypad 1', 0x5F: 'Keypad 2',
            0x60: 'Keypad 3', 0x61: 'Keypad 4', 0x62: 'Keypad 5', 0x63: 'Keypad 6',
            0x64: 'Keypad 7', 0x65: 'Keypad 8', 0x66: 'Keypad 9', 0x67: 'Keypad 0',
            0x68: 'Keypad .', 0x69: '\\', 0x6A: 'Application', 0x6B: 'Power',
            0x6C: 'Keypad =', 0x6D: 'F13', 0x6E: 'F14', 0x6F: 'F15', 0x70: 'F16',
            0x71: 'F17', 0x72: 'F18', 0x73: 'F19', 0x74: 'F20', 0x75: 'F21',
            0x76: 'F22', 0x77: 'F23', 0x78: 'F24'
        }
        
        # Modifier keys
        self.modifier_keys = {
            0x01: 'Left Ctrl', 0x02: 'Left Shift', 0x04: 'Left Alt', 0x08: 'Left GUI',
            0x10: 'Right Ctrl', 0x20: 'Right Shift', 0x40: 'Right Alt', 0x80: 'Right GUI'
        }

    def find_keyboard_device(self) -> bool:
        """Find and connect to a USB keyboard device using HIDAPI"""
        if not HIDAPI_AVAILABLE:
            print("HIDAPI not available. Installing...")
            print("Run: pip install hidapi")
            return False
            
        print("Searching for USB keyboard devices using HIDAPI...")
        
        try:
            # Enumerate all HID devices
            devices = hid.enumerate()
            
            print(f"Found {len(devices)} HID devices")
            
            # Look for keyboard devices
            for device_info in devices:
                # Check if it's a keyboard (usage page 0x07, usage 0x06) or generic desktop keyboard
                usage_page = device_info.get('usage_page', 0)
                usage = device_info.get('usage', 0)
                product_string = device_info.get('product_string', '').lower()
                
                is_keyboard = (
                    (usage_page == 7 and usage == 6) or  # Standard keyboard
                    (usage_page == 1 and usage == 6) or  # Generic desktop keyboard
                    'keyboard' in product_string or
                    'key' in product_string
                )
                
                if is_keyboard:
                    print(f"Found keyboard: {device_info['manufacturer_string']} {device_info['product_string']}")
                    print(f"  VID: 0x{device_info['vendor_id']:04X}")
                    print(f"  PID: 0x{device_info['product_id']:04X}")
                    print(f"  Path: {device_info['path']}")
                    
                    # Try to open the device
                    try:
                        self.device = hid.device()
                        self.device.open_path(device_info['path'])
                        self.keyboard_found = True
                        print("✓ Keyboard opened successfully")
                        return True
                    except Exception as e:
                        print(f"✗ Failed to open keyboard: {e}")
                        continue
            
            print("No keyboard device found!")
            return False
            
        except Exception as e:
            print(f"Error enumerating devices: {e}")
            return False

    def decode_keyboard_report(self, data: bytes) -> Dict:
        """Decode HID keyboard report data"""
        if len(data) < 8:
            return {"error": "Invalid report length"}
        
        # HID keyboard report format:
        # Byte 0: Modifier keys
        # Byte 1: Reserved
        # Bytes 2-7: Key codes (up to 6 keys)
        
        modifiers = data[0]
        key_codes = data[2:8]
        
        result = {
            "modifiers": [],
            "keys": [],
            "raw_data": [hex(b) for b in data]
        }
        
        # Decode modifier keys
        for bit, key_name in self.modifier_keys.items():
            if modifiers & bit:
                result["modifiers"].append(key_name)
        
        # Decode key codes
        for key_code in key_codes:
            if key_code != 0:  # 0 means no key pressed
                key_name = self.key_codes.get(key_code, f"Unknown(0x{key_code:02X})")
                result["keys"].append(key_name)
        
        return result

    def read_keyboard_reports(self):
        """Main loop to read and display keyboard reports"""
        if not self.keyboard_found:
            print("No keyboard device available")
            return
        
        print("\n=== USB Keyboard Host Started (HIDAPI) ===")
        print("Press keys on your keyboard to see the reports...")
        print("Press Ctrl+C to exit\n")
        
        try:
            while True:
                try:
                    # Read data from HID device
                    data = self.device.read(8, timeout_ms=1000)
                    
                    if data:
                        report = self.decode_keyboard_report(data)
                        
                        # Only display if there are keys pressed or modifiers
                        if report["keys"] or report["modifiers"]:
                            print(f"Raw Data: {report['raw_data']}")
                            if report["modifiers"]:
                                print(f"Modifiers: {', '.join(report['modifiers'])}")
                            if report["keys"]:
                                print(f"Keys: {', '.join(report['keys'])}")
                            print("-" * 40)
                    
                except Exception as e:
                    if "timeout" not in str(e).lower():
                        print(f"Error reading data: {e}")
                    continue
                    
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up HID resources"""
        if self.device:
            try:
                self.device.close()
                print("Device closed")
            except Exception as e:
                print(f"Error closing device: {e}")

def main():
    """Main function"""
    print("USB Keyboard Host Application (HIDAPI)")
    print("=" * 40)
    
    if not HIDAPI_AVAILABLE:
        print("HIDAPI is not installed.")
        print("Please install it with: pip install hidapi")
        return
    
    # Create and run the USB keyboard host
    keyboard_host = USBKeyboardHostHIDAPI()
    
    if keyboard_host.find_keyboard_device():
        keyboard_host.read_keyboard_reports()
    else:
        print("No suitable keyboard device found")
        print("\nTroubleshooting tips:")
        print("1. Make sure a USB keyboard is connected")
        print("2. Try running as administrator (Windows)")
        print("3. Check if the device is already in use by another application")

if __name__ == "__main__":
    main()
