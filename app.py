from sqlalchemy import create_engine, and_, text,func,distinct
from flask import Flask ,render_template, request, redirect, url_for, jsonify, json, Response, session, flash, request, make_response
from sqlalchemy.orm import sessionmaker, exc, join
from sqlalchemy.sql import exists
from dbsetup import *
import hashlib
from os import urandom
from datetime import datetime,timedelta
import random

app = Flask(__name__)

engine = create_engine('sqlite:///shg.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
dbsession = DBSession()
userID={'id':''}
minimun_requirement = 0

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

def transaction(from_user,to_user,amount):
    total_amount = int(''.join([str(*i) for i in (dbsession.query(Account.balance).filter(Account.user_id == from_user).all())]))
    print(f'the acc amt is {total_amount}',type(total_amount))
    if total_amount > amount:
        from_acc = ''.join([str(*i) for i in (dbsession.query(Account.account_no).filter(Account.user_id == from_user).all())])
        to_acc = ''.join([str(*i) for i in (dbsession.query(Account.account_no).filter(Account.user_id == to_user).all())])

        new_trans = Fin_trans(user_acc = from_user, created_on=datetime.now(), transaction_amount = amount, transaction_from=from_acc ,transaction_to=to_acc)
        dbsession.add(new_trans)
        dbsession.query(Account).filter(Account.user_id == from_user).update({Account.balance :Account.balance - amount },synchronize_session=False)
        dbsession.query(Account).filter(Account.user_id == to_user).update({Account.balance :Account.balance + amount },synchronize_session=False)
        dbsession.commit()
        return True
    return False

def check_user_balance(user_id,amount):
    user_amount = int(''.join([str(*i) for i in (dbsession.query(Account.balance).filter(Account.user_id == user_id)) ]))
    return(user_amount > amount)

def check_bank_balance_for(req_id):
    total_bank_amount = int(''.join([str(*i) for i in (dbsession.query(Account.balance).filter(Account.user_id == 1).all())]))
    request_amount = int(''.join([str(*i) for i in (dbsession.query(Loan_request.amount).filter(Loan_request.id==req_id)) ]))
    return(total_bank_amount > request_amount)

# sign in user
@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        try:
            session.clear()
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
        except:
            dbsession.rollback()
            print("An exception occurred")
    return render_template('signin.html', error=error)

# sign up user
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    message = None
    if request.method == 'POST':
        try:
            session.clear()
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
        except:
            dbsession.rollback()
            print("An exception occurred")
            message = 'Number taken. Please sign up with different phone number'
    return render_template('signup.html', message=message)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('know.html')


@app.route('/', methods=['GET', 'POST'])
def main():
    if 'user' in session: # check for user session
        
        if session['role'] == 'admin':
            account=dbsession.query(Account).filter(Account.user_id == session['id'])
            users=dbsession.query(Users)
            return render_template('admin.html',account=account,users=users)
        elif session['role']  == 'user':
            account=dbsession.query(Account).filter(Account.user_id == session['id'])
            users=dbsession.query(Users).filter(Users.id == session['id'])

            return render_template('index.html', account=account, users=users)
    return redirect(url_for('about'))


@app.route('/approve/', methods=['GET', 'POST'])
def approve():
    if 'user' in session: # check for user session
        users = dbsession.query(Users).filter(Users.verified == False).all()
        if request.method == 'POST':
            try:
                verifed_id = request.form['user_id']
                # User can only be approved once
                if not len(dbsession.query(Approver.id).filter(Approver.user_id == verifed_id, Approver.approver_id == session['id']).all()) > 0 :
                    new_approval = Approver( user_id=int(verifed_id), approver_id = int(session['id']) ,approved_on=datetime.now())
                    dbsession.add(new_approval)
                    dbsession.commit()
                    approved = dbsession.query(Approver.user_id).group_by(Approver.user_id).having(func.count(Approver.user_id) > minimun_requirement).all() 
                    if len(approved)>0:
                        for item in approved:
                            user = int(*item)
                            dbsession.query(Users).filter(Users.id == user).update({Users.verified : True},synchronize_session=False)
                            dbsession.commit()
                            transaction(user, 1, 2000)
            except:
                dbsession.rollback()
                print("An exception occurred")
        return render_template('approve.html',approves=users)
    return redirect(url_for('about'))


# delete session
@app.route('/signout/')
def signout():
    session.clear()
    return redirect(url_for('main'))




if __name__ == '__main__':
    app.secret_key = "\xc2\x0f\xdc\x9d0\x10A\xfa:DO\xcf\xa8%\xf0\x8e\xc1\xcb=\xf8$\xaa\xc8\xfb"
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000,threaded=False)