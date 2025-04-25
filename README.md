# Student Notification Service

![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Docker](https://img.shields.io/badge/docker-supported-green.svg)

A Flask-based microservice designed to send email notifications and schedule reminders for students. This service supports immediate email dispatch, scheduled reminders with Indian Standard Time (IST) support, and includes a user-friendly offline page when the server is down.

## Features
- Send immediate email notifications to students.
- Schedule reminder emails with customizable dates and times (supports IST).
- Displays a custom offline page with simple instructions when the server is unavailable.
- Built with Flask, Python, SMTP (Gmail), and Service Workers for offline support.

## Prerequisites
- **Docker**: For running the service in a containerized environment.
- **Git**: To clone the repository.
- **Internet Connection**: Required for email sending via SMTP.

## Installation
Follow these steps to set up the Student Notification Service on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Malleshappa-Patil/student-notification-service.git
   cd student-notification-service

2. **Build and Run with Docker**:
    ```bash
    docker-compose up --build
    This will start the service and make it available at http://127.0.0.1:5000.

3. **Configuration**:
    ```bash
    Update the SMTP credentials in app.py (e.g., SMTP_USERNAME and SMTP_PASSWORD) with your Gmail account details or an app-specific password if 2FA is enabled.
    Ensure your Gmail account allows "less secure apps" or use an app-specific password.


**Usage**
    ```bash
    1. Open your browser and visit http://127.0.0.1:5000.
    2. Fill out the form with:
            Student Name (optional)
            Student Email (required)
            Email Subject (required)
            Email Body (required)
            Reminder Date and Time (required)
            Reminder Subject (required)
            Reminder Message (required)
    3. Click "Send Notification" to send an immediate email and/or schedule a reminder.
    4. The service checks for reminders every minute. Ensure the server remains running for reminders to be sent.


**Offline Mode**
    ```bash
    If the server is down, a friendly message will appear: "Oops! Service is Down". Simply try again later or restart the server if you’re the administrator.

**Technologies**
    ```bash
    Framework: Flask
    Language: Python 3.8+
    Email: SMTP (Gmail)
    Offline Support: Service Workers
    Containerization: Docker

**Contact**
    ```bash
    For questions or support, feel free to open an issue on this repository or contact the maintainer:

    GitHub: Malleshappa-Patil
    Email: mdpatil2004@gmail.com

**Acknowledgments**
    ```bash
    Thanks to the Flask community for the robust framework.
    Inspired by the need for simple student notification systems.
