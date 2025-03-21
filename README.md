# The Goat's Encryption Tool

## Overview
This is an advanced encryption application with two encryption methods - an advanced method that's overkill for most users and a parent encryption method created just for fun.

## Quick Start 🚀

### Windows
1. Double-click `setup.bat`
2. Choose from the menu:
   - Run the Encryption Tool
   - Create a Standalone App
   - Exit

### macOS/Linux
1. Open Terminal
2. Run the setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
3. Choose from the menu:
   - Run the Encryption Tool
   - Create a Standalone App
   - Exit

## Prerequisites
Before running the application, ensure you have the following:

### Windows
- **Python 3.8+**
  - Download from [Python's Official Website](https://www.python.org/downloads/windows/)
  - **IMPORTANT**: Check "Add Python to PATH" during installation

### macOS
- **Homebrew** (recommended)
  - Install from [Homebrew's Website](https://brew.sh/)
- **Python 3.8+**
  ```bash
  brew install python
  ```

## Manual Installation (Alternative Method)

### Dependencies
Install required Python packages:

#### Windows
```powershell
pip install cryptography tkinter
```

#### macOS
```bash
# Create a virtual environment (recommended)
python3 -m venv encryption_env
source encryption_env/bin/activate

# Install dependencies
pip install cryptography tkinter
```

## Running the Application Manually

### Windows
1. **Method 1: Double-Click**
   - Simply double-click the `Advanceder Encryption.py` file
   - If prompted, choose to run with Python

2. **Method 2: Command Prompt**
   ```powershell
   python "Advanceder Encryption.py"
   ```

### macOS
1. **Method 1: Terminal**
   ```bash
   # Activate virtual environment
   source encryption_env/bin/activate

   # Run the application
   python3 "Advanceder Encryption.py"
   ```

## Troubleshooting

### Common Issues
- **Missing Dependencies**: Ensure all required packages are installed
- **Python Not in PATH**: Verify Python installation and system PATH
- **Permission Errors**: Run as administrator (Windows) or with `sudo` (macOS)

### Encryption Notes
- Files are saved with `.jonsnow` extension
- Use a strong, memorable passphrase because its important
- Keep your passphrase secret please

## Security Features
- Advanced key derivation (PBKDF2HMAC)
- Secure random salt generation
- Metadata encryption
- Secure memory clearing

## Disclaimer
This is a personal encryption tool so please that I just made for funsies so please, if it its anything serious consider upgrading this or using another method!

## License
MIT License

## Contributing
Feel free to fork and improve the project!
