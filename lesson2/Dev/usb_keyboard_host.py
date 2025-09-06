#!/usr/bin/env python3
"""
USB Keyboard Host Application
Receives and decodes HID keyboard reports from USB keyboards
"""

import usb.core
import usb.util
import usb.backend.libusb1
import usb.backend.libusb0
import time
import sys
from typing import List, Dict, Optional

class USBKeyboardHost:
    def __init__(self):
        self.device = None
        self.endpoint = None
        self.interface = None
        self.keyboard_found = False
        
        # USB HID keyboard report descriptor constants
        self.KEYBOARD_USAGE_PAGE = 0x07  # Keyboard/Keypad Usage Page
        self.KEYBOARD_USAGE = 0x06       # Keyboard Usage
        
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
        """Find and connect to a USB keyboard device"""
        print("Searching for USB keyboard devices...")
        
        # Try different backends
        backends = [
            usb.backend.libusb1.get_backend(),
            usb.backend.libusb0.get_backend(),
            None  # Try without explicit backend
        ]
        
        devices = None
        backend_used = None
        
        for backend in backends:
            try:
                if backend:
                    print(f"Trying backend: {backend}")
                    devices = usb.core.find(find_all=True, backend=backend)
                else:
                    print("Trying default backend...")
                    devices = usb.core.find(find_all=True)
                
                # Test if we can actually enumerate devices
                device_list = list(devices)
                print(f"Found {len(device_list)} USB devices")
                backend_used = backend
                break
                
            except Exception as e:
                print(f"Backend failed: {e}")
                continue
        
        if devices is None:
            print("No working USB backend found!")
            print("\nTroubleshooting:")
            print("1. Install libusb drivers: pip install libusb1")
            print("2. On Windows, you may need to install libusb-win32 drivers")
            print("3. Try running as administrator")
            return False
        
        for device in devices:
            try:
                # Get device descriptor
                if device.idVendor and device.idProduct:
                    print(f"Found device: VID={device.idVendor:04X}, PID={device.idProduct:04X}")
                    
                    # Check if it's a HID device
                    if device.bDeviceClass == 0 or device.bDeviceClass == 0xFF:  # HID or vendor specific
                        # Try to get configuration
                        try:
                            device.set_configuration()
                            cfg = device.get_active_configuration()
                            
                            # Look for HID interface
                            for interface in cfg:
                                if interface.bInterfaceClass == 3:  # HID class
                                    print(f"Found HID interface: Interface {interface.bInterfaceNumber}")
                                    
                                    # Look for interrupt endpoint
                                    for endpoint in interface:
                                        if endpoint.bmAttributes & 0x03 == 0x03:  # Interrupt endpoint
                                            print(f"Found interrupt endpoint: {endpoint.bEndpointAddress}")
                                            self.device = device
                                            self.interface = interface
                                            self.endpoint = endpoint
                                            self.keyboard_found = True
                                            return True
                        except usb.core.USBError as e:
                            print(f"Error accessing device: {e}")
                            continue
                            
            except usb.core.USBError as e:
                print(f"Error with device: {e}")
                continue
        
        print("No keyboard device found!")
        return False

    def claim_interface(self) -> bool:
        """Claim the keyboard interface"""
        if not self.device or not self.interface:
            return False
            
        try:
            # Detach kernel driver if attached
            if self.device.is_kernel_driver_active(self.interface.bInterfaceNumber):
                self.device.detach_kernel_driver(self.interface.bInterfaceNumber)
                print("Detached kernel driver")
            
            # Claim the interface
            usb.util.claim_interface(self.device, self.interface.bInterfaceNumber)
            print("Interface claimed successfully")
            return True
            
        except usb.core.USBError as e:
            print(f"Error claiming interface: {e}")
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
        
        print("\n=== USB Keyboard Host Started ===")
        print("Press keys on your keyboard to see the reports...")
        print("Press Ctrl+C to exit\n")
        
        try:
            while True:
                try:
                    # Read data from interrupt endpoint
                    data = self.device.read(self.endpoint.bEndpointAddress, 8, timeout=1000)
                    
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
                    
                except usb.core.USBTimeoutError:
                    # Timeout is normal when no data is available
                    continue
                except usb.core.USBError as e:
                    print(f"USB Error: {e}")
                    break
                    
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up USB resources"""
        if self.device and self.interface:
            try:
                usb.util.release_interface(self.device, self.interface.bInterfaceNumber)
                print("Interface released")
            except usb.core.USBError as e:
                print(f"Error releasing interface: {e}")

def main():
    """Main function"""
    print("USB Keyboard Host Application")
    print("=" * 40)
    
    # Check if running as administrator (required for USB access on Windows)
    try:
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("WARNING: This application may need administrator privileges to access USB devices.")
            print("If you encounter permission errors, try running as administrator.")
    except:
        pass  # Not on Windows or admin check failed
    
    # Create and run the USB keyboard host
    keyboard_host = USBKeyboardHost()
    
    if keyboard_host.find_keyboard_device():
        if keyboard_host.claim_interface():
            keyboard_host.read_keyboard_reports()
        else:
            print("Failed to claim keyboard interface")
    else:
        print("No suitable keyboard device found")
        print("\nTroubleshooting tips:")
        print("1. Make sure a USB keyboard is connected")
        print("2. Try running as administrator (Windows)")
        print("3. Check if the device is already in use by another application")

if __name__ == "__main__":
    main()


