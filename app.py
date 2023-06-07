from flask import render_template
# import sqlite3
from flask import Flask
from flask import request,redirect,url_for,session,flash
from pymongo import MongoClient
# from flask_wtf import Form
# from wtforms import TextField

# import ibm_db


# conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;PROTOCOL=TCPIP;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=fyy29026;PWD=qVHw50ZHhvAFJ0VT;", "", "")
print("Opened database successfully")

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def hel():
    if session.get('username')==True:
        messages = session['username']

    else:
        messages = ""
    user = {'username': messages}
    return redirect(url_for('index',user=user))


@app.route('/reg')
def add():
    return render_template('register.html')

@app.route('/news')
def news():
    return render_template('current.html')

@app.route('/trend')
def trend():
    return render_template('recent.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    msg = ""
    
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']
            bg = request.form['bg']
            email = request.form['email']
            passs = request.form['pass']
            usertype = request.form['usertype']
            avail = 'F'
            if usertype == "recipients":
                avail = 'T'
        
            # Connect to MongoDB
            client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
            db = client['userlist']
            collection = db['plasma_users']
            
            # Create a document to insert
            user_data = {
                'name': nm,
                'addr': addr,
                'city': city,
                'pin': pin,
                'bg': bg,
                'email': email,
                'pass': passs,
                'usertype': usertype,
                'available': avail
            }
            
            # Insert the document into the collection
            result = collection.insert_one(user_data)
            
            if result.inserted_id:
                print("Inserted")
                msg = "Successfully Inserted"
            else:
                print("Not inserted")
                msg = "Not Successfully Inserted"
        except Exception as e:
            print(e)
            msg = "Error in insert operation"
        finally:
            client.close()  # Close the MongoDB connection
            return redirect(url_for('index'))





@app.route('/index',methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        if session.get('username') is not None:
            messages = session['username']
        else:
            messages = ""
        user = {'username': messages}
        print(messages)
        val = request.form['search']
        print(val)
        type = request.form['type']
        print(type)
        if type == 'blood':
            # Connect to MongoDB
            client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
            db = client['userlist']
            collection = db['plasma_users']

            # Filter users by blood group and user type
            filter_query = {
                'bg': val,
                'usertype': 'donor'
            }
            rows = list(collection.find(filter_query))

            # Get all users of type 'donor'
            allusers = list(collection.find({'usertype': 'donor'}))

            client.close()  # Close the MongoDB connection

            print("rows----------------------------")
            print(rows)
            print("allusers---------------------------------------")
            print(allusers)

            return render_template('index.html', title='Home', user=user, rows=allusers, search=rows)

        if type == 'donorname':
            # Connect to MongoDB
            client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
            db = client['userlist']
            collection = db['plasma_users']

            # Filter users by name and user type
            filter_query = {
                'name': val,
                'usertype': 'donor'
            }
            rows = list(collection.find(filter_query))

            # Get all users of type 'donor'
            allusers = list(collection.find({'usertype': 'donor'}))

            client.close()  # Close the MongoDB connection

            print("rows----------------------------")
            print(rows)
            print("allusers---------------------------------------")
            print(allusers)

            return render_template('index.html', title='Home', user=user, rows=allusers, search=rows)

    if session.get('username') is not None:
        messages = session['username']
    else:
        messages = ""
    user = {'username': messages}
    print(messages)
    if request.method == 'GET':
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
        db = client['userlist']
        collection = db['plasma_users']

        # Get all users
        rows = list(collection.find())

        client.close()  # Close the MongoDB connection

        return render_template('index.html', title='Home', user=user, rows=rows)




@app.route('/list')
def lists():
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
    db = client['userlist']
    collection = db['users']

    # Retrieve all documents from the collection
    rows = list(collection.find())

    client.close()  # Close the MongoDB connection

    print(rows)
    return render_template("list.html", rows=rows)

@app.route('/drop')
def dr():
    # Connect to MongoDB
    client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
    db = client['userlist']

    # Drop the 'request' collection
    db['request'].drop()

    client.close()  # Close the MongoDB connection

    return "Dropped successfully"

@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('/login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        usertype = request.form['usertype']

        # Connect to MongoDB
        client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
        db = client['userlist']
        collection = db['plasma_users']

        # Query the user by email
        query = {
            'email': email
        }
        row = collection.find_one(query)

        if not row:
            print("User Not Exists")
            return render_template('/login.html')

        print(row['email'], row['pass'], row['usertype'])
        a = row['email']
        print(a)
        u = {'username': a}
        p = row['pass']
        utype = row['usertype']
        print(p)

        if email == a and password == p and usertype == utype:
            session['username'] = a
            session['name'] = row["name"]
            session['usertype'] = row["usertype"]
            session['level'] = 0
            session['logged_in'] = True

            if row["usertype"] == 'recipients':
                return redirect('dashboard')
            else:
                session['level'] = 0

                # Query requests for the user
                request_query = {
                    'toemail': email
                }
                request_data = list(collection.find(request_query))
                points = 0
                for data in request_data:
                    if data['status'] == 'Accepted':
                        points += 3
                    else:
                        points -= 2
                session['level'] = points
                return redirect('dashboard')
        else:
            return render_template('/login.html')

    else:
        return render_template('/')


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   session.pop('logged_in',None)
   session.pop('usertype',None)
   session.pop('name',None)
   try:
       session.pop('admin',None)
   except KeyError as e:
       print("I got a KeyError - reason " +str(e))


   return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():  
   return render_template("requestdonors.html")



@app.route("/myprofile/<email>", methods=('GET', 'POST'))
def myprofile(email):
    msg = ""
    if request.method == 'GET':
        print(email)

        # Connect to MongoDB
        client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
        db = client['userlist']
        collection = db['plasma_users']

        # Query the user by email
        query = {
            'email': email
        }
        row = collection.find_one(query)
        rows = [row] if row else []
        print(rows)

        client.close()  # Close the MongoDB connection

        return render_template("myprofile.html", rows=rows)

    if request.method == 'POST':
        try:
            name = request.form['name']
            addr = request.form['addr']
            city = request.form['city']
            pin = request.form['pin']
            bg = request.form['bg']
            email = request.form['email']
            avail = request.form['Aval']
            print(name, addr, avail)

            # Connect to MongoDB
            client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
            db = client['userlist']
            collection = db['plasma_users']

            # Update the user profile
            query = {
                'email': email
            }
            update = {
                '$set': {
                    'name': name,
                    'addr': addr,
                    'city': city,
                    'pin': pin,
                    'bg': bg,
                    'available': avail
                }
            }
            result = collection.update_one(query, update)

            client.close()  # Close the MongoDB connection

            if result.matched_count == 1:
                print("Updated")
                msg = "Successfully Updated"
            else:
                print("Not Updated")
                msg = "Not Successfully Inserted"

        except Exception as e:
            print("Error", e)
            msg = "error in insert operation"

        finally:
            flash('profile saved')
            return redirect(url_for('index'))



@app.route('/contactforblood/<emailid>', methods=('GET', 'POST'))
def contactforblood(emailid):
    if request.method == 'GET':
        fromemail = session['username']
        name = request.args.get('nm')
        addr = request.args.get('add')

        print(fromemail, emailid)

        # Connect to MongoDB
        client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
        db = client['userlist']
        collection = db['plasma_request']

        # Get the number of documents in the collection
        rows = collection.count_documents({})

        # Get the new document index
        rows += 1
        print(rows)

        # Insert a new document
        document = {
            'id': rows,
            'toemail': emailid,
            'fromemail': fromemail,
            'toname': name,
            'toaddr': addr,
            'status': 'PENDING'
        }
        result = collection.insert_one(document)

        client.close()  # Close the MongoDB connection

        if result.inserted_id:
            msg = "Successfully Inserted"
        else:
            msg = "Not Successfully Inserted"
        print(msg)
        flash('request sent')
        return redirect(url_for('index'))

    if request.method == 'POST':
        fromemail = session['username']
        name = request.form['nm']
        addr = request.form['add']

        print(fromemail, emailid)

        # Connect to MongoDB
        client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
        db = client['userlist']
        collection = db['plasma_request']

        # Get the number of documents in the collection
        rows = collection.count_documents({})

        # Get the new document index
        rows += 1
        print(rows)

        # Insert a new document
        document = {
            'id': rows,
            'toemail': emailid,
            'fromemail': fromemail,
            'toname': name,
            'toaddr': addr,
            'status': 'PENDING'
        }
        result = collection.insert_one(document)

        client.close()  # Close the MongoDB connection

        if result.inserted_id:
            msg = "Successfully Inserted"
        else:
            msg = "Not Successfully Inserted"
        print(msg)
        flash('request sent')
        return redirect(url_for('index'))



@app.route('/notifications',methods=('GET','POST'))
def notifications():
    if request.method == 'GET':
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
        db = client['userlist']
        collection = db['plasma_request']

        # Find documents matching the query
        query = {'toemail': session['username']}
        rows = collection.find(query)

        notify = []
        for row in rows:
            notify.append(row)
        notify.reverse()
        print(notify)

        client.close()  # Close the MongoDB connection

        if not notify:
            return render_template('notifications.html')
        else:
            return render_template('notifications.html', rows=notify)


@app.route('/notifyusers',methods=('GET','POST'))
def notifyusers():
    if request.method == 'GET':
        # Connect to MongoDB
        client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
        db = client['userlist']
        collection = db['plasma_request']

        # Find documents matching the query
        query = {'fromemail': session['username']}
        rows = collection.find(query)

        notify = []
        for row in rows:
            notify.append(row)
        notify.reverse()

        client.close()  # Close the MongoDB connection

        if not notify:
            return render_template('notifications.html')
        else:
            return render_template('notifications.html', rows=notify)



@app.route('/changestatus/<emailID>')
def changestatus(emailID):
    id = emailID[:-1]
    status = emailID[-1]
    print(id, status)

    # Connect to MongoDB
    client = MongoClient('mongodb+srv://ashwinhiro01:plasma-donor@cluster0.mlum8kj.mongodb.net/')
    db = client['userlist']
    collection = db['plasma_request']

    # Find the document with the given ID
    query = {'id': int(id)}
    row = collection.find_one(query)
    print(row)

    try:
        if row['status'] is None or row['status'] == 'PENDING':
            if status == 'A':
                print('A')
                collection.update_one(query, {'$set': {'status': 'Accepted'}})
            else:
                print('R')
                collection.update_one(query, {'$set': {'status': 'Rejected'}})
    except Exception as e:
        print(e)
        client.close()  # Close the MongoDB connection
        return render_template("notifications.html")

    client.close()  # Close the MongoDB connection
    return redirect(url_for('notifications'))








if __name__ == '__main__':
    app.run(debug=True)
