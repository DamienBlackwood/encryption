#!/bin/bash

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Detect the operating system
OS=$(uname -s)

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Homebrew on macOS
install_homebrew() {
    if ! command_exists brew; then
        echo -e "${YELLOW}Installing Homebrew...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH
        if [[ "$OS" == "Darwin" ]]; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
    fi
}

# Function to install Python
install_python() {
    case "$OS" in
        "Darwin")
            if ! command_exists python3; then
                echo -e "${YELLOW}Installing Python via Homebrew...${NC}"
                brew install python
            fi
            ;;
        "Linux")
            if ! command_exists python3; then
                echo -e "${YELLOW}Installing Python...${NC}"
                sudo apt-get update
                sudo apt-get install -y python3 python3-pip
            fi
            ;;
        MINGW*|CYGWIN*|MSYS*)
            echo -e "${RED}Please download Python from https://www.python.org/downloads/windows/${NC}"
            exit 1
            ;;
        *)
            echo -e "${RED}Unsupported operating system${NC}"
            exit 1
            ;;
    esac
}

# Function to create and activate virtual environment
setup_virtual_env() {
    if [ ! -d "encryption_env" ]; then
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv encryption_env
    fi

    # Activate virtual environment
    source encryption_env/bin/activate
}

# Function to install dependencies
install_dependencies() {
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install --upgrade pip
    pip install cryptography tkinter pyinstaller
}

# Function to create standalone app
create_standalone_app() {
    echo -e "${YELLOW}Creating standalone application...${NC}"
    pyinstaller --onefile --windowed --name "GoatEncryption" "Advanceder Encryption.py"
    echo -e "${GREEN}Standalone app created in 'dist' directory${NC}"
}

# Function to run the application
run_app() {
    echo -e "${GREEN}Launching Encryption Tool...${NC}"
    python3 "Advanceder Encryption.py"
}

# Main script
main() {
    echo -e "${GREEN}🔒 The Goat's Encryption Tool - Setup Script 🔒${NC}"

    # Detect OS and install prerequisites
    case "$OS" in
        "Darwin")
            install_homebrew
            install_python
            ;;
        "Linux")
            install_python
            ;;
        MINGW*|CYGWIN*|MSYS*)
            echo -e "${RED}Please run this script in Windows Subsystem for Linux (WSL)${NC}"
            exit 1
            ;;
        *)
            echo -e "${RED}Unsupported operating system${NC}"
            exit 1
            ;;
    esac

    # Setup virtual environment and install dependencies
    setup_virtual_env
    install_dependencies

    # Prompt user for action
    echo -e "\n${YELLOW}Choose an option:${NC}"
    echo "1. Run Encryption Tool"
    echo "2. Create Standalone App"
    echo "3. Exit"
    read -p "Enter your choice (1-3): " choice

    case $choice in
        1)
            run_app
            ;;
        2)
            create_standalone_app
            ;;
        3)
            echo -e "${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Exiting.${NC}"
            exit 1
            ;;
    esac
}

# Run the main function
main 