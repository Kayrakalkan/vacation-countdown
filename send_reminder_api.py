"""
Cron job script for Render - Calls API endpoint instead of accessing database directly.
This solves the issue of Render cron jobs not supporting persistent disks.
"""

import os
import sys
import requests
import random
import time as time_module

def main():
    """Call the web service API to send vacation reminder."""
    print("=" * 60)
    print("CRON JOB - API CALLER VERSION")
    print("=" * 60)
    
    # Get configuration from environment
    app_url = os.environ.get('APP_URL')
    api_key = os.environ.get('SECRET_KEY')
    
    if not app_url:
        print("ERROR: APP_URL environment variable not set!")
        sys.exit(1)
    
    if not api_key:
        print("ERROR: SECRET_KEY environment variable not set!")
        sys.exit(1)
    
    print(f"App URL: {app_url}")
    print(f"API Key: {'*' * 20} (hidden)")
    
    # Add random delay (0-60 seconds) to make reminder time random each day
    delay_seconds = random.randint(0, 3600)  # 0 to 60 seconds
    delay_minutes = delay_seconds / 60
    
    print(f"Waiting {delay_minutes:.1f} minutes before sending reminder...")
    time_module.sleep(delay_seconds)
    
    # Call the API endpoint
    api_endpoint = f"{app_url.rstrip('/')}/api/send-reminder"
    print(f"\nCalling API: {api_endpoint}")
    
    try:
        response = requests.post(
            api_endpoint,
            headers={'X-API-Key': api_key},
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.json()}")
        
        if response.status_code == 200:
            print("✓ Cron job completed successfully!")
            sys.exit(0)
        else:
            print(f"⚠ API returned status {response.status_code}")
            sys.exit(0)  # Don't fail the cron job
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error calling API: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
