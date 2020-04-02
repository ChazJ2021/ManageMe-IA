import os
from app import app
from flask import render_template, request, redirect, session, url_for
from bson.objectid import ObjectId

##Deleting one item
##Two words when enterring item location

# Steps for Pushing to GitHub:
# git add .
# git commit -m "(message)"
# git push

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
    #connect to the Mongo DB
    collection = mongo.db.events
    item_collection = mongo.db.items
    #find all of the events in that database using a query , store it as events
    #{} will return everything in the database
    #list constructor will turn the results into a list (of dictionaries/objects)
    items = list(collection.find({}))
    print (items)
    events = list(collection.find({}))
    print (events)
    # print("The session username is ", session['username'])
    return render_template('index.html', events = events, items = items)


@app.route('/add')
def add():
    users = mongo.db.users
    users.insert({'email' : "chazjackson"})
    return "something"

#SIGNUP
@app.route('/signup', methods=["get", "post" ])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_username = users.find_one({'username' : request.form['username']})
        existing_email= users.find_one({'email' : request.form['email']})

        if existing_username is None and existing_email is None:
            userinfo = request.form
            email = userinfo['email']
            username = userinfo['username']
            password = userinfo['password']
            FamilyMemberemail = userinfo['FamilyMemberemail']
            if FamilyMemberemail == "":
                print(FamilyMemberemail, "yyyyyyy")
                users.insert({'email' : request.form['email'], 'password' : request.form['password'], 'username' : request.form['username'], "FamilyEmail" : request.form['email']})
                session['email'] = request.form['email']
                session['username']= request.form['username']
            else:
                print("This user is signing up with a family username")
                users.insert({'email' : request.form['email'], 'password' : request.form['password'], 'username' : request.form['username'], "FamilyEmail" : request.form['FamilyMemberemail']})
                session['email'] = request.form['FamilyMemberemail']
                collection = mongo.db.users
                #Query the collection for email that is the family member email
                #Store query
                family_email = users.find_one({'email' : request.form['FamilyMemberemail']})
                print(family_email, "ccccccccccc")
                #Store username from Query
                family_username = (family_email["username"])
                print(family_username, "wwwwwwwwww")
                #Change the session username to the username from that object
                session['username']= request.form['username']
            return redirect(url_for('index'))

        return "That email already exists! Try logging in."

    return render_template('signup.html')

@app.route('/login', methods = ['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'email' : request.form['email']} )
    print("The login user is", login_user)

    if login_user:
        if request.form['password'] == login_user['password']:
            session ['email'] = login_user['email']
            session['username'] = login_user['username']
            return redirect (url_for('index'))

    return 'Invalid username/password combination, try again'

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/index')


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
    collection.insert({"event_name": event_name, "event_date": event_date, "category": category, "event_time": event_time, "email": session["email"]})
    #(so that it will continue to exist after this program stops)
    #redirect back to the index page
    return redirect('/myevents')


@app.route('/FilterbyCategory', methods = ["get","post"])
def FilterbyCategory():
    collection = mongo.db.events
    user_info = dict(request.form)
    category = user_info["category"]
    filterevents = list(collection.find({"category": category}))
    return render_template('EventFilter.html', events = filterevents)

@app.route('/Filterbyitemname', methods = ["get","post"])
def Filterbyitemname():
    collection = mongo.db.items
    user_info = dict(request.form)
    item_name = user_info["item_name"]
    filteritems = list(collection.find({"item_name": item_name}))
    return render_template('itemfilter.html', items = filteritems)

@app.route('/Filterbylocation', methods = ["get","post"])
def FilterbyLocation():
    collection = mongo.db.items
    user_info = dict(request.form)
    item_location = user_info["item_location"]
    filteritems = list(collection.find({"item_location": item_location}))
    return render_template('itemfilter.html', items = filteritems)

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

@app.route('/deleteallitems')
def deleteallitems():
    # connect to the database
    collection = mongo.db.items
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

@app.route('/deleteformitem')
def deleteformitem():
    collection = mongo.db.items
    items = list(collection.find({}))
    print (items)
    return render_template('deleteformitem.html')

@app.route('/delete', methods=['get', 'post'])
def delete():
    user_info = dict(request.form)
    myquery = mongo.db.events.find({'_id': ObjectId(user_info['_id'])})
    result = mongo.db.events.delete_one({'_id': ObjectId(user_info['_id'])})
    return redirect('/index')

@app.route('/deleteitem', methods=['get', 'post'])
def deleteitem():
    user_info = dict(request.form)
    myquery = mongo.db.items.find({'_id': ObjectId(user_info['_id'])})
    result = mongo.db.items.delete_one({'_id': ObjectId(user_info['_id'])})
    return redirect('/index')
#Show specific user events
@app.route('/myevents')

def myevents():
    #connect to mongo DB
    collection = mongo.db.events
    #find all data
    name = session['username']
    events = list(collection.find({"email":session["email"]}))
    print(events)
    # return a message
    return render_template("myevents.html", events = events)

@app.route('/eventfilter')
def eventfilter():
    #connect to mongo DB
    collection = mongo.db.events
    #find all data
    name = session['username']
    events = collection.find({"user":name})
    # from similar_text import similar_text
    # n = similar_text(a, x["event_category"])
    # N = similar_text(a.lower(), x["event_category"])
    # if N == 100 or n == 100:
    #     return render_template("eventfilter.html", events = events)
    # elif n >= 75 or n>= 75:
    #     print ("You might want to type that more carefully, that event category does not exist")
    return render_template("eventfilter.html", events = events)

@app.route('/itemfilter')
def itemfilter():
    #connect to mongo DB
    collection = mongo.db.items
    #find all data
    name = session['username']
    items = collection.find({"user":name})
    # from similar_text import similar_text
    # n = similar_text(a, x["event_category"])
    # N = similar_text(a.lower(), x["event_category"])
    # if N == 100 or n == 100:
    #     return render_template("eventfilter.html", events = events)
    # elif n >= 75 or n>= 75:
    #     print ("You might want to type that more carefully, that event category does not exist")
    return render_template("itemfilter.html", items = items)

@app.route('/deleteaccount', methods=['get', 'post'])
def deleteaccount():
    user_info = dict(request.form)
    ##Query all the events with the session username
    x = list(mongo.db.events.find({"username":session["username"]}))
    print(x)
    mongo.db.events.delete_many({"username":session["username"]})
    ##Delete all events with the username
    myquery = list(mongo.db.users.find({"username":session["username"]}))
    print(myquery ," ssssssssss ")
    result = mongo.db.users.delete_one({"username":session["username"]})
    session.clear()
    ##What should I pass through in order to delete an account, is it the same thing?
    return redirect('/index')

##Items First

@app.route('/itemsresults', methods = ["get", "post"])
def itemsresults():
    #Connect to mongoDB
    item_collection = mongo.db.items
    # store userinfo from the form
    user_info = dict(request.form)
    print(user_info)
    #store the event_name
    item_name = user_info["item_name"]
    #Store item location
    item_location = user_info["item_location"]
    if item_location!= "":
        item_collection.insert({"item_name": item_name, "item_location": item_location, "username": session["username"]})
    else:
        item_location = user_info["savedlocation"]
        item_collection.insert({"item_name": item_name, "item_location": item_location, "username": session["username"]})
    #insert the user's input event_name and event_date to MONGO
    # item_collection.insert({"item_name": item_name, "item_location": item_location, "username": session["username"]})
    #(so that it will continue to exist after this program stops)
    #redirect back to the index page
    return redirect('/myitems')

@app.route('/myitems')
def myitems():
    #connect to mongo DB
    item_collection = mongo.db.items
    #find all data
    name = session['username']
    items = list(item_collection.find({"username":session["username"]}))
    print(items)
    locations = []
    final_items = []
    for x in items:
        if x["item_location"] in locations:
            print("That's already in the list")
        else:
            locations.append(x["item_location"])
            final_items.append(x)
    return render_template("myitems.html", items = items, locations = locations)
