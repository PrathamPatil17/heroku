#!/usr/bin/env python3
"""
Test script for Heroku deployment
"""

import requests
import json
import os
import sys

def test_heroku_deployment(app_url=None):
    """Test the deployed Heroku application"""
    
    if not app_url:
        app_name = input("Enter your Heroku app name: ")
        app_url = f"https://{app_name}.herokuapp.com"
    
    print(f"Testing deployment at: {app_url}")
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{app_url}/health", timeout=30)
        if response.status_code == 200:
            print("✅ Health check passed")
            health_data = response.json()
            print(f"   Status: {health_data.get('status', 'unknown')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(f"{app_url}/", timeout=30)
        if response.status_code == 200:
            print("✅ Root endpoint accessible")
            root_data = response.json()
            print(f"   Message: {root_data.get('message', 'N/A')}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test 3: API Documentation
    print("\n3. Testing API documentation...")
    try:
        response = requests.get(f"{app_url}/docs", timeout=30)
        if response.status_code == 200:
            print("✅ API documentation accessible")
            print(f"   Documentation URL: {app_url}/docs")
        else:
            print(f"❌ Documentation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Documentation error: {e}")
    
    # Test 4: OpenAPI schema
    print("\n4. Testing OpenAPI schema...")
    try:
        response = requests.get(f"{app_url}/openapi.json", timeout=30)
        if response.status_code == 200:
            print("✅ OpenAPI schema accessible")
            schema = response.json()
            print(f"   API Title: {schema.get('info', {}).get('title', 'N/A')}")
            print(f"   API Version: {schema.get('info', {}).get('version', 'N/A')}")
        else:
            print(f"❌ OpenAPI schema failed: {response.status_code}")
    except Exception as e:
        print(f"❌ OpenAPI schema error: {e}")
    
    print(f"\n🎉 Deployment test completed!")
    print(f"📱 Your app is available at: {app_url}")
    print(f"📚 API Documentation: {app_url}/docs")
    print(f"📋 Alternative Docs: {app_url}/redoc")
    
    return True

def test_api_endpoint(app_url, bearer_token=None):
    """Test the main API endpoint with authentication"""
    
    if not bearer_token:
        bearer_token = "880b4911f53f0dc33bb443bfc2c5831f87db7bc9d8bf084d6f42acb6918b02f7"
    
    print(f"\n5. Testing main API endpoint (requires valid API keys)...")
    
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json"
    }
    
    # Simple test payload
    payload = {
        "documents": "https://www.example.com/sample.pdf",
        "questions": ["What is this document about?"]
    }
    
    try:
        response = requests.post(
            f"{app_url}/hackrx/run",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            print("✅ API endpoint accessible (authentication works)")
        elif response.status_code == 401:
            print("⚠️ API endpoint requires authentication (expected)")
        elif response.status_code == 422:
            print("⚠️ API endpoint validation error (check document URL)")
        else:
            print(f"❌ API endpoint error: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ API endpoint error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        app_url = sys.argv[1]
        if not app_url.startswith("http"):
            app_url = f"https://{app_url}.herokuapp.com"
    else:
        app_url = None
    
    success = test_heroku_deployment(app_url)
    
    if success and app_url:
        test_api_endpoint(app_url)
