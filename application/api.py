from flask import Flask, request
from bson import json_util
from helpers.users import *
from helpers.checking import check_params, check_exists


app = Flask(__name__)

@app.route("/greetings")
def greeting():
    '''
    Endpoint to test the API and say "hello" to the user 
    Returns: a  sentence to say hello
    '''
    return "helloooo!!"

@app.route("/users/new")
def users_new():
    '''
    Endpoint to introduce new users data to our data set
    Returns: a new user id
    '''
    args = dict(request.args)
    id = insert_user(args)
    return json_util.dumps({"_id":id})

@app.route("/users/complete")
def users():
    '''
    Endpoint to test the data in the API
    Returns: existing users in our database
    '''
    return json_util.dumps(list_users())

@app.route("/groups/complete")
def groups():
    '''
    Endpoint to test the data in the API
    Returns: existing groups in our database
    '''
    return json_util.dumps(list_groups())

@app.route("/users/delete/")   
def users_delete():
    '''
    Endpoint to delete an user and the related messages
    '''
    '''args = dict(request.args)
    return json_util.dumps(delete_user(args))'''
    args = dict(request.args)
    id = delete_user(args)
    return json_util.dumps({"user":id})

@app.route("/messages/complete/")
def messages():
    '''
    Endpoint to test the data in the API
    Returns: existing messages in our database
    '''
    return json_util.dumps(list_messsages())

@app.route("/messages/complete2/")
def messagess():
    '''
    Endpoint to test the data in the API
    Returns: existing messages in our database
    '''
    q = {"group":__name__}
    data = read_coll(db,q,project={"user":1,"message":1,"_id":0})
    return json_util.dumps(data)

@app.route("/messagesbygroup/<group>")
def messages_by_group(group):
    '''
    Endpoint to obtain messsages the data in the API by taking group name which returns messages.
    '''
    q = {"group":__name__}
    if not check_params(q,{"Turbias", "Jerez Covid","Family"}):
        return {"Error":"The group does not exist"}
    data = read_coll(db,q,project={"user":1,"message":1,"_id":0})

    return json_util.dumps(data)

app.run(debug=True)