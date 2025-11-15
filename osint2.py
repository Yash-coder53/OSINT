#!/usr/bin/env python3
# advanced_osint.py

import requests
import re
from bs4 import BeautifulSoup

class AdvancedOSINT:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
    
    def email_format_generator(self, first_name, last_name, domain):
        """Generate possible email formats"""
        formats = [
            f"{first_name}.{last_name}@{domain}",
            f"{first_name}@{domain}",
            f"{last_name}@{domain}",
            f"{first_name[0]}{last_name}@{domain}",
            f"{first_name}{last_name[0]}@{domain}",
        ]
        return formats
    
    def metadata_extractor(self, url):
        """Extract metadata from webpage"""
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            meta_data = {}
            for meta in soup.find_all('meta'):
                name = meta.get('name') or meta.get('property')
                content = meta.get('content')
                if name and content:
                    meta_data[name] = content
            
            return meta_data
        except Exception as e:
            return f"Error: {e}"

# Usage example
if __name__ == "__main__":
    advanced = AdvancedOSINT()
    
    # Email format generation
    emails = advanced.email_format_generator("john", "doe", "company.com")
    print("Possible email formats:")
    for email in emails:
        print(f"  {email}")
