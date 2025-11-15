#!/bin/bash
# Basic OSINT Scan Example
# For educational purposes only

echo "🔍 Starting Basic OSINT Scan - Educational Use Only"
echo "⚠️ Ensure you have proper authorization before scanning!"

# Target domain from command line or default
TARGET=${1:-"example.com"}

echo "📡 Target: $TARGET"
echo ""

# Domain reconnaissance
echo "🌐 Domain Reconnaissance:"
python osint_tool.py -d $TARGET

echo ""
echo "🔎 Subdomain Discovery:"
python osint_tool.py -s $TARGET

# Get IP and do port scan
echo ""
echo "🔌 Network Scanning:"
IP=$(nslookup $TARGET | grep "Address" | tail -1 | awk '{print $2}')
if [ ! -z "$IP" ]; then
    echo "IP Address: $IP"
    python osint_tool.py -i $IP
else
    echo "❌ Could not resolve IP address"
fi

echo ""
echo "📊 Basic scan completed!"
echo "💡 For comprehensive scanning, use: python osint_tool.py -d $TARGET --full-scan"
