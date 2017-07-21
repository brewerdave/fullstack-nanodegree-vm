#!/usr/bin/env python3

import random
import string
import httplib2
import json
import requests

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response, g
from flask import session as login_session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from setup_database import Base, CharacterClass, GameVersion, Build, User, Favorite

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///pathofexile.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.before_request
def checkLoginStatus():
    g.logged_in = False
    g.user = None
    if login_session.get('username'):
        g.user = getUser(login_session.get('user_id'))
        if g.user:
            g.logged_in = True



@app.route('/')
@app.route('/builds/')
def showHome():
    latest_builds = session.query(Build).order_by(Build.time_updated.desc()).limit(5)
    return render_template('home.html', latest_builds=latest_builds)


@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/builds/search', methods=['POST', 'GET'])
def showSearch():
    character_classes = session.query(CharacterClass).all()
    versions = session.query(GameVersion).order_by(GameVersion.name.desc())
    authors = session.query(Build.author).distinct()
    results = []

    if request.method == 'POST':
        query = session.query(Build)

        if request.form.get('title') is not None:
            query = query.filter(Build.title.contains(request.form['title']))
        if request.form.get('character_class') is not None:
            query = query.filter_by(character_class_name=request.form['character_class'])
        if request.form.get('version') is not None:
            query = query.filter_by(game_version=request.form['version'])
        if request.form.get('author') is not None:
            query = query.filter_by(game_version=request.form['author'])

        if request.form.get('sort') == 'Date Updated':
            results = query.order_by(Build.time_updated.desc()).all()
        else:
            results = query.order_by(Build.time_created.desc()).all()

    return render_template('search.html', character_classes=character_classes, versions=versions,
                           results=results, authors=authors)


@app.route('/builds/add', methods=['POST', 'GET'])
def addBuild():
    if request.method == 'POST':
        if request.form['title'] and request.form['url'] and request.form['short_description'] \
                and request.form['long_description'] and request.form['character_class'] \
                and request.form['version'] and request.form['author']:
            build = Build(title=request.form['title'], url=request.form['url'],
                          short_description=request.form['short_description'],
                          long_description=request.form['long_description'],
                          character_class_name=request.form['character_class'],
                          game_version=request.form['version'],
                          user_id=login_session['user_id'],
                          author=login_session['author'])
            session.add(build)
            session.commit()
            flash("Build added")

        return redirect(url_for('showBuild', character_class_name=build.character_class_name, build_id=build.id))
    else:
        character_classes = session.query(CharacterClass).all()
        versions = session.query(GameVersion).order_by(GameVersion.name.desc())
        return render_template('addbuild.html', character_classes=character_classes, versions=versions)


@app.route('/builds/<string:character_class_name>/<string:build_id>')
def showBuild(build_id, character_class_name):
    build = session.query(Build).filter_by(id=build_id).one()
    creator_id = build.user.id
    is_favorite = False

    if g.logged_in:
        if session.query(
                session.query(Favorite).filter_by(build_id=build_id, user_id=g.user.id).exists()
        ).scalar():
            is_favorite = True

    return render_template('showbuild.html', build=build, creator_id=creator_id, is_favorite=is_favorite)


@app.route('/builds/<string:character_class_name>/<string:build_id>/edit', methods=['GET', 'POST'])
def editBuild(build_id, character_class_name):
    build = session.query(Build).filter_by(id=build_id).one()
    character_classes = session.query(CharacterClass).all()
    versions = session.query(GameVersion).order_by(GameVersion.name.desc())

    if request.method == 'POST':
        if g.logged_in and g.user.id == build.user_id:
            if request.form['title']:
                build.title = request.form['title']
            if request.form['character_class_name']:
                build.character_class_name = request.form['character_class_name']
            if request.form['short_description']:
                build.short_description = request.form['short_description']
            if request.form['long_description']:
                build.long_description = request.form['long_description']
            if request.form['url']:
                build.url = request.form['url']
            if request.form['game_version']:
                build.game_version = request.form['game_version']
            if request.form['author']:
                build.author = request.form['author']

            flash("Build edited")
            return redirect(url_for('showBuild', build_id=build_id, character_class_name=character_class_name))

        else:
            flash("Must be logged in as user that created build")
            return redirect(url_for('showBuild', character_class_name=character_class_name, build_id=build_id))

    else:
        return render_template('editbuild.html', build=build, character_classes=character_classes, versions=versions)


@app.route('/builds/<string:character_class_name>/<string:build_id>/delete', methods=['GET', 'POST'])
def deleteBuild(build_id, character_class_name):
    build = session.query(Build).filter_by(id=build_id).one()
    if request.method == 'POST':
        session.delete(build)
        session.commit()
        flash('Build deleted')
        return redirect(url_for('showHome'))
    else:
        return render_template('deletebuild.html', build=build)


@app.route('/builds/favorites/')
def showFavorites():
    favorites = []

    if g.logged_in:
        favorites = session.query(Favorite).filter_by(user_id=g.user.id).all()
    return render_template('favorites.html', favorites=favorites)


@app.route('/builds/<string:character_class_name>/<string:build_id>/makefavorite')
def makeFavorite(build_id, character_class_name):
    if login_session.get('user_id'):
        favorite = Favorite(user_id=login_session.get('user_id'), build_id=build_id)
        session.add(favorite)
        session.commit()

        flash('Build added to favorites')
        return redirect(url_for('showBuild', build_id=build_id, character_class_name=character_class_name))
    else:
        flash('Please login for this feature')
        return redirect(url_for('showBuild', build_id=build_id, character_class_name=character_class_name))


def createUser(login_session):
    new_user = User(name=login_session['username'], email=login_session['email'],
                    picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUser(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except NoResultFound:
        return None


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except NoResultFound:
        return None


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data

    try:
        # Upgrade auth code into credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that token is used for intended use
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if user is already logged in
    stored_credentials = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    user_id = getUserID(login_session['email'])
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
    flash("You are now logged in as %s" % login_session['username'])
    return output


@app.route("/gdisconnect")
def gdisconnect():
    # See if user is connected
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Revoke current token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Logged out")
        return showHome()
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
