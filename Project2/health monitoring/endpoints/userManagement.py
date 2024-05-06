from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from bson.errors import InvalidId
from flask_cors import CORS, cross_origin 

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config["MONGO_URI"] = "mongodb+srv://admin:admin@ec530.qevqtrc.mongodb.net/healthmonitoring?retryWrites=true&w=majority"
mongo = PyMongo(app)

# Helper to parse ObjectId to string
def parse_json(data):
    if "_id" in data:
        data["_id"] = str(data["_id"])
    return data

@app.route('/admin/users', methods=['POST'])
def add_user():
    data = request.json
    if not data or not data.get('username'):
        return jsonify({'error': 'Missing user data'}), 400
    # Add additional validation as necessary
    user_id = mongo.db.users.insert_one(data).inserted_id
    return jsonify({'message': 'User added', 'user_id': str(user_id)}), 201

@app.route('/admin/users', methods=['GET'])
def list_users():
    role = request.args.get('role')
    query = {"roles": role} if role else {}
    users = mongo.db.users.find(query)
    users_list = [parse_json(user) for user in users]
    return jsonify(users_list), 200

@app.route('/admin/search', methods=['GET'])
@cross_origin()
def search_users():
    search_query = request.args.get('query', '')
    print(f"Search query received: {search_query}")

    query = {}
    if search_query:
        regex = f'^{search_query}'
        query = {
            "$or": [
                {"personalInfo.firstName": {"$regex": regex, "$options": "i"}},
                {"personalInfo.lastName": {"$regex": regex, "$options": "i"}}
            ]
        }
    print(f"MongoDB query: {query}")

    users = mongo.db.users.find(query)
    usernames_list = [user['personalInfo']['firstName'] + " " + user['personalInfo']['lastName'] for user in users]
    print(f"Users found: {usernames_list}")

    return jsonify(usernames_list), 200



@app.route('/admin/users/<userId>', methods=['PUT'])
def update_user(userId):
    data = request.json  # This will contain the personalInfo object and potentially other fields

    try:
        # Prepare the update object to include personalInfo and roles if provided
        update_data = {
            '$set': {
                'personalInfo': data.get('personalInfo', {})  # Ensuring the update only affects the personalInfo subdocument
            }
        }
        
        # Check if roles are provided and update them
        if 'roles' in data:
            update_data['$set']['roles'] = data['roles']

        result = mongo.db.users.update_one({'_id': ObjectId(userId)}, update_data)
        if result.modified_count:
            return jsonify({'message': 'User updated successfully'}), 200
        else:
            return jsonify({'error': 'No user found or data unchanged'}), 404
    except InvalidId:
        return jsonify({'error': 'Invalid user ID'}), 400

@app.route('/admin/users/<userId>', methods=['DELETE'])
def delete_user(userId):
    try:
        # Convert userId from string to ObjectId for MongoDB operation
        userObjectId = ObjectId(userId)
    except InvalidId:
        return jsonify({'error': 'Invalid user ID'}), 400

    # Delete user from 'users' collection
    result_users = mongo.db.users.delete_one({'_id': userObjectId})
    
    # Delete user from 'authentication' collection
    # Assuming 'userId' field in 'authentication' collection is storing ObjectId reference to 'users' collection
    result_auth = mongo.db.authentication.delete_one({'userId': userObjectId})

    if result_users.deleted_count and result_auth.deleted_count:
        return jsonify({'message': 'User and authentication details deleted successfully'}), 200
    elif result_users.deleted_count:
        return jsonify({'warning': 'User deleted but authentication details not found'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/admin/users/<userId>/roles', methods=['POST'])
def assign_roles(userId):
    roles = request.json.get('roles')
    if not roles:
        return jsonify({'error': 'Missing roles'}), 400
    try:
        result = mongo.db.users.update_one({'_id': ObjectId(userId)}, {'$addToSet': {'roles': {'$each': roles}}})
        if result.modified_count:
            mongo.db.users.update_one({'_id': ObjectId(userId)}, {'$set': {'status': 'active'}})
            return jsonify({'message': 'Roles assigned successfully'}), 200
        else:
            return jsonify({'error': 'User not found or roles unchanged'}), 404
    except InvalidId:
        return jsonify({'error': 'Invalid user ID'}), 400



@app.route('/admin/users/<userId>/roles', methods=['DELETE'])
def remove_role(userId):
    data = request.json
    roles_to_remove = data.get('roles')

    if not roles_to_remove:
        return jsonify({'error': 'Missing roles to remove'}), 400

    if isinstance(roles_to_remove, str):
        roles_to_remove = [roles_to_remove]

    try:
        userObjectId = ObjectId(userId)
    except InvalidId:
        return jsonify({'error': 'Invalid user ID'}), 400

    # Remove the specified roles
    result = mongo.db.users.update_one(
        {'_id': userObjectId},
        {'$pullAll': {'roles': roles_to_remove}}
    )

    if result.modified_count:
        # Check if the user has any roles left
        user = mongo.db.users.find_one({'_id': userObjectId}, {'roles': 1})
        if user and len(user.get('roles', [])) == 0:
            # If no roles left, set the user status to "inactive"
            mongo.db.users.update_one({'_id': userObjectId}, {'$set': {'status': 'inactive'}})
            return jsonify({'message': 'Role(s) removed and user set to inactive due to no roles'}), 200
        return jsonify({'message': 'Role(s) removed successfully'}), 200
    else:
        return jsonify({'error': 'User not found or roles not present in the user'}), 404


@app.route('/admin/search/details', methods=['GET'])
@cross_origin()
def search_user_details():
    # Fetch full name from query parameters
    full_name = request.args.get('name', '')
    print(f"Search query received: Full Name: {full_name}")

    # Split full name into first name and last name
    name_parts = full_name.split()
    if len(name_parts) < 2:
        return jsonify({"error": "Please provide both first and last names."}), 400

    first_name, last_name = name_parts[0], ' '.join(name_parts[1:])  # Handles middle names or double last names

    print(f"Searching for: First Name: {first_name}, Last Name: {last_name}")

    # Construct query to find users based on exact first name and last name
    query = {
        "personalInfo.firstName": first_name,
        "personalInfo.lastName": last_name
    }

    print(f"MongoDB query: {query}")

    # Execute the query
    user = mongo.db.users.find_one(query)  # Using find_one to ensure only one user is fetched

    # Check if user exists
    if not user:
        return jsonify({"error": "No user found matching the provided names."}), 404

    # Clean up MongoDB's _id field for JSON serialization
    user['_id'] = str(user['_id'])

    print(f"User found: {user}")

    return jsonify(user), 200


if __name__ == '__main__':
    app.run(debug=True)
