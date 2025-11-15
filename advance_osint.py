#!/usr/bin/env python3
"""
Advanced OSINT Features for Cybersecurity Education
ONLY FOR LEGAL AND EDUCATIONAL PURPOSES
"""

import requests
import re
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import hashlib

class AdvancedOSINT:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
    
    def email_intelligence(self, first_name, last_name, domain):
        """Generate possible email formats for security testing"""
        print(f"\n📧 [EMAIL INTELLIGENCE] Generating formats for {first_name} {last_name} @ {domain}")
        
        formats = [
            f"{first_name}.{last_name}@{domain}",
            f"{first_name}@{domain}",
            f"{last_name}@{domain}",
            f"{first_name[0]}{last_name}@{domain}",
            f"{first_name}{last_name[0]}@{domain}",
            f"{first_name}_{last_name}@{domain}",
            f"{first_name}-{last_name}@{domain}",
            f"{last_name}.{first_name}@{domain}",
            f"{first_name[0]}.{last_name}@{domain}",
        ]
        
        print("   Generated email formats:")
        for i, email in enumerate(formats, 1):
            print(f"   {i:2}. {email}")
        
        return formats
    
    def metadata_analysis(self, url):
        """Extract and analyze metadata from web resources"""
        print(f"\n📄 [METADATA ANALYSIS] Extracting from: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            meta_data = {}
            
            # Meta tags
            print("\n   🔍 Meta Tags:")
            for meta in soup.find_all('meta'):
                name = meta.get('name') or meta.get('property') or meta.get('http-equiv')
                content = meta.get('content')
                if name and content:
                    meta_data[name] = content
                    print(f"     {name}: {content[:100]}{'...' if len(content) > 100 else ''}")
            
            # Links and scripts
            print(f"\n   🔗 External Resources:")
            resources = {
                'Stylesheets': soup.find_all('link', rel='stylesheet'),
                'Scripts': soup.find_all('script', src=True),
                'Images': soup.find_all('img', src=True)
            }
            
            for resource_type, items in resources.items():
                print(f"     {resource_type}: {len(items)}")
                for item in items[:3]:  # Show first 3
                    src = item.get('src') or item.get('href')
                    if src:
                        full_url = urljoin(url, src)
                        print(f"       → {full_url[:80]}{'...' if len(full_url) > 80 else ''}")
            
            return meta_data
            
        except Exception as e:
            print(f"❌ Error in metadata analysis: {e}")
            return {}
    
    def website_technology(self, url):
        """Identify technologies used by website"""
        print(f"\n🛠️ [TECHNOLOGY DETECTION] Analyzing: {url}")
        
        technologies = {
            'CMS': ['wordpress', 'joomla', 'drupal', 'wix', 'squarespace'],
            'Frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'laravel'],
            'Web Servers': ['apache', 'nginx', 'iis', 'cloudflare'],
            'Programming': ['php', 'python', 'ruby', 'node.js', 'java'],
            'E-commerce': ['shopify', 'magento', 'woocommerce', 'prestashop']
        }
        
        try:
            response = self.session.get(url, timeout=10)
            headers = response.headers
            content = response.text.lower()
            
            detected = []
            
            # Check headers
            server = headers.get('server', '').lower()
            powered_by = headers.get('x-powered-by', '').lower()
            
            print("   🔍 Detected Technologies:")
            
            # Check for technologies in content
            for category, tech_list in technologies.items():
                for tech in tech_list:
                    if tech in content or tech in server or tech in powered_by:
                        detected.append(tech)
                        print(f"     ✅ {category}: {tech.title()}")
            
            # Check for common patterns
            patterns = {
                'Google Analytics': r'ga\(\'create\'|\'UA-\d',
                'Google Tag Manager': r'googletagmanager',
                'Facebook Pixel': r'facebook\.com\/tr\/',
                'jQuery': r'jquery',
                'Bootstrap': r'bootstrap'
            }
            
            for tech_name, pattern in patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    detected.append(tech_name)
                    print(f"     ✅ Analytics/Tools: {tech_name}")
            
            if not detected:
                print("     ⚠️ No common technologies detected")
            
            return detected
            
        except Exception as e:
            print(f"❌ Error in technology detection: {e}")
            return []
    
    def security_headers_audit(self, url):
        """Comprehensive security headers audit"""
        print(f"\n🛡️ [SECURITY HEADERS AUDIT] Testing: {url}")
        
        security_headers = {
            'Content-Security-Policy': 'Prevents XSS attacks',
            'Strict-Transport-Security': 'Enforces HTTPS',
            'X-Frame-Options': 'Prevents clickjacking',
            'X-Content-Type-Options': 'Prevents MIME sniffing',
            'X-XSS-Protection': 'XSS protection for older browsers',
            'Referrer-Policy': 'Controls referrer information',
            'Permissions-Policy': 'Controls browser features',
            'Feature-Policy': 'Controls browser features (older)'
        }
        
        try:
            response = self.session.get(url, timeout=10)
            
            print("   Security Headers Status:")
            for header, description in security_headers.items():
                value = response.headers.get(header, 'MISSING')
                status = "✅" if value != 'MISSING' else "❌"
                print(f"     {status} {header}:")
                print(f"        Value: {value}")
                print(f"        Purpose: {description}")
                print()
            
            # Calculate security score
            total_headers = len(security_headers)
            present_headers = sum(1 for h in security_headers if h in response.headers)
            security_score = (present_headers / total_headers) * 100
            
            print(f"   📊 Security Headers Score: {security_score:.1f}%")
            
        except Exception as e:
            print(f"❌ Error in security headers audit: {e}")

def main():
    advanced = AdvancedOSINT()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                   ADVANCED OSINT FEATURES                   ║
║                 For Cybersecurity Education                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Example usage
    print("🔧 Example Demonstrations:\n")
    
    # Email intelligence example
    advanced.email_intelligence("john", "doe", "company.com")
    
    # Technology detection example
    advanced.website_technology("https://httpbin.org")
    
    # Security headers audit example
    advanced.security_headers_audit("https://httpbin.org")
    
    print("\n🎓 Educational demonstrations completed!")

if __name__ == "__main__":
    main()
