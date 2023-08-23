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

password = "admin123"
salt = urandom(8)
hash_object = hashlib.sha256(password.encode() + salt)
try:
    admin = Users(username="admin", password=hash_object.hexdigest(), address='Hubli',phone = 1234567890 ,role='admin', salt=salt,verified=True)
    session.add(admin)
    session.commit()
    # userid=session.query(Users.id).filter(Users.username == 'admin',Users.phone == 1234567890,Users.password==hash_object.hexdigest()).all()
    # print(userid)
    account = Account(account_no=int(random.random()*pow(10,6)),user_id=admin.id,account_type='SHG',balance=10000,status='active',created_at = datetime.now())
    session.add(account)
    session.commit()
except:
    session.rollback()
    print("An exception occurred")