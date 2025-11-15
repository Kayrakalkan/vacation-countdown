# Vacation Countdown & Planner App

A simple web application to track remaining days until your planned vacations with daily SMS reminders.

## Features

- **Countdown Timer**: Real-time display of days remaining until your next vacation
- **Daily Reminders**: Automatic notifications sent at random times each day via Twilio
  - 📱 **WhatsApp** (recommended) - Rich formatting, emojis, free
  - 📧 **SMS** - Traditional text messages
- **Vacation Management**: Add, edit, and view vacation details
- **Notes System**: Keep track of planning notes for each vacation
- **Mobile-Friendly**: Responsive design that works on all devices

## Tech Stack

- **Backend**: Python (Flask)
- **Database**: SQLite
- **SMS Service**: Twilio API
- **Scheduler**: APScheduler
- **Deployment**: Render

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd vacation_timer
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+14155238886  # Twilio Sandbox for WhatsApp
TO_PHONE_NUMBER=your_whatsapp_number
MESSAGE_TYPE=whatsapp  # or 'sms' for traditional SMS
APP_URL=http://localhost:5000
```

**For WhatsApp Setup:**
1. Go to [Twilio WhatsApp Sandbox](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn)
2. Send the join code to the sandbox number from your WhatsApp
3. See [WHATSAPP_SETUP.md](WHATSAPP_SETUP.md) for detailed instructions

### 5. Initialize Database

```bash
python database.py
```

### 6. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Deployment to Render

### 1. Environment Variables

In your Render dashboard, add these environment variables:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `TO_PHONE_NUMBER`
- `APP_URL` (your Render app URL)

### 2. Web Service

- Connect your GitHub repository
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

### 3. Cron Job

Create a separate Cron Job service:
- Command: `python send_sms_cron.py`
- Schedule: `0 * * * *` (runs every hour, script handles random timing)

## Project Structure

```
vacation_timer/
├── app.py                  # Main Flask application
├── database.py             # Database initialization and models
├── sms_service.py          # Twilio SMS integration
├── send_sms_cron.py        # Cron job script for Render
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore file
├── README.md              # This file
├── render.yaml            # Render deployment configuration
├── templates/             # HTML templates
│   ├── index.html
│   ├── add_vacation.html
│   ├── list_vacations.html
│   └── edit_notes.html
└── static/                # Static files
    └── style.css
```

## Usage

1. **Add a Vacation**: Click "Add New Vacation" and fill in the destination, start date, and notes
2. **Set Active**: Mark one vacation as active to receive countdown updates
3. **Manage Notes**: Edit planning notes for any vacation
4. **View All**: See a list of all your planned vacations

## License

MIT
