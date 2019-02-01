#!/usr/bin/env python3
#
# Author: Matt Vulich
#
# Creation Date: 2019-01-04
#
##############################################################################
from flask import Flask, render_template, request, redirect
from flask import url_for, jsonify, flash
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
#from flask_httpauth import HTTPBasicAuth
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import sessionmaker
import psycopg2

app = Flask(__name__)
#auth = HTTPBasicAuth()

'''CLIENT_ID = json.loads(open('/var/www/fullstack-nanodegree-vm/vagrant/catalog/client_secrets.json', 'r')
                       .read())['web']['client_id']'''

APPLICATION_NAME = "Catalog-Project"

engine = create_engine('postgresql://catalog:password@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Directs to main catalog page


@app.route('/')
@app.route('/catalogs/')
def catalogs():
    access_token = login_session.get('access_token')
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    categories = session.query(Category)
    categories_count = session.query(Category).count()
    items = session.query(CategoryItem).order_by(desc(CategoryItem.id))\
        .limit(categories_count)
    if 'username' not in login_session:
        return render_template('publicCatalog.html',
                               categories=categories, items=items)
    else:
        return render_template('catalog.html',
                               categories=categories, items=items)

# Directs to login page using OAuth2.0


@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validating the state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtaining the authorization code
    code = request.data

    '''try:
        # Need to upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response'''

    # Validating the access token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # Abort if any errors in the access token
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verifying if the access token is for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verifying that the access token is valid for this app
    '''if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response'''

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json
                                 .dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Storing the accesses token for future use
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Grabing user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # If user does not exist create a new one
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
    output += ' " style = "width: 300px; height: 300px;\
        border-radius: 150px;-webkit-border-radius:\
        150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
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
    except IOerror:
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
    print (url)
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
        return redirect('/')
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Directs to specific category page


@app.route('/catalogs/<string:category_name>/items/')
def catalogCategory(category_name):
    categories = session.query(Category)
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(CategoryItem).filter_by(category_id=category.id)
    num_items = items.count()
    if num_items == 0 or num_items > 1:
        item_string = 'items'
    else:
        item_string = 'item'
    return render_template('items.html', category=category, items=items,
                           num_items=num_items, item_string=item_string,
                           categories=categories)

# Directs to specific item description page


@app.route('/catalogs/<string:category_name>/items/<string:item_name>/')
def catalogItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(CategoryItem)\
        .filter_by(name=item_name, category_id=category.id).first()
    # If user is not logged in they are directed to the public page
    if 'username' not in login_session:
        return render_template('publicItemDescription.html', item=item)
    elif item is not None:
        return render_template('item_description.html', item=item)
    else:
        return "Item Does not Exist!"

# Directs to add a new item page


@app.route('/catalogs/new/', methods=['GET', 'POST'])
def newItem():
    # Directs to login page if not logged in
    if 'username' not in login_session:
        return redirect('/login/')
    categories = session.query(Category).all()
    items = session.query(CategoryItem).all()
    if request.method == 'POST':
        category = session.query(Category)\
            .filter_by(name=request.form['category']).one()
        newItem = CategoryItem(name=request.form['name'],
                               description=request.form['description'],
                               category_id=category.id,
                               user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('catalogs'))
    else:
        return render_template('newCategoryItem.html',
                               categories=categories, items=items)

# Directs to edit an item page


@app.route('/catalogs/<string:item_name>/edit/', methods=['GET', 'POST'])
def editItem(item_name):
    # Directs to login page if not logged in
    if 'username' not in login_session:
        return redirect('/login/')
    editedItem = session.query(CategoryItem)\
        .filter_by(name=item_name).first()
    category = session.query(Category)\
        .filter_by(id=editedItem.category_id).one()
    categories = session.query(Category).all()
    # Determines if user has access to edit item and sends error if not
    if login_session['user_id'] != editedItem.user_id:
        return "<script>function myFunction()\
            {alert('You are not authorized to edit this item.\
            Please create your own item at http://localhost:8000/catalogs/new\
            in order to edit');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newCategory = session.query(Category)\
            .filter_by(name=request.form['category']).one()
        editedItem.category_id = newCategory.id
        editedItem.name = request.form['name']
        editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('catalogCategory',
                                category_name=newCategory.name))
    else:
        return render_template('editCategoryItem.html',
                               item=editedItem, category=category,
                               item_name=item_name, categories=categories)


@app.route('/catalogs/<string:item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(item_name):
    # Directs to login page if not logged in
    if 'username' not in login_session:
        return redirect('/login/')
    deletedItem = session.query(CategoryItem)\
        .filter_by(name=item_name).first()
    category = session.query(Category)\
        .filter_by(id=deletedItem.category_id).one()
    # Determines if user has access to delete item and sends error if not
    if login_session['user_id'] != deletedItem.user_id:
        return "<script>function myFunction()\
        {alert('You are not authorized to delete this item.\
        Please create your own item at http://localhost:8000/catalogs/new/\
        in order to delete it.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('catalogCategory',
                                category_name=category.name))
    else:
        return render_template('deleteCategoryItem.html',
                               item_name=item_name, item=deletedItem,
                               category=category)


@app.route('/catalogs/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).order_by(asc(Category.name))
    return jsonify(categories=[c.serialize for c in categories])


@app.route('/catalogs/items/JSON')
def itemsJSON():
    items = session.query(CategoryItem).order_by(asc(CategoryItem.name))
    return jsonify(items=[i.serialize for i in items])


if __name__ == '__main__':
    app.secret_key = 'catalog_secret_key'
    app.debug = True
    app.run(host='3.92.192.125', port=80)
