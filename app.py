from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime
from database import (
    init_db, add_vacation, get_all_vacations, get_active_vacation,
    get_vacation_by_id, update_vacation_notes, set_active_vacation,
    delete_vacation, calculate_days_remaining
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database on startup
init_db()

@app.route('/')
def index():
    """Homepage showing countdown to active vacation."""
    active_vacation = get_active_vacation()
    
    days_remaining = None
    if active_vacation:
        days_remaining = calculate_days_remaining(active_vacation['start_date'])
    
    return render_template('index.html', 
                         vacation=active_vacation, 
                         days_remaining=days_remaining)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new vacation."""
    if request.method == 'POST':
        location = request.form.get('location')
        start_date = request.form.get('start_date')
        notes = request.form.get('notes', '')
        is_active = request.form.get('is_active') == 'on'
        
        if not location or not start_date:
            flash('Location and start date are required!', 'error')
            return redirect(url_for('add'))
        
        try:
            vacation_id = add_vacation(location, start_date, notes, is_active)
            flash(f'Vacation to {location} added successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error adding vacation: {str(e)}', 'error')
            return redirect(url_for('add'))
    
    return render_template('add_vacation.html')

@app.route('/list')
def list_vacations():
    """List all vacations."""
    vacations = get_all_vacations()
    
    # Calculate days remaining for each vacation
    vacation_data = []
    for vacation in vacations:
        days = calculate_days_remaining(vacation['start_date'])
        vacation_data.append({
            'vacation': vacation,
            'days_remaining': days
        })
    
    return render_template('list_vacations.html', vacation_data=vacation_data)

@app.route('/edit/<int:vacation_id>', methods=['GET', 'POST'])
def edit_notes(vacation_id):
    """Edit notes for a vacation."""
    vacation = get_vacation_by_id(vacation_id)
    
    if not vacation:
        flash('Vacation not found!', 'error')
        return redirect(url_for('list_vacations'))
    
    if request.method == 'POST':
        notes = request.form.get('notes', '')
        try:
            update_vacation_notes(vacation_id, notes)
            flash('Notes updated successfully!', 'success')
            return redirect(url_for('list_vacations'))
        except Exception as e:
            flash(f'Error updating notes: {str(e)}', 'error')
    
    return render_template('edit_notes.html', vacation=vacation)

@app.route('/set_active/<int:vacation_id>')
def set_active(vacation_id):
    """Set a vacation as active."""
    try:
        set_active_vacation(vacation_id)
        flash('Active vacation updated!', 'success')
    except Exception as e:
        flash(f'Error setting active vacation: {str(e)}', 'error')
    
    return redirect(url_for('list_vacations'))

@app.route('/delete/<int:vacation_id>', methods=['POST'])
def delete(vacation_id):
    """Delete a vacation."""
    try:
        delete_vacation(vacation_id)
        flash('Vacation deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting vacation: {str(e)}', 'error')
    
    return redirect(url_for('list_vacations'))

@app.route('/api/send-reminder', methods=['POST'])
def api_send_reminder():
    """API endpoint for cron job to trigger WhatsApp reminder."""
    # Simple API key check for security
    api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
    expected_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    if api_key != expected_key:
        return {'error': 'Unauthorized'}, 401
    
    # Import here to avoid circular import
    from sms_service import send_vacation_reminder
    
    success = send_vacation_reminder()
    
    if success:
        return {'status': 'success', 'message': 'Reminder sent successfully'}, 200
    else:
        return {'status': 'warning', 'message': 'No active vacation or failed to send'}, 200

@app.template_filter('format_date')
def format_date(date_str):
    """Format date for display."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'production') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
