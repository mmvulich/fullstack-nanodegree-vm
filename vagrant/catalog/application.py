from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
app= Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_database_setup import Base, Category, CategoryItem, User

from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog-Project"

engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Add @auth.verify_password here
'''@auth.verify_password
def verify_password(username,password):
    user = session.query(User).filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True

@app.route('/users', methods = ['POST'])
def new_user():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        if username is None or password is None:
            abort(400)
        if session.query(User).filter_by(username = username).first() is not None:
            print "existing user"
            user = session.query(User).filter_by(username=username).first()
            return jsonify({'message': 'user already exists'}), 200
        user = User(username=username)
        session.add(user)
        session.commit()
        return jsonify({'username': user.username}), 201

@app.route('/user/<int:id>')
def get_user(id):
    user = session.query(User).filter_by(id=id).one()
    if not user:
        abort(400)
    return jsonify({'username', : user.username})

@app.route('/resource')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s' % g.user.username})'''
        

#Directs to main catalog page
@app.route('/')
@app.route('/catalogs/')
def catalogs():
    categories = session.query(Category)
    items = session.query(CategoryItem)
    return render_template('catalog.html', categories = categories, items = items)

#Directs to login page using OAuth2.0
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) 
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)

@app.route('/gconnect', methods = ['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        #print credentials
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    #print url
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions



def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id



def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user



def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
        # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response   

#Directs to specific category page

@app.route('/catalogs/<string:category_name>/items/')
def catalogCategory(category_name):
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(CategoryItem).filter_by(category_id = category.id)
    return render_template('items.html', category = category, items = items)

#Directs to specific item description page
@app.route('/catalogs/<string:category_name>/items/<string:item_name>/')
def catalogItem(category_name, item_name):
    category = session.query(Category).filter_by(name = category_name).one()
    item = session.query(CategoryItem).filter_by(name = item_name, category_id = category.id).first()
    if item != None:
        return render_template('item_description.html', item = item)
    else:
        return "Item Does not Exist!"

#Directs to add a new item page
@app.route('/catalogs/new/', methods = ['GET', 'POST'])
def newItem():
    if 'username' not in login_session:
        return redirect('/login/')
    categories = session.query(Category).all()
    items = session.query(CategoryItem).all()
    if request.method == 'POST':
        category = session.query(Category).filter_by(name = request.form['category']).one()
        newItem = CategoryItem(name = request.form['name'],
                              description= request.form['description'],
                              category_id = category.id,
                              user_id = login_session['user_id'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('catalogs'))
    else:
        return render_template('newCategoryItem.html', categories = categories, items = items)

#Directs to edit an item page
@app.route('/catalogs/<int:item_id>/edit/', methods = ['GET', 'POST'])
def editItem(item_id):
    if 'username' not in login_session:
        return redirect('/login/')
    editedItem = session.query(CategoryItem).filter_by(id = item_id).first()
    category = session.query(Category).filter_by(id = editedItem.category_id).one()
    categories = session.query(Category).all()
    if login_session['user_id'] != editedItem.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this item. Please create your own item at http://localhost:8000/catalogs/new in order to edit');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newCategory = session.query(Category).filter_by(name = request.form['category']).one()
        editedItem.category_id = newCategory.id
        editedItem.name = request.form['name']
        editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('catalogCategory', category_name = newCategory.name))
    else:
        return render_template('editCategoryItem.html', item = editedItem, category = category, item_id = item_id, categories = categories)

@app.route('/catalogs/<int:item_id>/delete/', methods = ['GET', 'POST'])
def deleteItem(item_id):
    if 'username' not in login_session:
        return redirect('/login/')
    deletedItem = session.query(CategoryItem).filter_by(id = item_id).first()
    category = session.query(Category).filter_by(id = deletedItem.category_id).one()
    if login_session['user_id'] != deletedItem.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this item. Please create your own item at http://localhost:8000/catalogs/new/ in order to delete it.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('catalogCategory', category_name = category.name))
    else:
        return render_template('deleteCategoryItem.html', item_id = item_id, item = deletedItem, category = category)




if __name__ == '__main__':
    app.secret_key = 'catalog_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)