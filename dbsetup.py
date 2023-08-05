from sqlalchemy import Column, ForeignKey, Integer, String, Text, LargeBinary,Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import CheckConstraint
from sqlalchemy import UniqueConstraint

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, autoincrement=True)
    username = Column(Text)
    password = Column(Text)
    address = Column(Text)
    phone = Column(Integer , unique=True)
    role = Column(String)
    salt = Column(LargeBinary)
    verified = Column(Boolean)
 
    @property
    def serialise(self):
        return {
            'id': self.id,
            'username':self.username,
            'password':self.password,
            'address':self.address,
            'phone':self.phone,
            'role':self.role,
            'salt':self.salt,
            'verified':self.verified
            }

class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key = True, autoincrement=True)
    account_no = Column(Integer,unique=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    # username = Column(String, ForeignKey('users.username'))
    users = relationship(Users)
    account_type = Column(String)
    balance = Column(Integer)
    status = Column(Text, default = Text("active"))
    created_at=Column(Date)
    UniqueConstraint("account_no","user_id")


    @property
    def serialise(self):
        return {
            'id' :self.id,
            'account_no' : self.account_no,
            'user_id' : self.user_id,
            'account_type' : self.account_type,
            'balance' : self.balance,
            'status' : self.status,
            'created_at': self.created_at,
            }

class Loan_request(Base):
    __tablename__ = 'loan_request'
    id = Column(Integer, primary_key=True, autoincrement=True)
    purpose = Column(Text)
    user_id = Column(Integer , ForeignKey('users.id'))
    users = relationship(Users)
    amount = Column(Integer)

    @property
    def serialise(self):
        return {
            'id' : self.id,
            'purpose' : self.purpose,
            'user_id' : self.user_id,
            'amount' : self.amount
            }

class Loan(Base):
    __tablename__ = 'loan'
    id=Column(Integer, primary_key=True, autoincrement=True)
    request_id=Column(Integer,ForeignKey('loan_request.id'))
    # request_amount=Column(Integer,ForeignKey('loan_request.amount'))
    status=Column(String)
    created_on=Column(Date)
    nominee_1=Column(Integer, ForeignKey('users.id'))
    nominee_2=Column(Integer, ForeignKey('users.id'))
    
    request = relationship("Loan_request", foreign_keys=[request_id],backref="req")
    nom1 = relationship("Users",foreign_keys=[nominee_1],backref="n1")
    nom2 = relationship("Users",foreign_keys=[nominee_2],backref="n2")


    @property
    def serialise(self):
        return{
            'id':self.id,
            'request_id':self.request_id,
            # 'request_amount':self.request_amount,
            'status':self.status,
            'created_on':self.created_on,
            'nominee_1':self.nominee_1,
            'nominee_2':self.nominee_2
        }

class Fin_trans(Base):
    __tablename__='fin_trans'
    id=Column(Integer, primary_key=True, autoincrement=True)
    user_acc=Column(Integer, ForeignKey('account.id'))
    created_on=Column(Date)
    transaction_amount=Column(Integer)
    transaction_from=Column(Integer,ForeignKey('account.id'))
    transaction_to=Column(Integer,ForeignKey('account.id'))

    user = relationship("Account",foreign_keys=[user_acc],backref="fin_user_id")
    trans_from = relationship("Account",foreign_keys=[transaction_from],backref="from")
    trans_to = relationship("Account",foreign_keys=[transaction_to],backref="to")

    @property
    def serialise(self):
        return{
            'transaction_id':self.id,
            'user_id':self.user_acc,
            'created_on':self.created_on,
            'transaction_amount':self.transaction_amount,
            'transaction_from':self.transaction_from,
            'transaction_to':self.transaction_to
        }
    
class Pinalty(Base):
    __tablename__='pinalty'
    id=Column(Integer,primary_key=True, autoincrement=True)
    loan_id=Column(Integer,ForeignKey('loan.id'))
    status=Column(String)
    transaction_id=Column(Integer,ForeignKey('fin_trans.id'))
    loan = relationship(Loan)
    fin_trans = relationship(Fin_trans)


    @property
    def serialise(self):
        return{
            'id':self.id,
            'loan_id':self.loan_id,
            'status':self.status,
            'transaction_id':self.transaction_id
        }
        
    
class Approver(Base):
    __tablename__='approver'
    id=Column(Integer,primary_key=True, autoincrement=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    approver_id=Column(Integer,ForeignKey('users.id'))
    approved_on=Column(Date)
    UniqueConstraint("user_id", "approver_id")

    approve_user = relationship("Users",foreign_keys=[user_id],backref="approv_user_id")
    approve_id = relationship("Users",foreign_keys=[approver_id],backref="approv_id")
 
    @property
    def serialise(self):
        return{
            'id':self.id,
            'user_id':self.user_id,
            'approver_id':self.approver_id,
            'approved_on':self.approved_on,
        }

engine = create_engine('sqlite:///shg.db')
Base.metadata.create_all(engine)