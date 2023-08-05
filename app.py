from flask import Flask, render_template, request, redirect, url_for, jsonify, json, Response, session, g, flash, request, make_response
from sqlalchemy import create_engine, and_, text,func,distinct
from sqlalchemy.orm import sessionmaker, exc, join
from sqlalchemy.sql import exists
from dbsetup import *
import hashlib
from os import urandom
from datetime import datetime
import random 

app = Flask(__name__)

engine = create_engine('sqlite:///shg.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
dbsession = DBSession()
userID={'id':''}

# compare credentials with database
def check_password(hashed_password, user_password, salt):
    return hashed_password == hashlib.sha256((user_password.encode()) + salt).hexdigest()


def validate(username, password, role):
    completion = False
    users = dbsession.query(Users)
    # print(users)
    for user in users:
        print(user.role,role)
        if user.username == username and user.verified and user.role == role:
            completion = check_password(user.password, password, user.salt)
            userID['id'] = user.id if completion else completion
    return completion

# sign in user
@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        session.pop('user', None)
        session.pop('role', None)
        session.pop('id', None)
        uname = request.form['username']
        pword = request.form['password']
        role = request.form['role'].lower()
        completion = validate(uname, pword,role)
        print(completion)
        if completion == True:
            session['user'] = uname # create user session
            session['role'] = role
            session['id'] = userID['id']
            # session['id'] = user_id
            # print(session)
            return redirect(url_for('main'))
        else:
            error = 'Invalid Credentials. Please try again.'
    return render_template('signin.html', error=error)

# sign up user
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    message = None
    if request.method == 'POST':
        session.pop('user', None)
        session.pop('role', None)
        session.pop('id', None)
        uname = request.form['username']
        pword = request.form['password']
        phone = request.form['phone']
        address = request.form['address']

        salt = urandom(8)
        hash_object = hashlib.sha256(pword.encode() + salt)
        new_user = Users(username=uname, password=hash_object.hexdigest(), address=address, phone=int(phone),role='user',salt=salt,verified=False)
        dbsession.add(new_user)
        dbsession.commit()
        account = Account(account_no = int(random.random()*pow(10,6)),user_id=new_user.id,account_type='user',balance=3000,status='active',created_at = datetime.now())
        dbsession.add(account)
        dbsession.commit()
        message = 'Your Credentials are being Verified. Please wait.'
    return render_template('signup.html', message=message)


@app.route('/', methods=['GET', 'POST'])
def main():
    if g.user: # check for user session
        if g.role == 'admin':
            return render_template('admin.html')
        elif g.role  == 'user':
            return render_template('index.html')
    return redirect(url_for('signin'))


@app.route('/approve/', methods=['GET', 'POST'])
def approve():
    if g.user: # check for user session
        users = dbsession.query(Users).filter(Users.verified == False).all()
        if request.method == 'POST':
            verifed_id = request.form['user_id']
            if not len(dbsession.query(Approver.id).filter(Approver.user_id == verifed_id,Approver.approver_id == g.id).all()) > 0 :
                new_approval = Approver( user_id=int(verifed_id), approver_id = int(g.id) ,approved_on=datetime.now())
                dbsession.add(new_approval)
                dbsession.commit()
                approved = dbsession.query(Approver.user_id).group_by(Approver.user_id).having(func.count(Approver.user_id) > 4).all() 
                if len(approved)>0:
                    for item in approved:
                        user = int(*item)
                        dbsession.query(Users).filter(Users.id == user).update({Users.verified : True},synchronize_session=False)
                        dbsession.commit()
        return render_template('approve.html',approves=users)
    return redirect(url_for('signin'))


# delete session
@app.route('/signout/')
def signout():
    session.pop('user', None)
    session.pop('role', None)
    session.pop('id', None)
    return redirect(url_for('main'))


# create user session
@app.before_request
def before_request():
    g.user = None
    g.role = None
    g.id = None
    if 'user' in session:
        g.user = session['user']
        g.role = session['role']
        g.id = session['id']



if __name__ == '__main__':
    app.secret_key = "\xc2\x0f\xdc\x9d0\x10A\xfa:DO\xcf\xa8%\xf0\x8e\xc1\xcb=\xf8$\xaa\xc8\xfb"
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000,threaded=False)