"""
Cron job script for sending daily message reminders (SMS or WhatsApp) via Render Cron Job.
This version has NO DELAY - for testing purposes only.
"""

import os
import sys
import time as time_module

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sms_service import send_vacation_reminder, MESSAGE_TYPE

def main():
    """Main function for the cron job - NO DELAY VERSION."""
    print(f"Starting {MESSAGE_TYPE.upper()} cron job (NO DELAY) at {time_module.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Send the message immediately (no delay for testing)
    print(f"Sending {MESSAGE_TYPE.upper()} immediately at {time_module.strftime('%Y-%m-%d %H:%M:%S')}")
    success = send_vacation_reminder()
    
    if success:
        print(f"{MESSAGE_TYPE.upper()} sent successfully!")
        sys.exit(0)
    else:
        print(f"{MESSAGE_TYPE.upper()} failed or no active vacation found.")
        sys.exit(0)  # Exit with 0 even if no message sent (might not have active vacation)

if __name__ == '__main__':
    main()
