# Termux OSINT Tool - Cybersecurity Education Platform

![OSINT Tool](https://img.shields.io/badge/Platform-Multi--platform-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Purpose](https://img.shields.io/badge/Purpose-Education%20%26%20Cybersecurity-orange)

A comprehensive Open Source Intelligence (OSINT) tool designed for cybersecurity education, ethical hacking practice, and authorized penetration testing. This tool helps security professionals and students learn about information gathering techniques in a legal and ethical manner.

## ⚠️ CRITICAL LEGAL DISCLAIMER

**THIS TOOL IS STRICTLY FOR EDUCATIONAL PURPOSES AND AUTHORIZED SECURITY TESTING ONLY.**

### ✅ Permitted Uses:
- Cybersecurity education and learning
- Authorized penetration testing with written permission
- Security research on your own systems
- Academic projects and coursework
- CTF (Capture The Flag) competitions

### ❌ Strictly Prohibited:
- Unauthorized scanning of systems you don't own
- Illegal activities or privacy violations
- Malicious attacks or intrusions
- Violating terms of service
- Any activities that break local laws

**By using this tool, you agree to use it ethically and legally. The developers are NOT responsible for any misuse.**

## 🚀 Features

### Core OSINT Capabilities
- **🌐 Domain Reconnaissance** - DNS records, IP resolution, WHOIS data
- **🔍 Subdomain Discovery** - Common subdomain enumeration
- **📍 IP Intelligence** - Geolocation and network information
- **🔌 Port Scanning** - Common service port detection
- **🔒 Website Forensics** - Security headers and server analysis
- **👤 Digital Footprint** - Username presence across platforms

### Advanced Features
- **📧 Email Intelligence** - Email format generation
- **🛠️ Technology Detection** - CMS and framework identification
- **📄 Metadata Analysis** - Web resource metadata extraction
- **🛡️ Security Headers Audit** - Comprehensive security assessment

## 📋 Supported Platforms

The tool is tested on:
- ✅ Termux (Android)
- ✅ Linux (Debian, Ubuntu, Kali)
- ✅ Windows (WSL2 recommended)
- ✅ macOS
- ✅ Other Unix-like systems

## 🛠️ Installation

### Termux (Android)
```bash
# Update packages
pkg update && pkg upgrade

# Install dependencies
pkg install python git

# Clone repository
git clone https://github.com/Yash-coder53/OSINT.git
cd OSINT

# Run setup script
chmod +x setup.sh
./setup.sh

# Install system dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y

# Clone repository
git clone https://github.com/Yash-coder53/OSINT.git
cd OSINT

# Run setup
chmod +x setup.sh
./setup.sh

# For RHEL/CentOS/Fedora
sudo dnf update && sudo dnf install python3 python3-pip git -y

# For Arch Linux
sudo pacman -Syu python python-pip git

# Then clone and setup
git clone https://github.com/Yash-coder53/OSINT.git
cd OSINT
chmod +x setup.sh
./setup.sh
# Clone and setup
git clone https://github.com/yourusername/termux-osint
