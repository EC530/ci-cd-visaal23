## API Overview

### Device Management

- **POST /api/device/register**
  - Register a new medical device in the system.
  - **Request Payload**:
    ```json
    {
      "deviceId": "string",
      "patientId": "string",
      "deviceType": "string",
      "model": "string",
      "manufacturer": "string"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Device registered successfully"
    }
    ```

- **POST /api/device/:deviceId/data**
  - Submit data from a medical device.
  - **Request Parameters**: `deviceId` (unique identifier for the device)
  - **Request Payload**:
    ```json
    {
      "measurementType": "string",
      "value": "number",
      "timestamp": "ISO 8601 string"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Data received successfully"
    }
    ```

- **PUT /api/device/:deviceId/settings**
  - Update settings for a medical device.
  - **Request Parameters**: `deviceId`
  - **Request Payload**:
    ```json
    {
      "measurementInterval": "string",
      "alertThresholds": "object"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Settings updated successfully"
    }
    ```

- **GET /api/device/:deviceId/info**
  - Retrieve information about a registered medical device.
  - **Request Parameters**: `deviceId`
  - **Response**:
    ```json
    {
      "deviceId": "string",
      "deviceType": "string",
      "model": "string",
      "manufacturer": "string",
      "settings": "object"
    }
    ```

### Appointment Management

- **POST /appointments**
  - Create an appointment.
  - **Request Payload**:
    ```json
    {
      "patientId": "string",
      "doctorId": "string",
      "date": "YYYY-MM-DD",
      "time": "HH:MM",
      "location": "string",
      "priority": "string"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Appointment created successfully",
      "appointmentId": "string"
    }
    ```

- **GET /appointments**
  - Retrieve appointments based on optional filters.
  - **Request Parameters (optional)**:
    - `patientId`: ID of the patient
    - `doctorId`: ID of the doctor
  - **Response**:
    ```json
    [
      {
        "_id": "string",
        "patientId": "string",
        "doctorId": "string",
        "date": "YYYY-MM-DD",
        "time": "HH:MM",
        "location": "string",
        "priority": "string",
        "status": "string"
      }
    ]
    ```

- **GET /appointments/:appointmentId**
  - Retrieve a specific appointment.
  - **Request Parameters**: `appointmentId`
  - **Response**:
    ```json
    {
      "_id": "string",
      "patientId": "string",
      "doctorId": "string",
      "date": "YYYY-MM-DD",
      "time": "HH:MM",
      "location": "string",
      "priority": "string",
      "status": "string"
    }
    ```

- **DELETE /appointments/:appointmentId**
  - Cancel an appointment.
  - **Request Parameters**: `appointmentId`
  - **Response**:
    ```json
    {
      "message": "Appointment canceled successfully"
    }
    ```

- **PUT /appointments/:appointmentId**
  - Update an appointment.
  - **Request Parameters**: `appointmentId`
  - **Request Payload**:
    ```json
    {
      "newDate": "YYYY-MM-DD",
      "newTime": "HH:MM"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Appointment rescheduled successfully"
    }
    ```

- **PATCH /appointments/:appointmentId**
  - Partially update an appointment.
  - **Request Parameters**: `appointmentId`
  - **Request Payload**:
    ```json
    {
      "priority": "string"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Appointment updated successfully"
    }
    ```

### Authentication and User Management

- **POST /register**
  - Register a new user.
  - **Request Payload**:
    ```json
    {
      "username": "string",
      "email": "string",
      "password": "string",
      "roles": ["string"],
      "firstName": "string",
      "lastName": "string",
      "dateOfBirth": "YYYY-MM-DD"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "User registered successfully",
      "user_id": "string"
    }
    ```

- **POST /login**
  - Log in a user.
  - **Request Payload**:
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Login successful"
    }
    ```

- **POST /logout**
  - Log out a user.
  - **Response**:
    ```json
    {
      "message": "Logged out successfully"
    }
    ```

### Conversations and Messaging

- **GET /api/conversations/:user_id**
  - Retrieve all conversations for a specific user.
  - **Request Parameters**: `user_id`
  - **Response**:
    ```json
    [
      {
        "_id": "string",
        "doctorId": "string",
        "patientId": "string",
        "createdAt": "ISO 8601 string",
        "lastMessage": "string",
        "lastMessageAt": "ISO 8601 string"
      }
    ]
    ```

- **GET /api/conversations/:conversation_id/messages**
  - Retrieve all messages for a specific conversation.
  - **Request Parameters**: `conversation_id`
  - **Response**:
    ```json
    [
      {
        "_id": "string",
        "conversationId": "string",
        "senderId": "string",
        "text": "string",
        "createdAt": "ISO 8601 string"
      }
    ]
    ```

- **POST /api/conversations/:conversation_id/send**
  - Send a message in a specific conversation.
  - **Request Parameters**: `conversation_id`
  - **Request Payload**:
    ```json
    {
      "senderId": "string",
      "text": "string"
    }
    ```
  - **Response**:
    ```json
    {
      "status": "Message sent"
    }
    ```

- **POST /api/conversations/start**
  - Start a new conversation between a doctor and a patient.
  - **Request Payload**:
    ```json
    {
      "doctorId": "string",
      "patientId": "string"
    }
    ```
  - **Response**:
    ```json
    {
      "conversationId": "string"
    }
    ```

### Patient Measurements and Alerts

- **GET /patients/:patientId/measurements**
  - Retrieve all measurements for a specific patient.
  - **Request Parameters**: `patientId`
  - **Response**:
    ```json
    [
      {
        "_id": "string",
        "patientId": "string",
        "measurementType": "string",
        "value": "number",
        "dateTime": "ISO 8601 string"
      }
    ]
    ```

- **POST /patients/:patientId/measurements**
  - Add a measurement for a specific patient.
  - **Request Parameters**: `patientId`
  - **Request Payload**:
    ```json
    {
      "measurementType": "string",
      "value": "number",
      "dateTime": "ISO 8601 string"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Measurement added successfully"
    }
    ```

- **GET /patients/:patientId/alerts**
  - Retrieve all alerts for a specific patient.
  - **Request Parameters**: `patientId`
  - **Response**:
    ```json
    [
      {
        "_id": "string",
        "patientId": "string",
        "alertType": "string",
        "description": "string",
        "dateTime": "ISO 8601 string"
      }
    ]
    ```

- **POST /patients/:patientId/alerts**
  - Create an alert for a specific patient.
  - **Request Parameters**: `patientId`
  - **Request Payload**:
    ```json
    {
      "alertType": "string",
      "description": "string",
      "dateTime": "ISO 8601 string"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "Alert created successfully"
    }
    ```
