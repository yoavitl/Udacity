from flask import Flask, render_template, url_for, request, redirect, flash
from flask import Response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Team, Player, User
# imports for the login section
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


# Create the app and opens the connection to the DB
app = Flask(__name__)

engine = create_engine('sqlite:///premierleague.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

""" this is the login section, most of code here produced thanks to the udactiy
course and google api instructions."""
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "English Premier League"


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', state=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    request.get_data()
    code = request.data.decode('utf-8')

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

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),  # noqa
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # after the user login return this answer.
    Answerpage = ''
    Answerpage += '<h1>Welcome, '
    Answerpage += login_session['username']
    Answerpage += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    return Answerpage


# This function add a user to the database
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'])  # noqa
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


# This function return an object of a user
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


# This function returns user id
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# This function responsible for the disconnet of a user
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('credentials')
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)  # noqa
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['credentials']
        del login_session['username']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("you are now logged out")
        return redirect("http://localhost:5000/", code=302)
        login_session.clear()
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))  # noqa
        response.headers['Content-Type'] = 'application/json'
        return response


# This is the homepage function
@app.route('/')
@app.route('/home')
def LeagueHP():
    team = session.query(Team).all()
    # if the user is logged in show the page with logut button, else show login
    if 'username' not in login_session:
        return render_template('connect.html', team=team)
    else:
        return render_template('disconnect.html', team=team)


# This function responsibale for the team page
@app.route('/Team/<int:team_id>/')
def TeamPage(team_id):
    team = session.query(Team).filter_by(id=team_id).one()
    players = session.query(Player).filter_by(team_id=team_id).all()
    if 'username' not in login_session:
        return render_template('ReadOnly.html', team=team, players=players)
    else:
        return render_template('EditDelete.html', team=team, players=players)


# This function responsible for adding a new player (item) to the team
@app.route('/Team/<int:team_id>/newitem', methods=['GET', 'POST'])
def newPlayer(team_id):
    if request.method == 'POST':
        newPlayer = Player(name=request.form['name'], description=request.form[
                           'description'], position=request.form['position'], image=request.form['imageURL'], user_id=login_session['user_id'], team_id=team_id)  # noqa
        session.add(newPlayer)
        session.commit()
        flash("new Player has been added!")
        return redirect(url_for('TeamPage', team_id=team_id))
    else:
        return render_template('newplayer.html', team_id=team_id)


# This funtion is responsible for editing a player.
@app.route('/Team/<int:team_id>/<int:player_id>/editplayer', methods=['GET', 'POST'])  # noqa
def editPlayer(team_id, player_id):
    editedPLayer = session.query(Player).filter_by(id=player_id).one()
    oldName = editedPLayer.name
    # check that the user have authoriztion to edit the player
    if editedPLayer.user_id != login_session['user_id']:
        return "<script>function editalert() {alert('You are not the owner of this player. you are now redircted to the team page.'); window.location = '../';}</script><body onload='editalert()''>"  # noqa
    if request.method == 'POST':
        if request.form['name']:
            editedPLayer.name = request.form['name']
        elif request.form['imageURL']:
            editedPLayer.image = request.form['imageURL']
        session.add(editedPLayer)
        session.commit()
        flash("The Player %s has changed to %s" % (oldName, editedPLayer.name))
        return redirect(url_for('TeamPage', team_id=team_id))
    else:
        return render_template(
            'editplayer.html', team_id=team_id, player_id=player_id, player=editedPLayer)  # noqa


# this function is for deleting a player from the DB
@app.route('/Team/<int:team_id>/<int:player_id>/deleteplayer', methods=['GET', 'POST'])  # noqa
def DeletePlayer(team_id, player_id):
    # check that the user have authoriztion to delete the player
    DeletePLayer = session.query(Player).filter_by(id=player_id).one()
    if DeletePLayer.user_id != login_session['user_id']:
        return "<script>function deletealert() {alert('You can only delete a player that you created!'); window.location = '../';}</script><body onload='deletealert()''>"  # noqa
    if request.method == 'POST':
        session.query(Player).filter_by(id=player_id).delete()
        session.commit()
        flash("The Player %s have been deleted" % DeletePLayer.name)
        return redirect(url_for('TeamPage', team_id=team_id))
    else:
        return render_template('deleteplayer.html', team_id=team_id, DeletePLayer=DeletePLayer)  # noqa


# this function manifest the JSON of a Team
@app.route('/Team/<int:team_id>/JSON')
def TeamPageJson(team_id):
    team = session.query(Team).filter_by(id=team_id).all()
    return jsonify(team=[i.serialize for i in team])


# this function emanifest the JSON of a player
@app.route('/Team/<int:team_id>/<int:player_id>/JSON')
def TeamPlayerJson(team_id, player_id):
    team = session.query(Team).filter_by(id=team_id).one()
    players = session.query(Player).filter_by(id=player_id).all()
    return jsonify(players=[i.serialize for i in players])


# This function manifest XML of the entire league
@app.route('/xml')
def ajax_ddl():
    teams = session.query(Team).all()
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<league>'
    for team in teams:
        xml += '''<Team>
                \t<id>{0}</id>
                \t<name>{1}</name>
                \t<location>{2}</location>
                \t<symbol>{3}</symbol>
                </Team>\n'''.format(team.id, team.name, team.location, team.symbol)  # noqa
    xml += '</league>'
    return Response(xml, mimetype='text/xml')


"""
This Part of code enables also API endpoit of atom feed, but because of atom
beind with mandatory fiels like article etc.. i didn't included it to the users
but you can uncomment it and look at the ATOM feed, it works great as well :)


from urlparse import urljoin
from flask import request
from werkzeug.contrib.atom import AtomFeed
import datetime

def make_external(url):
    return urljoin(request.url_root, url)


@app.route('/recent.atom')
def recent_feed():
    feed = AtomFeed('Recent Articles',
                    feed_url=request.url, url=request.url_root)
    articles = session.query(Team).all()
    for article in articles:
        feed.add(id = article.id,
                 content_type='html',
                 author=article.name,
                 title=article.name,
                 updated=datetime.date.today())
    return feed.get_response()
"""


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
