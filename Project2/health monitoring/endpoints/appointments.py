from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongomongo.db+srv://visaaln2:visaal456@ec530.qevqtrc.mongomongo.db.net/healthmonitoring?retryWrites=true&w=majority"
mongo = PyMongo(app)
CORS(app)

@app.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    if not all(key in data for key in ['patientId', 'doctorId', 'date', 'time', 'location', 'priority']):
        return jsonify({"error": "Missing data"}), 400

    # Create the appointment
    appointment_id = mongo.db.appointments.insert_one({
        'patientId': data['patientId'],
        'doctorId': data['doctorId'],
        'date': data['date'],
        'time': data['time'],
        'location': data['location'],
        'priority': data['priority'],
        'status': 'scheduled'
    }).inserted_id

    return jsonify({'message': 'Appointment created successfully', 'appointmentId': str(appointment_id)}), 201

@app.route('/appointments', methods=['GET'])
def get_appointments():
    patient_id = request.args.get('patientId')
    doctor_id = request.args.get('doctorId')
    query = {}
    if patient_id:
        query['patientId'] = patient_id
    if doctor_id:
        query['doctorId'] = doctor_id

    appointments = list(mongo.db.appointments.find(query))
    for appointment in appointments:
        appointment['_id'] = str(appointment['_id'])

    return jsonify(appointments), 200

@app.route('/appointments/<appointmentId>', methods=['GET'])
def get_appointment(appointmentId):
    appointment = mongo.db.appointments.find_one({'_id': ObjectId(appointmentId)})
    if appointment is None:
        return jsonify({'error': 'Appointment not found'}), 404

    appointment['_id'] = str(appointment['_id'])
    return jsonify(appointment), 200

@app.route('/appointments/<appointmentId>', methods=['DELETE'])
def delete_appointment(appointmentId):
    result = mongo.db.appointments.delete_one({'_id': ObjectId(appointmentId)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Appointment not found'}), 404

    return jsonify({'message': 'Appointment canceled successfully'}), 204

@app.route('/appointments/<appointmentId>', methods=['PUT'])
def update_appointment(appointmentId):
    data = request.json
    if not all(key in data for key in ['newDate', 'newTime']):
        return jsonify({"error": "Missing new date or time"}), 400

    result = mongo.db.appointments.update_one(
        {'_id': ObjectId(appointmentId)},
        {'$set': {'date': data['newDate'], 'time': data['newTime'], 'status': 'rescheduled'}}
    )
    if result.modified_count == 0:
        return jsonify({'error': 'Appointment not found or data not changed'}), 404

    return jsonify({'message': 'Appointment rescheduled successfully'}), 200

@app.route('/appointments/<appointmentId>', methods=['PATCH'])
def patch_appointment(appointmentId):
    data = request.json
    update_data = {}
    if 'priority' in data:
        update_data['priority'] = data['priority']

    if not update_data:
        return jsonify({"error": "No data provided for update"}), 400

    result = mongo.db.appointments.update_one(
        {'_id': ObjectId(appointmentId)},
        {'$set': update_data}
    )
    if result.modified_count == 0:
        return jsonify({'error': 'Appointment not found or data not changed'}), 404

    return jsonify({'message': 'Appointment updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
