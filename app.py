<<<<<<< HEAD
from sqlalchemy import create_engine, and_, text,func,distinct, or_
=======
from sqlalchemy import create_engine, and_, text,func,distinct
>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef
from flask import Flask ,render_template, request, redirect, url_for, jsonify, json, Response, session, flash, request, make_response
from sqlalchemy.orm import sessionmaker, exc, join
from sqlalchemy.sql import exists
from dbsetup import *
import hashlib
from os import urandom
<<<<<<< HEAD
from datetime import datetime,timedelta,date
=======
from datetime import datetime,timedelta
>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef
import random

app = Flask(__name__)

engine = create_engine('sqlite:///shg.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
dbsession = DBSession()
userID={'id':''}
<<<<<<< HEAD
minimun_requirement = 1
=======
minimun_requirement = 0
>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef

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
<<<<<<< HEAD
    print(f'the acc amt is {total_amount}',type(amount))
=======
    print(f'the acc amt is {total_amount}',type(total_amount))
>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef
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

<<<<<<< HEAD
=======
def check_user_balance(user_id,amount):
    user_amount = int(''.join([str(*i) for i in (dbsession.query(Account.balance).filter(Account.user_id == user_id)) ]))
    return(user_amount > amount)

def check_bank_balance_for(req_id):
    total_bank_amount = int(''.join([str(*i) for i in (dbsession.query(Account.balance).filter(Account.user_id == 1).all())]))
    request_amount = int(''.join([str(*i) for i in (dbsession.query(Loan_request.amount).filter(Loan_request.id==req_id)) ]))
    return(total_bank_amount > request_amount)

>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef
# sign in user
@app.route('/signin/', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        try:
            session.clear()
<<<<<<< HEAD
            uname = request.form['username'].lower()
=======
            uname = request.form['username']
>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef
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
<<<<<<< HEAD
            new_user = Users(username=uname.lower(), password=hash_object.hexdigest(), address=address, phone=int(phone),role='user',salt=salt,verified=False)
            dbsession.add(new_user)
            dbsession.commit()
            account = Account(account_no = int(random.random()*pow(10,8)),user_id=new_user.id,account_type='user',balance=3000,status='active',created_at = datetime.now())
=======
            new_user = Users(username=uname, password=hash_object.hexdigest(), address=address, phone=int(phone),role='user',salt=salt,verified=False)
            dbsession.add(new_user)
            dbsession.commit()
            account = Account(account_no = int(random.random()*pow(10,6)),user_id=new_user.id,account_type='user',balance=3000,status='active',created_at = datetime.now())
>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef
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
<<<<<<< HEAD
=======

>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef

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
<<<<<<< HEAD
=======

>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef
            return render_template('index.html', account=account, users=users)
    return redirect(url_for('about'))


@app.route('/approve/', methods=['GET', 'POST'])
def approve():
    if 'user' in session: # check for user session
        if request.method == 'POST':
<<<<<<< HEAD
            verifed_id = request.form['user_id']
            try:
=======
            try:
                verifed_id = request.form['user_id']
>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef
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
        users = dbsession.query(Users).filter(Users.verified == False).all()
        return render_template('approve.html',approves=users)
    return redirect(url_for('about'))
<<<<<<< HEAD


@app.route('/requests/', methods=['GET', 'POST'])
def requests():
    if 'user' in session:
        if request.method == 'POST':
            try:
                purpose = request.form['purpose']
                amount = request.form['amount']
                new_req = Loan_request(purpose = purpose ,status='pending', user_id = session['id'], amount = amount)
                dbsession.add(new_req)
                dbsession.commit()
                account=dbsession.query(Account).filter(Account.user_id == session['id'])
                users=dbsession.query(Users).filter(Users.id == session['id'])
                nomines = dbsession.query(Loan).join(Loan_request).filter(Loan_request.user_id == session['id']).all()
                loan_req = dbsession.query(Loan_request).filter(Loan_request.user_id == session['id']).all()
                all_users = dbsession.query(Users.id,Users.username).filter(Users.id != session['id'])
                return render_template('index.html', account=account, users=users, nomines=nomines, loans=loan_req, all_users = all_users)
            except:
                dbsession.rollback()
                print("An exception occurred")
            return redirect(url_for('requests'))
        return render_template('loanRequest.html')
    return redirect(url_for('about'))

def check_user_balance(user_id,amount):
    user_amount = int(''.join([str(*i) for i in (dbsession.query(Account.balance).filter(Account.user_id == user_id)) ]))
    return(user_amount > amount)

def check_bank_balance_for(req_id):
    total_bank_amount = int(''.join([str(*i) for i in (dbsession.query(Account.balance).filter(Account.user_id == 1).all())]))
    request_amount = int(''.join([str(*i) for i in (dbsession.query(Loan_request.amount).filter(Loan_request.id==req_id)) ]))
    return(total_bank_amount > request_amount)

@app.route('/view/', methods=['GET', 'POST'])
def view():
    if 'user' in session:
        if request.method == 'POST':
            request_id = request.form['req_id']
            try:
                if check_bank_balance_for(request_id) and not len(dbsession.query(Loan.id).filter(Loan.request_id == request_id,Loan.nominee_id == session['id']).all()) > 0 :
                    new_loan = Loan(request_id=int(request_id), nominee_id = int(session['id']) ,created_on=datetime.now())
                    dbsession.add(new_loan)
                    dbsession.commit()
                    approved = dbsession.query(Loan_request.id).join(Loan).filter(Loan_request.status=='pending').group_by(Loan.request_id).having(func.count(Loan.request_id) > minimun_requirement).all()
                    print(approved)
                    if len(approved) > 0 :
                        for item in approved:
                            req = int(*item)
                            granted_to_user = int(''.join([str(*i) for i in dbsession.query(Loan_request.user_id).filter(Loan_request.id == req)]))
                            amount = int(''.join([str(*i) for i in dbsession.query(Loan_request.amount).filter(Loan_request.id == req)]))
                            if transaction(1 , granted_to_user,amount):
                                dbsession.query(Loan_request).filter(Loan_request.id == req).update({Loan_request.status : 'granted' ,Loan_request.sanctioned_on : datetime.now()},synchronize_session=False)
                                dbsession.commit()
                # return redirect(url_for('main'))
            except:
                dbsession.rollback()
                print("An exception occurred")
            return redirect(url_for('view'))
        users = dbsession.query(Users)
        requests = dbsession.query(Loan_request).filter(Loan_request.status == 'pending',Loan_request.user_id != session['id']).all()
        return render_template('view.html', requests = requests, users = users)
    return redirect(url_for('about'))


@app.route('/transactions/')  
def transactions():
    if 'user' in session:
        acc = ''.join([str(*i) for i in (dbsession.query(Account.account_no).filter(Account.user_id == session['id']).all())])
        transaction = dbsession.query(Fin_trans).filter(or_(Fin_trans.transaction_from==acc , Fin_trans.transaction_to==acc )).order_by(Fin_trans.created_on)
        return render_template( 'transaction.html', transaction = transaction, now=datetime.now() )
    return redirect(url_for('about'))

@app.route('/reminder/')  
def reminder():
    if 'user' in session:
        users=dbsession.query(Users)
        nominee_pinalty_loan = dbsession.query(Loan_request).join(Loan).filter(Loan_request.status == 'granted',Loan.nominee_id == session['id'] ).order_by(Loan_request.sanctioned_on).all()
        print(nominee_pinalty_loan)
        return render_template( 'reminder.html', users=users, nominees=nominee_pinalty_loan )
    return redirect(url_for('about'))

@app.route('/chat/', methods=['GET', 'POST'])  
def chat():
    if 'user' in session:
        if request.method == 'POST':
            message = request.form['message']
            if len(message.strip()) > 0 :
                try:
                    new_chat = Chat(user_id = session['id'], message=message , date=datetime.now())
                    dbsession.add(new_chat)
                    dbsession.commit()
                except:
                    dbsession.rollback()
                    print("An exception occurred in chat")
            return redirect(url_for('chat'))

        users = dbsession.query(Users)
        chats = dbsession.query(Chat).order_by(Chat.date.desc())
        return render_template( 'chat.html', chats=chats, users=users )
    return redirect(url_for('about'))

@app.route('/loan/', methods=['GET', 'POST'])  
def loan():
    if 'user' in session:
        if session['role'] == 'admin':
            users=dbsession.query(Users).all()
            loan_req=dbsession.query(Loan_request).order_by(Loan_request.status).all()
            return render_template( 'adminLoan.html', loans = loan_req ,users=users)
        else:
            loan_req = dbsession.query(Loan_request).filter(Loan_request.user_id == session['id']).all()
            all_users = dbsession.query(Users.id,Users.username).filter(Users.id != session['id'])
            nomines = dbsession.query(Loan).join(Loan_request).filter(Loan_request.user_id == session['id']).all()
            
            if request.method == 'POST':
                try:
                    request_id = request.form['request_id']
                    request_amount = int(''.join([str(*i) for i in (dbsession.query(Loan_request.amount).filter(Loan_request.id==request_id)) ]))
                    user_id = int(''.join([str(*i) for i in (dbsession.query(Loan_request.user_id).filter(Loan_request.id==request_id)) ]))
                    if check_user_balance(user_id,request_amount) and (''.join([str(*i) for i in (dbsession.query(Loan_request.status).filter(Loan_request.id==request_id)) ]))=='granted':
                        if transaction(user_id,1,request_amount):
                            dbsession.query(Loan_request).filter(Loan_request.id == request_id).update({Loan_request.status : 'repaid'},synchronize_session=False)
                            dbsession.commit()
                except:
                    dbsession.rollback()
                    print("An exception occurred")
                return redirect(url_for('loan'))
            return render_template( 'userLoan.html', loans = loan_req ,all_users = all_users, nomines = nomines )
    return redirect(url_for('about'))
=======
>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef


# delete session
@app.route('/signout/')
def signout():
    session.clear()
    return redirect(url_for('main'))


<<<<<<< HEAD
=======


>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef
if __name__ == '__main__':
    app.secret_key = "\xc2\x0f\xdc\x9d0\x10A\xfa:DO\xcf\xa8%\xf0\x8e\xc1\xcb=\xf8$\xaa\xc8\xfb"
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000,threaded=False)