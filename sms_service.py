import os
import random
from datetime import datetime, time
from dotenv import load_dotenv
from twilio.rest import Client
from database import get_active_vacation, calculate_days_remaining

# Load environment variables from .env file
load_dotenv()

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
TO_PHONE_NUMBER = os.environ.get('TO_PHONE_NUMBER')
APP_URL = os.environ.get('APP_URL', 'http://localhost:5000')

# Message type: 'sms' or 'whatsapp'
MESSAGE_TYPE = os.environ.get('MESSAGE_TYPE', 'whatsapp').lower()

def send_vacation_reminder():
    """Send message reminder about the active vacation via SMS or WhatsApp."""
    
    # Check if Twilio credentials are configured
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, TO_PHONE_NUMBER]):
        print("Twilio credentials not configured. Skipping message.")
        return False
    
    # Get active vacation
    vacation = get_active_vacation()
    
    if not vacation:
        print("No active vacation found. Skipping message.")
        return False
    
    # Calculate days remaining
    days_remaining = calculate_days_remaining(vacation['start_date'])
    
    if days_remaining is None:
        print("Error calculating days remaining.")
        return False
    
    # Get vacation notes if available
    notes = vacation['notes'] if vacation['notes'] else ''
    notes = notes.strip()
    notes_section = f"\n\n*Notes:* {notes}" if notes else ""
    
    # Create message based on days remaining
    if days_remaining > 0:
        if MESSAGE_TYPE == 'whatsapp':
            # WhatsApp supports rich formatting and emojis
            message = f"""🏖️ *Vacation Countdown* 🏖️

Only *{days_remaining} day{'s' if days_remaining != 1 else ''}* left until your vacation to *{vacation['location']}*! ✈️{notes_section}

Get ready for an amazing time! 🎉

{APP_URL}"""
        else:
            # SMS - simpler message
            notes_text = f" - {notes}" if notes else ""
            message = f"Only {days_remaining} day{'s' if days_remaining != 1 else ''} left until {vacation['location']}!{notes_text} 🏖️ {APP_URL}"
    elif days_remaining == 0:
        if MESSAGE_TYPE == 'whatsapp':
            message = f"""🎉 *TODAY IS THE DAY!* 🎉

Your vacation to *{vacation['location']}* starts TODAY!{notes_section}

Have an absolutely amazing time! 🌴✨

{APP_URL}"""
        else:
            message = f"🎉 Today is the day! Your vacation to {vacation['location']} starts today! Have an amazing time! {APP_URL}"
    else:
        print(f"Vacation to {vacation['location']} has already passed.")
        return False
    
    # Prepare phone numbers for WhatsApp or SMS
    if MESSAGE_TYPE == 'whatsapp':
        from_number = f'whatsapp:{TWILIO_PHONE_NUMBER}'
        to_number = f'whatsapp:{TO_PHONE_NUMBER}'
        service_name = 'WhatsApp'
    else:
        from_number = TWILIO_PHONE_NUMBER
        to_number = TO_PHONE_NUMBER
        service_name = 'SMS'
    
    # Send message using Twilio
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        msg = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )
        
        print(f"{service_name} sent successfully! SID: {msg.sid}")
        print(f"Status: {msg.status}")
        print(f"Message: {message}")
        return True
        
    except Exception as e:
        print(f"Error sending {service_name}: {str(e)}")
        return False

def get_random_time_today():
    """Generate a random time between 9 AM and 8 PM."""
    hour = random.randint(9, 20)
    minute = random.randint(0, 59)
    return time(hour, minute)

if __name__ == '__main__':
    # Test the messaging service
    print(f"Testing {MESSAGE_TYPE.upper()} service...")
    send_vacation_reminder()
