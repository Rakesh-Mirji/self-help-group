from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import *
import hashlib
from os import urandom
from datetime import datetime
import random 

engine = create_engine('sqlite:///shg.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def transaction(from_user,to_user,amount):
    total_amount = int(''.join([str(*i) for i in (session.query(Account.balance).filter(Account.user_id == from_user).all())]))
    print(f'the acc amt is {total_amount}',type(amount))
    if total_amount > amount:
        from_acc = ''.join([str(*i) for i in (session.query(Account.account_no).filter(Account.user_id == from_user).all())])
        to_acc = ''.join([str(*i) for i in (session.query(Account.account_no).filter(Account.user_id == to_user).all())])

        new_trans = Fin_trans(user_acc = from_user, created_on=datetime.now(), transaction_amount = amount, transaction_from=from_acc ,transaction_to=to_acc)
        session.add(new_trans)
        session.query(Account).filter(Account.user_id == from_user).update({Account.balance :Account.balance - amount },synchronize_session=False)
        session.query(Account).filter(Account.user_id == to_user).update({Account.balance :Account.balance + amount },synchronize_session=False)
        session.commit()
        return True
    return False

def newUser(name,password,phone,location):
    try:
        hash_object = hashlib.sha256(password.encode() + salt)
        user = Users(username=name, password=hash_object.hexdigest(), address=location,phone = phone ,role='user', salt=salt,verified=True)
        session.add(user)
        session.commit()
        # userid=session.query(Users.id).filter(Users.username == 'admin',Users.phone == 1234567890,Users.password==hash_object.hexdigest()).all()
        # print(user)
        account = Account(account_no=int(random.random()*pow(10,8)), user_id=user.id,account_type='user',balance=3000,status='active',created_at = datetime.now())
        session.add(account)
        session.commit()
        transaction(user.id,1,2000)
    except:
        session.rollback()
        print(f"An exception occurred with {name}'s registeration")

password = "admin123"
salt = urandom(8)
hash_object = hashlib.sha256(password.encode() + salt)
try:
    admin = Users(username="admin", password=hash_object.hexdigest(), address='Hubli',phone = 1234567890 ,role='admin', salt=salt,verified=True)
    session.add(admin)
    session.commit()
    # userid=session.query(Users.id).filter(Users.username == 'admin',Users.phone == 1234567890,Users.password==hash_object.hexdigest()).all()
    # print(userid)
<<<<<<< HEAD
    account = Account(account_no=int(random.random()*pow(10,8)),user_id=admin.id,account_type='SHG',balance=100000,status='active',created_at = datetime.now())
=======
    account = Account(account_no=int(random.random()*pow(10,6)),user_id=admin.id,account_type='SHG',balance=10000,status='active',created_at = datetime.now())
>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef
    session.add(account)
    session.commit()
except:
    session.rollback()
<<<<<<< HEAD
    print("An exception occurred")

newUser('ross','1234',9876543210,'NYC')
newUser('chandler','1234',8765432109,'Ocalhoma')
newUser('rachel','1234',7654321089,'Bosten')
newUser('monica','1234',6543207890,'NYC')
=======
    print("An exception occurred")
>>>>>>> d62e9aa72717e4f88f362f4187197bbf20914bef
