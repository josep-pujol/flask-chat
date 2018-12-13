from datetime import datetime
import os
from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = 'randomstring123'
messages = []


def write_to_file(filename, data):
    with open(filename, 'a') as file:
        file.writelines(data)


def add_messages(username, message):
    write_to_file('data/messages.txt', '{0} {1}: {2}\n'.format(
                            datetime.now().strftime('%H:%M:%S'), 
                            username.title(), 
                            message))

def get_all_messages():
    ''''Get all of the messages and separate them by a <br> '''
    messages = []
    with open('data/messages.txt', 'r') as chat_messages:
        messages = chat_messages.readlines()
    return messages


@app.route('/', methods=['GET', 'POST'])
def index():
    '''Main page with instructions'''
    if request.method == 'POST':
        write_to_file('data/users.txt', request.form['username'] + '\n')
        return redirect(request.form['username'])
    return render_template('index.html')


@app.route('/<username>')
def user(username):
    '''Display chat messages'''
    messages = get_all_messages()
    return render_template('chat.html', 
                            username=username, chat_messages=messages)


@app.route('/<username>/<message>')
def send_message(username, message):
    '''Create a new message and redirect back to the chat page'''
    add_messages(username, message)
    return redirect(username)


app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)

