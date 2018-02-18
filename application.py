from flask import Flask, render_template,  # noqa
request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc  # noqa
from sqlalchemy.orm import sessionmaker  # noqa
from database_setup import Base, Category, CategoryItem, User  # noqa

from flask import session as login_session  # noqa
import random  # noqa
import string  # noqa

from oauth2client.client import flow_from_clientsecrets  # noqa
from oauth2client.client import FlowExchangeError  # noqa
import httplib2  # noqa
import json  # noqa
from flask import make_response  # noqa
import requests  # noqa

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog"

# Connect to Database and create database session
engine = create_engine('sqlite:///categoryitemswithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create a state token to prevent request forgery.
# Store it in the session for later validation.


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/logout')
def logout():

    gdisconnect()
    if login_session['credentials']:
        del login_session['credentials']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']

    return redirect(url_for('showCategories'))


@app.route('/gconnect', methods=['POST'])
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
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
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
        response = make_response(json.dumps
                                 ('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    # print 'here we assign login_session with credentials ',
    # credentials.access_token
    # print 'here we assign login_session with credentials ',
    # login_session['credentials']
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it does not make a new one
    # print "chek to see if user exists ", login_session['email']
    user_id = getUserId(login_session['email'])
    # print "user _id is ", user_id
    if not user_id:
        user_id = createUser(login_session)
        print "user _id after creating new user ", user_id
    login_session['user_id'] = user_id
    print "user _id is ", login_session['user_id']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px;"'+
            +' "height: 300px;border-radius: 150px;"'+
            +'"-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/logout')
@app.route('/gdisconnect')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps(
                'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

        print 'In gdisconnect access token is %s', credentials
        print 'User name is: '
        print login_session['username']
        url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'
                %login_session['credentials']
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        print 'result is '
        print result
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        reponse = redirect(url_for('showCategories'))
        flash("signed out Successfully")
        return response
    else:
        response = make_response(json.dumps
                                    ('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Category Information
@app.route('/category.JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    # items = session.query(Category).filter_by(category_id=category_id).all()
    return jsonify(Category=[i.serialize for i in categories])


@app.route('/category/<int:category_id>/item/JSON')
def categoryItemsJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(CategoryItem).filter_by
    (category_id=category_id).all()
    return jsonify(CategoryItems=[i.serialize for i in items])


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def categoryEachItemJSON(category_id, item_id):
    Category_Item = session.query(CategoryItem).filter_by(id=item_id).one()
    return jsonify(Category_Item=Category_Item.serialize)


# Show all categories
@app.route('/')
@app.route('/category/')
# @app.route('/categories/')
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    if 'username' not in login_session:
        return render_template('publiccategories.html', categories=categories)
    else:
        return render_template('categories.html', categories=categories)


# Create a new Category
@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    print "category new login usernmae is ", login_session['user_id']
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'],
                              user_id=login_session['user_id'])
        print "new category ", newCategory.name
        session.add(newCategory)
        flash('New Category %s Successfully Created' %
                newCategory.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')


# Edit a Category
@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    # editedCategory = session.query(Category)
    # .filter_by(name = category_id).one()
    if editedCategory.user_id != login_session['user_id']:
        return "<script>function myFunction()"+
                +"{alert('You are not authorized to edit this category. "+
                +"</script>Please create your own category in order to edit.');}"+
                +"<body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Category Successfully Edited %s' % editedCategory.name)
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category=editedCategory)


# Delete a category
@app.route('/category/<int:category_id>/delete/',
    methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if categoryToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction()"+
            +"{alert('You are not authorized to delete this category."+
            +"Please create your own category in order to delete.');}</script>"+
            +"<body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('deleteCategory.html', category=categoryToDelete)


#Show a category items
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/items/')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    users = session.query(User).all()
    print users
    print "category user_id ", category.name
    print "category user_id ", category.user_id
    creator = getUserInfo(category.user_id)
    items = session.query(CategoryItem).filter_by(
            category_id=category_id).all()
    print "in show items creator id %s", creator.id
    if 'username' not in login_session:
        print "going in login session"
    if 'username' not in login_session or
    creator.id != login_session['user_id']:
        # print "in show items if condition %s",creator.id
        # print "login session user id ", login_session['user_id']
        return render_template('publicitemlist.html',
            items=items,
            category=category)
    else:
        print "in show items else condition %s",creator.id
        print "in show items else ", login_session['username']
        return render_template('itemlist.html',
            items=items,
            category=category,
            creator=creator)


#Create a category item
@app.route('/category/<int:category_id>/item/new/',
    methods=['GET', 'POST'])
def newCategoryItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    print "categroy user id new category item", category.user_id
    print "categroy user id new category name", category.name
    if request.method == 'POST':
        newItem = CategoryItem(name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            category_id=category_id,
            user_id=category.user_id)
        # newItem = CategoryItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], category_id = category_id, user_id = login_session['user_id')
        session.add(newItem)
        session.commit()
        flash('New Category %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showItems',
            category_id=category_id))
    else:
        return render_template('newitem.html',
            category_id=category_id, category=category)


#Edit a category item
@app.route('/category/<int:category_id>/item/<int:item_id>/edit',
    methods=['GET', 'POST'])
def editCategoryItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    # editedItem = session.query(CategoryItem).filter_by(id = item_id).one()
    editedItem = session.query(CategoryItem).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        flash('Category Item Successfully Edited')
        return redirect(url_for('showItems',
            category_id=category_id))
    else:
        return render_template('edititem.html',
            category_id=category_id,
            item_id=item_id, item=editedItem)


# Delete a category item
@app.route('/category/<int:category_id>/item/<int:item_id>/delete',
    methods=['GET', 'POST'])
def deleteCategoryItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(CategoryItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Category Item Successfully Deleted')
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteitem.html', item=itemToDelete)


@app.route('/')
@app.route('/categories/<int:category_id>/')
def categoryItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    # print "category",category.id
    items = session.query(CategoryItem).filter_by(category_id=category.id)
    print items
    render = render_template('itemlist.html', category=category, items=items)
    return render


def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    newUser = User(name=login_session['username'],
            email=login_session['email'],
            picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
