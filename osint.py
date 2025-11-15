#!/usr/bin/env python3
"""
Educational OSINT Tool for Termux
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
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
    def banner(self):
        print("""
╔═══════════════════════════════════════╗
║         EDUCATIONAL OSINT TOOL        ║
║           FOR TERMUX ONLY             ║
║      ONLY FOR LEGAL PURPOSES          ║
╚═══════════════════════════════════════╝
        """)
    
    def check_dependencies(self):
        """Check if required packages are installed"""
        try:
            import dns.resolver
            import requests
            return True
        except ImportError as e:
            print(f"Missing dependency: {e}")
            print("Install with: pip install requests dnspython")
            return False
    
    def domain_info(self, domain):
        """Gather domain information"""
        print(f"\n[+] Gathering information for: {domain}")
        
        try:
            # IP resolution
            ip = socket.gethostbyname(domain)
            print(f"IP Address: {ip}")
            
            # DNS records
            record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA']
            for record_type in record_types:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    for rdata in answers:
                        print(f"{record_type} Record: {rdata}")
                except:
                    pass
                    
        except Exception as e:
            print(f"Error in domain lookup: {e}")
    
    def ip_lookup(self, ip):
        """Basic IP information"""
        print(f"\n[+] IP Lookup for: {ip}")
        
        try:
            # Basic IP information
            response = self.session.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            
            if data['status'] == 'success':
                print(f"Country: {data.get('country', 'N/A')}")
                print(f"Region: {data.get('regionName', 'N/A')}")
                print(f"City: {data.get('city', 'N/A')}")
                print(f"ISP: {data.get('isp', 'N/A')}")
                print(f"Organization: {data.get('org', 'N/A')}")
                print(f"AS: {data.get('as', 'N/A')}")
            else:
                print("IP lookup failed")
                
        except Exception as e:
            print(f"Error in IP lookup: {e}")
    
    def website_headers(self, url):
        """Analyze website headers"""
        print(f"\n[+] Analyzing headers for: {url}")
        
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
                
            response = self.session.get(url, timeout=10)
            
            print(f"Status Code: {response.status_code}")
            print("Headers:")
            for header, value in response.headers.items():
                print(f"  {header}: {value}")
                
            # Check security headers
            security_headers = ['strict-transport-security', 'content-security-policy', 
                              'x-frame-options', 'x-content-type-options']
            print("\nSecurity Headers:")
            for header in security_headers:
                value = response.headers.get(header, 'NOT SET')
                print(f"  {header}: {value}")
                
        except Exception as e:
            print(f"Error analyzing headers: {e}")
    
    def subdomain_scan(self, domain):
        """Basic subdomain enumeration"""
        print(f"\n[+] Scanning for subdomains: {domain}")
        
        subdomains = [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop', 'ns1', 'webdisk',
            'ns2', 'cpanel', 'whm', 'autodiscover', 'autoconfig', 'm', 'imap', 'test',
            'ns', 'blog', 'pop3', 'dev', 'www2', 'admin', 'forum', 'news', 'vpn',
            'api', 'apps', 'app', 'secure', 'demo', 'portal', 'shop', 'cdn', 'static'
        ]
        
        found_subdomains = []
        
        def check_subdomain(subdomain):
            full_domain = f"{subdomain}.{domain}"
            try:
                socket.gethostbyname(full_domain)
                found_subdomains.append(full_domain)
                print(f"Found: {full_domain}")
            except:
                pass
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(check_subdomain, subdomains)
        
        return found_subdomains
    
    def port_scan(self, target, ports=None):
        """Basic port scanning"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 8080, 8443]
        
        print(f"\n[+] Scanning ports on: {target}")
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                sock.close()
                if result == 0:
                    service = socket.getservbyport(port, 'tcp') if port in range(1, 65536) else 'unknown'
                    print(f"Port {port}/tcp open - {service}")
                    return port
            except:
                pass
            return None
        
        open_ports = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(scan_port, ports)
            open_ports = [port for port in results if port is not None]
        
        return open_ports
    
    def social_media_check(self, username):
        """Check username across platforms (educational)"""
        print(f"\n[+] Checking username: {username}")
        
        platforms = {
            'GitHub': f'https://github.com/{username}',
            'Twitter': f'https://twitter.com/{username}',
            'Instagram': f'https://instagram.com/{username}',
            'Reddit': f'https://reddit.com/user/{username}',
            'YouTube': f'https://youtube.com/@{username}',
        }
        
        for platform, url in platforms.items():
            try:
                response = self.session.head(url, timeout=5)
                if response.status_code == 200:
                    print(f"✓ {platform}: Found")
                else:
                    print(f"✗ {platform:10}: Not found")
            except:
                print(f"✗ {platform:10}: Error checking")
    
    def save_results(self, data, filename):
        """Save results to file"""
        try:
            with open(filename, 'w') as f:
                if isinstance(data, (dict, list)):
                    json.dump(data, f, indent=2)
                else:
                    f.write(str(data))
            print(f"\n[+] Results saved to: {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")

def main():
    tool = OSINTTool()
    tool.banner()
    
    if not tool.check_dependencies():
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='Educational OSINT Tool')
    parser.add_argument('-d', '--domain', help='Target domain')
    parser.add_argument('-i', '--ip', help='Target IP address')
    parser.add_argument('-u', '--url', help='Target URL')
    parser.add_argument('-s', '--subdomain', help='Subdomain scan')
    parser.add_argument('-p', '--portscan', help='Port scan target')
    parser.add_argument('-U', '--username', help='Username for social media check')
    parser.add_argument('-o', '--output', help='Output file')
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    results = {}
    
    try:
        if args.domain:
            tool.domain_info(args.domain)
            results['domain_info'] = args.domain
            
        if args.ip:
            tool.ip_lookup(args.ip)
            results['ip_info'] = args.ip
            
        if args.url:
            tool.website_headers(args.url)
            results['website_headers'] = args.url
            
        if args.subdomain:
            subdomains = tool.subdomain_scan(args.subdomain)
            results['subdomains'] = subdomains
            
        if args.portscan:
            ports = tool.port_scan(args.portscan)
            results['open_ports'] = ports
            
        if args.username:
            tool.social_media_check(args.username)
            results['username_check'] = args.username
            
        if args.output and results:
            tool.save_results(results, args.output)
            
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user")
    except Exception as e:
        print(f"[!] Error: {e}")

if __name__ == "__main__":
    main()
