"""
Cron job script for sending daily message reminders (SMS or WhatsApp) via Render Cron Job.
This script should be scheduled to run daily on Render.
"""

import os
import sys
import random
import time as time_module

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sms_service import send_vacation_reminder, MESSAGE_TYPE

def main():
    """Main function for the cron job."""
    print(f"Starting {MESSAGE_TYPE.upper()} cron job at {time_module.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Add random delay (0-60 minutes) to make SMS time random each day
    # This ensures SMS is sent at different times
    delay_seconds = random.randint(0, 3600)  # 0 to 60 minutes
    delay_minutes = delay_seconds / 60
    
    print(f"Waiting {delay_minutes:.1f} minutes before sending {MESSAGE_TYPE.upper()}...")
    time_module.sleep(delay_seconds)
    
    # Send the message
    print(f"Sending {MESSAGE_TYPE.upper()} at {time_module.strftime('%Y-%m-%d %H:%M:%S')}")
    success = send_vacation_reminder()
    
    if success:
        print(f"{MESSAGE_TYPE.upper()} cron job completed successfully!")
        sys.exit(0)
    else:
        print(f"{MESSAGE_TYPE.upper()} cron job completed with warnings.")
        sys.exit(0)  # Exit with 0 even if no message sent (might not have active vacation)

if __name__ == '__main__':
    main()
