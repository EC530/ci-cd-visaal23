from flask import Flask, request, jsonify
from bson import ObjectId
from pymongo import MongoClient
from flask_pymongo import PyMongo
from datetime import datetime


app = Flask(__name__)

app = Flask(__name__)
app.config["MONGO_URI"] = "mongomongo.db+srv://visaaln2:visaal456@ec530.qevqtrc.mongomongo.db.net/healthmonitoring?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/api/conversations/<user_id>', methods=['GET'])
def list_conversations(user_id):
    conversations = mongo.db.conversations.find({"$or": [{"doctorId": ObjectId(user_id)}, {"patientId": ObjectId(user_id)}]})
    return jsonify([conv for conv in conversations])

@app.route('/api/conversations/<conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    messages = mongo.db.messages.find({"conversationId": ObjectId(conversation_id)})
    return jsonify([message for message in messages])

@app.route('/api/conversations/<conversation_id>/send', methods=['POST'])
def send_message(conversation_id):
    data = request.json
    message = {
        "conversationId": ObjectId(conversation_id),
        "senderId": ObjectId(data['senderId']),
        "text": data['text'],
        "createdAt": datetime.now()
    }
    mongo.db.messages.insert_one(message)
    mongo.db.conversations.update_one({"_id": ObjectId(conversation_id)}, {"$set": {"lastMessage": data['text'], "lastMessageAt": datetime.now()}})
    return jsonify({"status": "Message sent"}), 201

@app.route('/api/conversations/start', methods=['POST'])
def start_conversation():
    data = request.json
    conversation = {
        "doctorId": ObjectId(data['doctorId']),
        "patientId": ObjectId(data['patientId']),
        "createdAt": datetime.now(),
        "lastMessage": "",
        "lastMessageAt": None
    }
    result = mongo.db.conversations.insert_one(conversation)
    return jsonify({"conversationId": str(result.inserted_id)}), 201

if __name__ == '__main__':
    app.run(debug=True)
