# Patient Monitoring Platform

## Overview

The **Patient Monitoring Platform** is a comprehensive solution designed to monitor patients in both home and hospital settings. It caters to various user roles and provides seamless integration with third-party medical devices for accurate health data collection.

## Features

### Users and Roles
1. **Roles**:
   - **Patient**: Monitors their health metrics and books appointments.
   - **Medical Professionals (Nurses and Doctors)**: Monitor and interact with patients.
   - **Administrators**: Manage system roles and permissions.
   - **Family Members**: Monitor their family member's health.


2. **User Management**:
   - Add users manually to the system.
   - Assign or change roles to users.
   - A user can have multiple roles (e.g., a doctor can also be a patient).

### Device Integration and Monitoring
1. **Third-Party Medical Device Integration**:
   - Interface for third-party medical devices (Thermometer, Pulse, Blood Pressure, Glucometer, etc.) to send data to the system.

2. **Device Management**:
   - Assign a medical device to a patient.
   - Enable or disable any device.

### Patient Monitoring
1. **Alerts and Scheduling**:
   - Set alerts and schedules for medical measurements (e.g., blood pressure daily).
   - Medical professionals receive alerts if patients fail to measure or if measurements are outside an acceptable range.

2. **Data Entry**:
   - Medical professionals can input data for any patient.
   - Patients can enter measurements at any time.
   - Medical professionals can read transcripts of patient-uploaded videos and messages.

### Communication and Appointments
1. **Communication**:
   - Medical professionals can chat with patients using text, voice, or video.

2. **Appointment Management**:
   - Medical professionals can show open time slots on their calendar.
   - Medical professionals can see all booked appointments.
   - Patients can book appointments with medical professionals.

## Tech Stack
- **Backend**: Flask
- **Database**: MongoDB
- **Frontend**: React

