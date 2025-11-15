#!/bin/bash
# Advanced OSINT Scan Example
# For cybersecurity education and authorized testing only

echo "🎯 Starting Advanced OSINT Scan - Educational Use Only"
echo "🚨 ONLY USE WITH PROPER AUTHORIZATION!"

TARGET=${1:-"example.com"}
OUTPUT_FILE="osint_scan_$(date +%Y%m%d_%H%M%S).json"

echo "🎯 Target: $TARGET"
echo "💾 Output: $OUTPUT_FILE"
echo ""

# Comprehensive scan
echo "🚀 Starting Comprehensive OSINT Analysis..."
python osint_tool.py -d $TARGET --full-scan -o $OUTPUT_FILE

echo ""
echo "🔧 Running Advanced Analysis..."
python advanced_osint.py

echo ""
echo "📈 Generating Report..."
if [ -f "$OUTPUT_FILE" ]; then
    echo "✅ Scan completed successfully!"
    echo "📁 Results saved to: $OUTPUT_FILE"
    
    # Show scan summary
    echo ""
    echo "📊 Scan Summary:"
    python -c "
import json
try:
    with open('$OUTPUT_FILE', 'r') as f:
        data = json.load(f)
    print('Scanned targets:')
    for key in data:
        print(f'  - {key}: {data[key]}')
except Exception as e:
    print('Error reading results:', e)
"
else
    echo "❌ Scan completed but output file not found"
fi

echo ""
echo "🎓 Educational scan completed!"
echo "⚠️ Remember: This tool is for learning and authorized testing only!"
