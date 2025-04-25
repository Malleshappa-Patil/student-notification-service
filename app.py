from flask import Flask, request, render_template, send_file
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import threading
import time
import pytz

app = Flask(__name__)

# Configuration (You might want to move these to environment variables)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your-mailid'
SMTP_PASSWORD = 'you-smtp-server-password'
SENDER_EMAIL = 'your-mailid'

reminders = []

# Define IST timezone
IST = pytz.timezone('Asia/Kolkata')

def send_email(recipient_email, subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def check_reminders():
    while True:
        now = datetime.now(IST)
        print(f"Checking reminders at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}...")
        for reminder in reminders[:]:
            if reminder['datetime'] <= now and not reminder['sent']:
                reminder_subject_with_time = f"Reminder: {reminder['subject']}"
                reminder_body = f"""
                Hello,
                This is a reminder for: {reminder['message']}
                Scheduled for: {reminder['datetime'].strftime('%Y-%m-%d %H:%M %Z')}
                """
                if send_email(reminder['email'], reminder_subject_with_time, reminder_body):
                    reminder['sent'] = True
                    print(f"Reminder sent to {reminder['email']} at {reminder['datetime']} for: {reminder['subject']}")
                else:
                    print(f"Failed to send reminder to {reminder['email']}")
        time.sleep(60)

reminder_thread = threading.Thread(target=check_reminders, daemon=True)
reminder_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/offline.html')
def offline():
    return send_file('templates/offline.html')

@app.route('/sw.js')
def service_worker():
    return send_file('templates/sw.js', mimetype='application/javascript')

@app.route('/send_notification', methods=['POST'])
def send_notification():
    student_name = request.form.get('student_name')
    student_email = request.form.get('student_email')
    email_subject = request.form.get('email_subject')
    email_body = request.form.get('email_body')
    reminder_datetime_str = request.form.get('reminder_datetime')
    reminder_subject = request.form.get('reminder_subject')
    reminder_message = request.form.get('reminder_message')

    email_sent = False
    if student_email and email_subject and email_body:
        email_body_with_name = f"""
        Hello {student_name or 'Student'},

        {email_body}
        """
        email_sent = send_email(student_email, email_subject, email_body_with_name)
        print(f"Immediate email sent: {email_sent} to {student_email}")

    if reminder_datetime_str and reminder_subject and reminder_message and student_email:
        try:
            naive_reminder_datetime = datetime.strptime(reminder_datetime_str, '%Y-%m-%dT%H:%M')
            reminder_datetime = IST.localize(naive_reminder_datetime)
            now = datetime.now(IST)
            print(f"Current time: {now}, Reminder time: {reminder_datetime}")
            if reminder_datetime > now:
                reminders.append({
                    'email': student_email,
                    'datetime': reminder_datetime,
                    'subject': reminder_subject,
                    'message': reminder_message,
                    'sent': False
                })
                print(f"Reminder set for {student_email} at {reminder_datetime} for: {reminder_subject}")
            else:
                print(f"Reminder time {reminder_datetime} is not in the future. Current time: {now}")
        except ValueError as e:
            print(f"Invalid reminder datetime format: {e}")

    return render_template('index.html', email_sent=email_sent)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')