#!/usr/bin/env python3
"""
Demo script showing USB keyboard host functionality
This demonstrates the concept without requiring a physical USB keyboard
"""

import time
import random

class KeyboardHostDemo:
    def __init__(self):
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
            0x47: 'F9', 0x48: 'F10', 0x49: 'F11', 0x4A: 'F12'
        }
        
        # Modifier keys
        self.modifier_keys = {
            0x01: 'Left Ctrl', 0x02: 'Left Shift', 0x04: 'Left Alt', 0x08: 'Left GUI',
            0x10: 'Right Ctrl', 0x20: 'Right Shift', 0x40: 'Right Alt', 0x80: 'Right GUI'
        }

    def decode_keyboard_report(self, data):
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

    def generate_demo_reports(self):
        """Generate demo keyboard reports to show how the system works"""
        print("USB Keyboard Host Demo")
        print("=" * 40)
        print("This demo shows how USB keyboard reports are decoded.")
        print("In a real scenario, these reports would come from a USB keyboard.\n")
        
        # Demo reports simulating different key presses
        demo_reports = [
            # Single key press: 'H'
            [0x00, 0x00, 0x0B, 0x00, 0x00, 0x00, 0x00, 0x00],
            
            # Shift + 'H' (capital H)
            [0x02, 0x00, 0x0B, 0x00, 0x00, 0x00, 0x00, 0x00],
            
            # Ctrl + 'C'
            [0x01, 0x00, 0x06, 0x00, 0x00, 0x00, 0x00, 0x00],
            
            # Multiple keys: 'H' + 'E' + 'L' + 'L' + 'O'
            [0x00, 0x00, 0x0B, 0x08, 0x0F, 0x0F, 0x12, 0x00],
            
            # Function key F1
            [0x00, 0x00, 0x3F, 0x00, 0x00, 0x00, 0x00, 0x00],
            
            # Arrow key (Right Arrow)
            [0x00, 0x00, 0x4F, 0x00, 0x00, 0x00, 0x00, 0x00],
            
            # No keys pressed (all zeros)
            [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        ]
        
        print("Demo keyboard reports:\n")
        
        for i, report_data in enumerate(demo_reports, 1):
            print(f"Report {i}:")
            decoded = self.decode_keyboard_report(report_data)
            
            print(f"  Raw Data: {decoded['raw_data']}")
            
            if decoded["modifiers"]:
                print(f"  Modifiers: {', '.join(decoded['modifiers'])}")
            
            if decoded["keys"]:
                print(f"  Keys: {', '.join(decoded['keys'])}")
            else:
                print("  Keys: (no keys pressed)")
            
            print("-" * 40)
            time.sleep(1)  # Pause between reports

    def show_installation_instructions(self):
        """Show installation and usage instructions"""
        print("\n" + "=" * 60)
        print("REAL USB KEYBOARD HOST SETUP INSTRUCTIONS")
        print("=" * 60)
        
        print("\n1. INSTALL DEPENDENCIES:")
        print("   pip install hidapi")
        print("   # OR for pyusb version:")
        print("   pip install pyusb libusb1")
        
        print("\n2. CONNECT A USB KEYBOARD:")
        print("   - Connect any USB keyboard to your computer")
        print("   - Make sure it's recognized by the operating system")
        
        print("\n3. RUN THE APPLICATION:")
        print("   # HIDAPI version (recommended for Windows):")
        print("   python usb_keyboard_host_hidapi.py")
        print("   # OR pyusb version:")
        print("   python usb_keyboard_host.py")
        
        print("\n4. TEST THE APPLICATION:")
        print("   - Press keys on the connected keyboard")
        print("   - Watch the decoded reports appear in real-time")
        print("   - Press Ctrl+C to exit")
        
        print("\n5. TROUBLESHOOTING:")
        print("   - If no keyboard found: Try running as administrator")
        print("   - If permission errors: Check USB device permissions")
        print("   - If backend errors: Install libusb drivers")
        
        print("\n6. UNDERSTANDING THE OUTPUT:")
        print("   - Raw Data: The actual bytes received from USB")
        print("   - Modifiers: Ctrl, Shift, Alt, GUI keys")
        print("   - Keys: The actual keys being pressed")
        
        print("\n" + "=" * 60)

def main():
    """Main demo function"""
    demo = KeyboardHostDemo()
    demo.generate_demo_reports()
    demo.show_installation_instructions()

if __name__ == "__main__":
    main()
