import os
from app import app
from flask import render_template, request, redirect, session, url_for
from bson.objectid import ObjectId

events = [
        {"event":"First Day of Classes", "date":"2019-08-21"},
        {"event":"Winter Break", "date":"2019-12-20"},
        {"event":"Finals Begin", "date":"2019-12-01"}
    ]


from flask_pymongo import PyMongo

app.secret_key = b'i3rfnign4##@@'

# name of database
app.config['MONGO_DBNAME'] = 'IA'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:TRq3ABvirj4uQc3M@cluster0-acen4.mongodb.net/IA?retryWrites=true&w=majority'

mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')

def index():
    #sessions
    session["username"] = "Chaz"
    #connect to the Mongo DB
    collection = mongo.db.events
    #find all of the events in that database using a query , store it as events
    #{} will return everything in the database
    #list constructor will turn the results into a list (of dictionaries/objects)
    events = list(collection.find({}))
    print (events)
    return render_template('index.html', events = events)

@app.route('/add')

def add():
    users = mongo.db.users
    users.insert({'email' : "chazjackson"})
    return "something"





#SIGNUP
@app.route('/signup', methods=["get", "post" ])

def signup():
    print("signup is running")
    print(request.method)
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'email' : request.form['email']})
        print(existing_user)

        if existing_user is None:
            userinfo = request.form
            print(userinfo)
            email = userinfo['email']
            print(email)
            password = userinfo['password']
            print(password)
            users.insert({'email' : request.form['email'], 'password' : request.form['password']})
            session['email'] = request.form['email']
            return redirect(url_for('index'))

        return "That username already exists! Try logging in."

    return render_template('signup.html')
# CONNECT TO DB, ADD DATA

@app.route('/results', methods = ["get", "post"])
def results():
    collection = mongo.db.events
    # store userinfo from the form
    user_info = dict(request.form)
    print(user_info)
    #store the event_name
    event_name = user_info["event_name"]
    print("the event name is ", event_name)
    #store the event_date
    event_date = user_info["event_date"]
    print("the event date is ", event_date)
    #connect to Mongo DB
    category = user_info["category"]
    print("the category is ", category)
    event_time = user_info["event_time"]
    print("the time of the event is ", event_time)
    #insert the user's input event_name and event_date to MONGO
    collection.insert({"event_name": event_name, "event_date": event_date, "category": category, "event_time": event_time})
    #(so that it will continue to exist after this program stops)
    #redirect back to the index page
    return redirect('/index')

@app.route('/FilterbyCategory', methods = ["get","post"])
def FilterbyCategory():
    collection = mongo.db.events
    user_info = dict(request.form)
    category = user_info["category"]
    filterevents = list(collection.find({"category": category}))
    return render_template('EventFilter.html', events = filterevents)

@app.route('/Filterbydate', methods = ["get","post"])
def Filterbydate():
    collection = mongo.db.events
    user_info = dict(request.form)
    event_date = user_info["event_date"]
    filterevents = list(collection.find({"event_date": event_date}))
    return render_template('EventFilter.html', events = filterevents)

@app.route('/Filterbyname', methods = ["get","post"])
def Filterbyname():
    collection = mongo.db.events
    user_info = dict(request.form)
    event_name = user_info["event_name"]
    filterevents = list(collection.find({"event_name": event_name}))
    return render_template('EventFilter.html', events = filterevents)



@app.route('/deleteall')

def deleteall():
    # connect to the database
    collection = mongo.db.events
    # insert new data
    collection.delete_many({})
    # return a message to the user
    return redirect('/index')

@app.route('/deleteform')

def deleteform():
    collection = mongo.db.events
    events = list(collection.find({}))
    print (events)
    return render_template('deleteform.html', events = events)


@app.route('/delete', methods=['get', 'post'])

def delete():
    user_info = dict(request.form)
    print(user_info)

    myquery = mongo.db.events.find({'_id': ObjectId(user_info['_id'])})
    print("This is myquery")
    print(list(myquery))

    result = mongo.db.events.delete_one({'_id': ObjectId(user_info['_id'])})
    #
    #
    return redirect('/index')
