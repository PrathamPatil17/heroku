#!/usr/bin/env python3
"""
Simple health check for Heroku deployment
"""

import requests
import sys
import os

def health_check():
    """Perform a basic health check"""
    port = os.getenv('PORT', '8001')
    url = f"http://localhost:{port}/health"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') in ['healthy', 'running']:
                print("✅ Health check passed")
                return 0
            else:
                print(f"❌ Health check failed: {data.get('status', 'unknown')}")
                return 1
        else:
            print(f"❌ Health check failed: HTTP {response.status_code}")
            return 1
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(health_check())
