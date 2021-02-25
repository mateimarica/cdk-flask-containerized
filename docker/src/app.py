import os
import boto3
from flask import jsonify, request

dynamodb = boto3.resource('dynamodb')
dynamodb_table = dynamodb.Table(os.environ['DYNAMODB_TABLE_NAME'])

app = Flask("cdk-flask-api")

@api.route('/user/<username>', methods=['PUT'])
def create_user(username):
	
	# Check if the user already exists, return error if it does
	response = get_user(username)
	if (response[1] == 200):
		return bad_request("That user already exists", 409)

	# Retrieve URL arguements
	email = request.args.get('email')
	age = request.args.get('age')

	# If email and/or age were not provided, keep track of the missing params
	missingParams = []
	if (not email):
		missingParams.append('email')
	if (not age):
		missingParams.append('age')

	# If missingParams is not empty, return error with names of missing parameters
	if (missingParams):
		return bad_request(
			message=f"Invalid syntax, missing parameters: {', '.join(missingParams)}",
			statusCode=400
		)		
	
	# Construct new user
	user = {
		'username': username,
		'email': email,
		'age': age
	}

	# Put user into users table
	dynamodb_table.put_item(Item=user)

	return jsonify({'userCreated': True}), 201

@api.route('/user/<username>', methods=['GET'])
def get_user(username):
	
	# Get user with given username
	response = dynamodb_table.get_item(
		Key={'username': username}
	)

	# If no user returned, return error
	if ('Item' not in response):
		return bad_request("That user could not be found", 404)

	return jsonify(response['Item']), 200

@api.route('/user', methods=['GET'])
def get_all_users():
	response = dynamodb_table.scan()

	return jsonify(response['Items']), 200


@api.route('/user/<username>', methods=['PATCH'])
def update_user(username):

	# Check if user exists
	response = dynamodb_table.get_item(
		Key={'username': username}
	)

	# If user does not exist, cannot update, return error
	if ('Item' not in response):
		return bad_request("That user could not be found", 404)

	# Isolate user item
	response = response['Item']	

	# Retrieve URL parameters
	email = request.args.get('email')
	age = request.args.get('age')

	# If missing any URL parameters, return error
	if (not email and not age):
		return bad_request("Invalid syntax, must have at least one of the following parameters: age, email", 400)

	# Put parameters (if not None) into user item
	if (email):
		response['email'] = email
	if (age):
		response['age'] = age

	# Put user item back into users table
	dynamodb_table.put_item(Item=response)

	return jsonify({'userUpdated': True}), 200

@api.route('/user/<username>', methods=['DELETE'])
def delete_user(username):
	
	# Check if user exists, return error if they don't
	response = get_user(username)
	if (response[1] == 404):
		return response
	
	# Delete user item from users table
	dynamodb_table.delete_item(Key={'username': username})

	return jsonify({'userDeleted': True}), 200

# Build a structured error response
def bad_request(message, statusCode):
	return jsonify(
		{
			'message': message,
			'statusCode': statusCode
		}
	), statusCode
