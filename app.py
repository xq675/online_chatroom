from flask import Flask, render_template, request, session
import random
import json
import uuid
import os
#print(os.urandom(24))

app = Flask(__name__)

app.secret_key = b'\xf7h\xd9D\xdc\xc5ljC\xfb`\xec\xe8\xf6s`\xde7\xe30\xef\xc7\xf2\xb2'

# global list of previously used usernames
usernames = []

# global list of messages
messages = []

@app.route('/')
def index():
    return render_template('combined.html')

@app.route('/login', methods=["POST"])
def login():
    # grab incoming data from the request object
    incoming_data = request.json

    # if the username variable is not present, generate an error
    if 'username' not in incoming_data:
        payload = {
            'status': 'error',
            'detail': 'empty username'
        }
        return json.dumps(payload)

    # extract the username
    username = incoming_data['username'].lower()

    # if the username is an empty string, generate an error
    if len(username) == 0:
        payload = {
            'status': 'error',
            'detail': 'empty username'
        }
        return json.dumps(payload)

    # if the username contains non-alphabetic characters, generate an error
    if username.isalpha() == False:
        payload = {
            'status': 'error',
            'detail': 'invalid username'
        }
        return json.dumps(payload)        

    # if the username is a duplicate, generate an error
    if username in usernames:
        payload = {
            'status': 'error',
            'detail': 'duplicate username'
        }
        return json.dumps(payload)

    # username is valid! add it to our global list of usernames
    usernames.append(username)

    # set up a 'session' for the client
    session['username'] = username

    colors = ['deeppink', 'darkmagenta', 'darkorange', 'darkblue', 'darkolivegreen', 'gold', 'maroon', 'teal']
    session['color'] = random.choice(colors)

    # generate a success message and send it to the client
    payload = {
        'status': 'success',
        'detail': None
    }
    return json.dumps(payload)

@app.route('/add_message', methods=['POST'])
def add_message():

    if 'username' not in session:
        payload = {
            'status': 'error',
            'detail': 'unknown user'
        }
        return json.dumps(payload)        

    # grab incoming data from the request object
    incoming_data = request.json

    # if the message variable is not present, generate an error
    if 'message' not in incoming_data:
        payload = {
            'status': 'error',
            'detail': 'empty message'
        }
        return json.dumps(payload)

    # extract the message
    message = incoming_data['message'].lower()

    # if the message is an empty string, generate an error
    if len(message) == 0:
        payload = {
            'status': 'error',
            'detail': 'empty message'
        }
        return json.dumps(payload)

    if message == '/roll':
        randomNum = random.randint(1, 6)
        message = f"rolled a {randomNum}!"

    # the message is valid! add it to our messages list
    messages.append({
        'username': session['username'],
        'message': message,
        'color': session['color']
    })

    # generate a success message and send it to the client
    payload = {
        'status': 'success',
        'detail': None
    }
    return json.dumps(payload)

@app.route('/get_messages')
def get_messages():

    # get message offset (default to 0 to get all messages)
    message_offset = int( request.args.get('message_offset', 0) )

    print("message offset:", message_offset)

    # extract the desired set of messages
    set_of_messages = messages[message_offset:]

    # package this up into a payload that includes the total length of the messages list
    payload = {
        'messages': set_of_messages,
        'total_messages': len(messages)
    }

    # send back the serialized version of the messages dictionary to the client
    return json.dumps( payload )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
