#!/bin/bash
# Termux OSINT Tool Setup Script
# For educational and cybersecurity testing purposes only

echo "
╔══════════════════════════════════════════════════════════════╗
║                TERMUX OSINT TOOL SETUP                      ║
║           For Educational Purposes Only                     ║
╚══════════════════════════════════════════════════════════════╝
"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Ethical warning
echo ""
print_warning "ETHICAL USAGE REMINDER"
echo "This tool is for:"
echo "✅ Educational purposes"
echo "✅ Cybersecurity learning" 
echo "✅ Authorized penetration testing"
echo ""
echo "STRICTLY PROHIBITED:"
echo "❌ Unauthorized scanning"
echo "❌ Illegal activities"
echo "❌ Privacy violations"
echo ""
echo "By continuing, you agree to use this tool ethically and legally."
echo ""

read -p "Do you agree to use this tool only for legal educational purposes? (y/N): " agree

if [[ ! $agree =~ ^[Yy]$ ]]; then
    print_error "Installation cancelled. Tool must only be used for educational purposes."
    exit 1
fi

# Detect platform
detect_platform() {
    if [[ -d /data/data/com.termux/files/usr ]]; then
        echo "termux"
    elif [[ -f /etc/debian_version ]]; then
        echo "debian"
    elif [[ -f /etc/redhat-release ]]; then
        echo "rhel"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

PLATFORM=$(detect_platform)

print_status "Detected platform: $PLATFORM"

# Installation functions
install_termux() {
    print_status "Installing on Termux..."
    pkg update && pkg upgrade -y
    pkg install python python-pip git -y
    pip install --upgrade pip
}

install_debian() {
    print_status "Installing on Debian/Ubuntu..."
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3 python3-pip python3-venv git -y
}

install_linux() {
    print_status "Installing on Linux..."
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install python3 python3-pip git -y
    elif command -v yum &> /dev/null; then
        sudo yum update && sudo yum install python3 python3-pip git -y
    elif command -v dnf &> /dev/null; then
        sudo dnf update && sudo dnf install python3 python3-pip git -y
    elif command -v pacman &> /dev/null; then
        sudo pacman -Syu python python-pip git --noconfirm
    else
        print_error "Unsupported Linux distribution"
        exit 1
    fi
}

install_macos() {
    print_status "Installing on macOS..."
    if command -v brew &> /dev/null; then
        brew update
        brew install python3 git
    else
        print_error "Homebrew not found. Please install Homebrew first."
        exit 1
    fi
}

install_windows() {
    print_status "Installing on Windows..."
    if command -v choco &> /dev/null; then
        choco install python git -y
    elif command -v winget &> /dev/null; then
        winget install Python.Python.3.11 Git.Git
    else
        print_warning "Please install Python and Git manually from:"
        echo "  Python: https://www.python.org/downloads/"
        echo "  Git: https://git-scm.com/download/win"
    fi
}

# Platform-specific installation
case $PLATFORM in
    "termux")
        install_termux
        ;;
    "debian")
        install_debian
        ;;
    "linux")
        install_linux
        ;;
    "macos")
        install_macos
        ;;
    "windows")
        install_windows
        ;;
    *)
        print_error "Unsupported platform: $PLATFORM"
        exit 1
        ;;
esac

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Make scripts executable
chmod +x osint_tool.py advanced_osint.py

# Create examples directory
mkdir -p examples

print_success "Installation completed successfully!"
echo ""
print_status "Usage examples:"
echo "  Basic domain reconnaissance: python osint_tool.py -d example.com"
echo "  IP intelligence: python osint_tool.py -i 8.8.8.8"
echo "  Full scan: python osint_tool.py -d target.com --full-scan -o report.json"
echo "  Advanced features: python advanced_osint.py"
echo ""
print_warning "Remember: Always use this tool ethically and with proper authorization!"
