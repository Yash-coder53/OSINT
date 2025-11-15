#!/usr/bin/env python3
"""
Educational OSINT Tool for Cybersecurity Learning
ONLY FOR LEGAL AND EDUCATIONAL PURPOSES
"""

import os
import sys
import requests
import json
import socket
import time
import dns.resolver
from urllib.parse import urlparse
import concurrent.futures
import argparse

class OSINTTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def display_banner(self):
        print("""
╔══════════════════════════════════════════════════════════════╗
║                   EDUCATIONAL OSINT TOOL                    ║
║                 For Cybersecurity Learning                  ║
║                                                            ║
║  ⚠️  ONLY FOR LEGAL EDUCATIONAL AND TESTING PURPOSES  ⚠️  ║
║        Misuse of this tool is strictly prohibited          ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def check_dependencies(self):
        """Check if required packages are installed"""
        required_modules = ['requests', 'dns.resolver']
        missing = []
        
        for module in required_modules:
            try:
                if module == 'dns.resolver':
                    import dns.resolver
                else:
                    __import__(module)
            except ImportError:
                missing.append(module)
        
        if missing:
            print(f"❌ Missing dependencies: {', '.join(missing)}")
            print("💡 Install with: pip install -r requirements.txt")
            return False
        return True
    
    def domain_reconnaissance(self, domain):
        """Comprehensive domain information gathering"""
        print(f"\n🔍 [DOMAIN RECON] Gathering information for: {domain}")
        
        try:
            # Basic DNS resolution
            print(f"\n📡 DNS Information:")
            ip = socket.gethostbyname(domain)
            print(f"   IP Address: {ip}")
            
            # Various DNS record types
            record_types = {
                'A': 'IPv4 Address',
                'AAAA': 'IPv6 Address', 
                'MX': 'Mail Exchange',
                'NS': 'Name Server',
                'TXT': 'Text Records',
                'SOA': 'Start of Authority',
                'CNAME': 'Canonical Name'
            }
            
            for rtype, description in record_types.items():
                try:
                    answers = dns.resolver.resolve(domain, rtype)
                    print(f"\n   {description} ({rtype}):")
                    for rdata in answers:
                        print(f"     → {rdata}")
                except Exception as e:
                    print(f"   {description} ({rtype}): Not found")
                    
        except Exception as e:
            print(f"❌ Error in domain reconnaissance: {e}")
    
    def ip_intelligence(self, ip):
        """IP address information and geolocation"""
        print(f"\n🌐 [IP INTELLIGENCE] Lookup for: {ip}")
        
        try:
            response = self.session.get(f"http://ip-api.com/json/{ip}", timeout=10)
            data = response.json()
            
            if data['status'] == 'success':
                print(f"\n📍 Geolocation:")
                print(f"   Country: {data.get('country', 'N/A')}")
                print(f"   Region: {data.get('regionName', 'N/A')}")
                print(f"   City: {data.get('city', 'N/A')}")
                print(f"   ZIP: {data.get('zip', 'N/A')}")
                print(f"   Coordinates: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
                
                print(f"\n🏢 Network Information:")
                print(f"   ISP: {data.get('isp', 'N/A')}")
                print(f"   Organization: {data.get('org', 'N/A')}")
                print(f"   AS: {data.get('as', 'N/A')}")
                
                print(f"\n🌍 Timezone:")
                print(f"   Timezone: {data.get('timezone', 'N/A')}")
            else:
                print("❌ IP lookup failed")
                
        except Exception as e:
            print(f"❌ Error in IP intelligence: {e}")
    
    def website_forensics(self, url):
        """Website security headers and information"""
        print(f"\n🔒 [WEBSITE FORENSICS] Analyzing: {url}")
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            response = self.session.get(url, timeout=15, allow_redirects=True)
            
            print(f"\n📊 Response Details:")
            print(f"   Status Code: {response.status_code}")
            print(f"   Final URL: {response.url}")
            print(f"   Content Length: {len(response.content)} bytes")
            print(f"   Encoding: {response.encoding}")
            
            print(f"\n🏗️ Server Headers:")
            server_headers = ['server', 'x-powered-by', 'x-aspnet-version']
            for header in server_headers:
                value = response.headers.get(header, 'NOT DISCLOSED')
                print(f"   {header.title()}: {value}")
            
            print(f"\n🛡️ Security Headers Analysis:")
            security_headers = {
                'strict-transport-security': 'HSTS Policy',
                'content-security-policy': 'Content Security Policy', 
                'x-frame-options': 'Clickjacking Protection',
                'x-content-type-options': 'MIME Sniffing Prevention',
                'x-xss-protection': 'XSS Protection',
                'referrer-policy': 'Referrer Policy'
            }
            
            for header, description in security_headers.items():
                value = response.headers.get(header, '❌ NOT SET')
                status = "✅" if value != '❌ NOT SET' else "❌"
                print(f"   {status} {description}: {value}")
                
        except Exception as e:
            print(f"❌ Error in website forensics: {e}")
    
    def subdomain_discovery(self, domain, wordlist=None):
        """Subdomain enumeration with common wordlist"""
        print(f"\n🔎 [SUBDOMAIN DISCOVERY] Scanning: {domain}")
        
        if wordlist is None:
            subdomains = [
                'www', 'mail', 'ftp', 'smtp', 'pop', 'imap', 'webmail', 'admin', 'api',
                'blog', 'shop', 'store', 'forum', 'support', 'help', 'docs', 'portal',
                'test', 'dev', 'staging', 'cdn', 'static', 'media', 'img', 'images',
                'app', 'apps', 'mobile', 'm', 'secure', 'vpn', 'remote', 'ssh',
                'ns1', 'ns2', 'dns', 'mysql', 'db', 'database', 'backup', 'old'
            ]
        else:
            subdomains = wordlist
        
        discovered = []
        
        def check_subdomain(subdomain):
            full_domain = f"{subdomain}.{domain}"
            try:
                ip = socket.gethostbyname(full_domain)
                discovered.append((full_domain, ip))
                print(f"   ✅ Found: {full_domain} → {ip}")
            except socket.gaierror:
                pass
            except Exception as e:
                pass
        
        print(f"   Scanning {len(subdomains)} subdomains...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(check_subdomain, subdomains)
        
        print(f"\n📈 Discovery Summary: {len(discovered)} subdomains found")
        return discovered
    
    def network_port_scan(self, target, ports=None):
        """Network port scanning for common services"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 8080, 8443, 3306, 3389]
        
        print(f"\n🔌 [PORT SCANNING] Target: {target}")
        print(f"   Scanning {len(ports)} common ports...")
        
        def scan_port(port):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(2)
                    result = sock.connect_ex((target, port))
                    if result == 0:
                        try:
                            service = socket.getservbyport(port, 'tcp')
                        except:
                            service = 'unknown'
                        return port, service
            except:
                pass
            return None
        
        open_ports = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(scan_port, ports)
            for result in results:
                if result:
                    port, service = result
                    print(f"   ✅ Port {port}/tcp open - {service}")
                    open_ports.append((port, service))
        
        print(f"\n📊 Port Scan Summary: {len(open_ports)} ports open")
        return open_ports
    
    def digital_footprint(self, username):
        """Check digital footprint across platforms"""
        print(f"\n👤 [DIGITAL FOOTPRINT] Username: {username}")
        
        platforms = {
            'GitHub': f'https://github.com/{username}',
            'Twitter': f'https://twitter.com/{username}',
            'Instagram': f'https://instagram.com/{username}',
            'Reddit': f'https://reddit.com/user/{username}',
            'YouTube': f'https://youtube.com/@{username}',
            'Facebook': f'https://facebook.com/{username}',
            'LinkedIn': f'https://linkedin.com/in/{username}',
            'TikTok': f'https://tiktok.com/@{username}',
            'Pinterest': f'https://pinterest.com/{username}',
            'GitLab': f'https://gitlab.com/{username}',
        }
        
        found = []
        
        for platform, url in platforms.items():
            try:
                response = self.session.head(url, timeout=8, allow_redirects=False)
                if response.status_code in [200, 301, 302]:
                    print(f"   ✅ {platform:12}: Account exists")
                    found.append(platform)
                else:
                    print(f"   ❌ {platform:12}: Not found")
            except:
                print(f"   ⚠️ {platform:12}: Connection failed")
        
        print(f"\n📱 Digital Presence: {len(found)} platforms found")
        return found
    
    def export_results(self, data, filename):
        """Export results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Results exported to: {filename}")
        except Exception as e:
            print(f"❌ Error exporting results: {e}")

def ethical_warning():
    """Display ethical usage warning"""
    print("""
⚠️  ETHICAL USAGE WARNING ⚠️

This tool is designed for:
✅ Educational purposes
✅ Cybersecurity learning
✅ Authorized penetration testing
✅ Security research with permission

STRICTLY PROHIBITED:
❌ Unauthorized scanning
❌ Illegal activities  
❌ Privacy violations
❌ Malicious attacks

By using this tool, you agree to use it ethically and legally.
The developers are not responsible for any misuse.
    """)

def main():
    tool = OSINTTool()
    tool.display_banner()
    ethical_warning()
    
    if not tool.check_dependencies():
        sys.exit(1)
    
    parser = argparse.ArgumentParser(
        description='Educational OSINT Tool for Cybersecurity Learning',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python osint_tool.py -d example.com
  python osint_tool.py -i 8.8.8.8 -o ip_report.json
  python osint_tool.py -s target.com -p 192.168.1.1
  python osint_tool.py -U john_doe --full-scan
        '''
    )
    
    parser.add_argument('-d', '--domain', help='Target domain for reconnaissance')
    parser.add_argument('-i', '--ip', help='Target IP address for intelligence')
    parser.add_argument('-u', '--url', help='Target URL for website forensics')
    parser.add_argument('-s', '--subdomain', help='Domain for subdomain discovery')
    parser.add_argument('-p', '--portscan', help='Target for port scanning')
    parser.add_argument('-U', '--username', help='Username for digital footprint analysis')
    parser.add_argument('-o', '--output', help='Output file to save results')
    parser.add_argument('--full-scan', action='store_true', help='Perform comprehensive scan when using domain')
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    results = {}
    
    try:
        if args.domain:
            results['domain_recon'] = args.domain
            tool.domain_reconnaissance(args.domain)
            
            if args.full_scan:
                results['subdomains'] = tool.subdomain_discovery(args.domain)
                try:
                    ip = socket.gethostbyname(args.domain)
                    results['port_scan'] = tool.network_port_scan(ip)
                except:
                    print("❌ Cannot resolve domain for port scanning")
            
        if args.ip:
            results['ip_intelligence'] = args.ip
            tool.ip_intelligence(args.ip)
            results['port_scan'] = tool.network_port_scan(args.ip)
            
        if args.url:
            results['website_forensics'] = args.url
            tool.website_forensics(args.url)
            
        if args.subdomain:
            results['subdomain_discovery'] = args.subdomain
            tool.subdomain_discovery(args.subdomain)
            
        if args.portscan:
            results['port_scanning'] = args.portscan
            tool.network_port_scan(args.portscan)
            
        if args.username:
            results['digital_footprint'] = args.username
            tool.digital_footprint(args.username)
            
        if args.output and results:
            tool.export_results(results, args.output)
            
        print(f"\n🎯 OSINT Operations Completed!")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
