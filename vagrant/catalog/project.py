#!/usr/bin/env python3

import random
import string
import httplib2
import json
import requests
import time
from functools import update_wrapper

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response, g
from flask import session as login_session

from flask_httpauth import HTTPBasicAuth
from flask_login import *

from redis import Redis

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from setup_database import Base, CharacterClass, GameVersion, Build, User, Favorite, secret_key

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

auth = HTTPBasicAuth()
login_manager = LoginManager()
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///pathofexile.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
login_manager.init_app(app)
login_manager.login_view = "show_login"
redis = Redis()


""" Used to limit the amount of requests in a small period of time """
class RateLimit(object):
    expiration_window = 10

    def __init__(self, key_prefix, limit, per, send_x_headers):
        self.reset = (int(time.time()) // per) * per + per
        self.key = key_prefix + str(self.reset)
        self.limit = limit
        self.per = per
        self.send_x_headers = send_x_headers
        p = redis.pipeline()
        p.incr(self.key)
        p.expireat(self.key, self.reset + self.expiration_window)
        self.current = min(p.execute()[0], limit)

    remaining = property(lambda x: x.limit - x.current)
    over_limit = property(lambda x: x.current >= x.limit)


def get_view_rate_limit():
    return getattr(g, '_view_rate_limit', None)


def on_over_limit(limit):
    return (jsonify({'data':'You hit the rate limit','error':'429'}),429)


def ratelimit(limit, per=300, send_x_headers=True,
              over_limit=on_over_limit,
              scope_func=lambda: request.remote_addr,
              key_func=lambda: request.endpoint):
    def decorator(f):
        def rate_limited(*args, **kwargs):
            key = 'rate-limit/%s/%s/' % (key_func(), scope_func())
            rlimit = RateLimit(key, limit, per, send_x_headers)
            g._view_rate_limit = rlimit
            if over_limit is not None and rlimit.over_limit:
                return over_limit(rlimit)
            return f(*args, **kwargs)
        return update_wrapper(rate_limited, f)
    return decorator


@app.after_request
def inject_x_rate_headers(response):
    limit = get_view_rate_limit()
    if limit and limit.send_x_headers:
        h = response.headers
        h.add('X-RateLimit-Remaining', str(limit.remaining))
        h.add('X-RateLimit-Limit', str(limit.limit))
        h.add('X-RateLimit-Reset', str(limit.reset))
    return response


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


@login_manager.request_loader
def load_user_from_request(request):
    token = request.headers.get('Authorization')
    if token:
        token = token.replace('Basic ', '', 1)

    elif request.json:
        token = request.json.get("token")
        user_id = User.verify_auth_token(token)

    if user_id:
        user_id = User.verify_auth_token(token)
        if user_id:
            return get_user(user_id)

    return None


@app.route('/')
@app.route('/buildfinder/')
def show_home():
    latest_builds = session.query(Build).order_by(Build.time_updated.desc()).limit(5)
    return render_template('home.html', latest_builds=latest_builds)


@app.route('/buildfinder/login/')
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    next_url = request.args.get('next')
    if next_url:
        return render_template('login.html', STATE=state, next_url=next_url)
    else:
        return render_template('login.html', STATE=state, next_url=url_for('show_home'))


@app.route('/buildfinder/search', methods=['POST', 'GET'])
def show_search():
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


@app.route('/buildfinder/add', methods=['POST', 'GET'])
@login_required
def add_build():
    if request.method == 'POST':
        build = add_build()
        if build:
            return redirect(url_for('show_build', build_id=build.id))

    character_classes = session.query(CharacterClass).all()
    versions = session.query(GameVersion).order_by(GameVersion.name.desc())
    return render_template('addbuild.html', character_classes=character_classes, versions=versions)


@app.route('/buildfinder/<int:build_id>')
def show_build(build_id):
    build = get_build(build_id)
    creator_id = build.user.id
    is_favorite = False

    if not current_user.is_anonymous:
        # Returns true if build/user exists in favorites list
        if session.query(
                session.query(Favorite).filter_by(build_id=build_id, user_id=current_user.id).exists()
        ).scalar():
            is_favorite = True

    return render_template('showbuild.html', build=build, creator_id=creator_id, is_favorite=is_favorite)


@app.route('/buildfinder/<int:build_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_build(build_id):
    build = session.query(Build).filter_by(id=build_id).one()
    character_classes = session.query(CharacterClass).all()
    versions = session.query(GameVersion).order_by(GameVersion.name.desc())

    if request.method == 'POST':
        edit_build(build_id)
        return redirect(url_for('show_build', build_id=build_id))

    else:
        return render_template('editbuild.html', build=build, versions=versions, character_classes=character_classes)


@app.route('/buildfinder/<int:build_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_build(build_id):
    if request.method == 'POST':
        if delete_build(build_id):
            return redirect(url_for('show_home'))

    build = get_build(build_id)
    return render_template('deletebuild.html', build=build)


@app.route('/favorites/')
@login_required
def show_favorites():
    favorites = session.query(Favorite).filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', favorites=favorites)


@app.route('/buildfinder/<int:build_id>/favorite')
@login_required
def make_favorite(build_id):
    if login_session.get('user_id'):
        favorite = Favorite(user_id=login_session.get('user_id'), build_id=build_id)
        session.add(favorite)
        session.commit()

        flash('Build added to favorites')
        return redirect(url_for('show_build', build_id=build_id))
    else:
        flash('Please login for this feature')
        return redirect(url_for('show_build', build_id=build_id))


@app.route('/oauth/google', methods=['POST'])
def login_google():
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
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id

    user = session.query(User).filter_by(id=user_id).first()
    login_user(user, remember=True)

    token = current_user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route("/logout")
def logout():
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
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Logged out")
        logout_user()
        return show_home()

    else:
        flash('Failed to revoke token for given user.')
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/buildfinder/api/v1/token')
@login_required
def get_auth_token():
    token = current_user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route("/buildfinder/api/v1/builds", methods=['GET', 'POST'])
@login_required
def api_builds_function():
    if request.method == 'GET':
        builds = session.query(Build).all()
        return jsonify(json_list=[build.serialize for build in builds])

    elif request.method == 'POST':
        if add_build():
            return jsonify(success="true")
        return jsonify(success="false")



@app.route("/buildfinder/api/v1/build/<int:build_id>", methods=['GET', 'PUT', 'DELETE'])
@login_required
def api_build_function(build_id):
    if request.method == 'GET':
        build = get_build(build_id)
        return jsonify(json_list=[build.serialize])

    elif request.method == 'DELETE':
        if delete_build(build_id):
            return jsonify(success="true")
        return jsonify(success="false")

    elif request.method == 'PUT':
        if edit_build(build_id):
            return jsonify(success="true")
        return jsonify(success="false")


def add_build():
    if not request.json:
        build = Build(title=request.form['title'], url=request.form['url'],
                      short_description=request.form['short_description'],
                      long_description=request.form['long_description'],
                      character_class_name=request.form['character_class'],
                      game_version=request.form['version'],
                      user_id=current_user.id,
                      author=request.form['author'])

    else:
        if request.json:
            title = request.json.get("title")
            url = request.json.get("url")
            short_description = request.json.get("short_description")
            long_description = request.json.get("long_description")
            character_class_name = request.json.get("character_class")
            game_version = request.json.get("version")
            user_id = current_user.id
            author = request.json.get("author")

            build = Build(title=title, url=url, short_description=short_description, long_description=long_description,
                          character_class_name=character_class_name, game_version=game_version, user_id=user_id,
                          author=author)

    session.add(build)
    session.commit()
    flash('Build Added')
    return build


def delete_build(build_id):
    build = session.query(Build).filter_by(id=build_id).one()
    if current_user.id == build.user_id:
        session.delete(build)
        session.commit()
        flash('Build deleted')
        return True
    else:
        flash('Only build submitter can delete the build')
        return False


def get_build(build_id):
    return session.query(Build).filter_by(id=build_id).one()


def edit_build(build_id):
    build = session.query(Build).filter_by(id=build_id).one()

    if not request.json:
        if current_user.id == build.user_id:
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

            session.commit()
            flash('Build edited')
            return True

    else:
        data = request.json
        if data and current_user.id == build.user_id:
            if request.json.get("title"):
                build.title = request.json.get("title")
            if request.json.get("character_class_name"):
                build.character_class_name = request.json.get("character_class_name")
            if request.json.get("short_description"):
                build.short_description = request.json.get("short_description")
            if request.json.get("long_description"):
                build.long_description = request.json.get("long_description")
            if request.json.get("url"):
                build.url = request.json.get("url")
            if request.json.get("game_version"):
                build.game_version = request.json.get("game_version")
            if request.json.get("author"):
                build.author = request.json.get("author")

            session.commit()
            return True

    flash('Only build submitter can edit the build')
    return False


def create_user(login_session):
    new_user = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def get_user(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except NoResultFound:
        return None


def get_user_id(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except NoResultFound:
        return None


if __name__ == '__main__':
    app.secret_key = secret_key
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
