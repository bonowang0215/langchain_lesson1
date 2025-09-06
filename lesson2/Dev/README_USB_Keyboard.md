# USB Keyboard Host Application

This application creates a USB host that can receive and decode HID keyboard reports from USB keyboards.

## Features

- **USB Device Detection**: Automatically finds and connects to USB keyboard devices
- **HID Report Decoding**: Decodes raw HID keyboard reports into readable key presses
- **Real-time Monitoring**: Displays keyboard input in real-time
- **Modifier Key Support**: Recognizes Ctrl, Shift, Alt, and GUI keys
- **Cross-platform**: Works on Windows, Linux, and macOS

## Requirements

- Python 3.6 or higher
- USB keyboard connected to the computer
- Administrator/root privileges (for USB access)

## Installation

### Method 1: Automatic Installation
```bash
python install_dependencies.py
```

### Method 2: Manual Installation
```bash
pip install pyusb>=1.2.1
```

### Platform-specific Requirements

#### Windows
- Install libusb drivers from https://libusb.info/
- Or install via: `pip install libusb1`
- Run as administrator

#### Linux
- Install system packages: `sudo apt-get install python3-usb`
- Or run with sudo: `sudo python usb_keyboard_host.py`
- May need to add udev rules for USB access

#### macOS
- Install via Homebrew: `brew install libusb`
- Or install via pip: `pip install pyusb`

## Usage

1. **Connect a USB keyboard** to your computer
2. **Run the application**:
   ```bash
   python usb_keyboard_host.py
   ```
3. **Press keys** on the keyboard to see the decoded reports
4. **Press Ctrl+C** to exit

## Example Output

```
USB Keyboard Host Application
========================================
Searching for USB keyboard devices...
Found device: VID=046D, PID=C31C
Found HID interface: Interface 0
Found interrupt endpoint: 130
Detached kernel driver
Interface claimed successfully

=== USB Keyboard Host Started ===
Press keys on your keyboard to see the reports...
Press Ctrl+C to exit

Raw Data: ['0x0', '0x0', '0x4', '0x0', '0x0', '0x0', '0x0', '0x0']
Keys: A
----------------------------------------
Raw Data: ['0x2', '0x0', '0x4', '0x0', '0x0', '0x0', '0x0', '0x0']
Modifiers: Left Shift
Keys: A
----------------------------------------
```

## How It Works

### USB HID Protocol
The application communicates with USB keyboards using the Human Interface Device (HID) protocol:

1. **Device Discovery**: Scans for USB devices with HID class interfaces
2. **Interface Claiming**: Claims the keyboard's HID interface
3. **Report Reading**: Reads interrupt endpoint data containing keyboard reports
4. **Report Decoding**: Decodes raw bytes into key presses and modifier states

### HID Keyboard Report Format
```
Byte 0: Modifier keys (bitfield)
Byte 1: Reserved
Bytes 2-7: Key codes (up to 6 simultaneous keys)
```

### Key Mapping
The application includes mappings for:
- **Alphanumeric keys**: A-Z, 0-9
- **Function keys**: F1-F24
- **Special keys**: Enter, Space, Tab, etc.
- **Arrow keys**: Up, Down, Left, Right
- **Modifier keys**: Ctrl, Shift, Alt, GUI (Windows/Cmd)

## Troubleshooting

### "No keyboard device found"
- Ensure a USB keyboard is connected
- Try running as administrator/root
- Check if another application is using the keyboard

### "Permission denied" or "Access denied"
- Run as administrator (Windows) or with sudo (Linux)
- Check USB device permissions
- Install proper USB drivers

### "Interface claim failed"
- Disconnect and reconnect the keyboard
- Close other applications that might be using the keyboard
- Try a different USB port

### "USB Error" messages
- Check USB cable connection
- Try a different keyboard
- Restart the application

## Technical Details

### Supported Keyboards
- Any USB HID-compliant keyboard
- Wired and wireless USB keyboards
- Gaming keyboards with additional features

### Report Rate
- Typically 125 Hz (8ms intervals)
- Varies by keyboard manufacturer
- Can be configured in some keyboards

### Simultaneous Keys
- Standard HID keyboards support up to 6 simultaneous keys
- Modifier keys don't count toward the 6-key limit
- Some gaming keyboards support more keys

## Development

### Adding New Key Mappings
Edit the `key_codes` dictionary in `USBKeyboardHost.__init__()` to add support for additional keys.

### Customizing Report Processing
Modify the `decode_keyboard_report()` method to change how reports are processed and displayed.

### Adding Features
- Key combination detection
- Key press duration tracking
- Custom key mapping
- Data logging to file
- Network transmission of key data

## Security Note

This application can capture all keyboard input. Use responsibly and ensure you have proper authorization before monitoring keyboard input on systems you don't own.

