from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, DateTime, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:password@localhost/database')

Base = declarative_base()

class Queue(Base):
    __tablename__ = 'message_queue'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    sender = Column(Text)
    message = Column(Text)
    status = Column(Integer)
    
    def __init__(self, date, sender, message, status):
        self.date = date
        self.sender = sender
        self.message = message
        self.status = status
    
    def __repr__(self):
        return "<Entries('%s','%s', '%s', %s)>" % (self.tanggal, self.pengirim, self.pesan, self.status)

class Inbox(Base):
    __tablename__ = 'inbox'
    
    ID = Column(Integer, primary_key=True)
    UpdatedInDB = Column(TIMESTAMP)
    ReceivingDateTime = Column(TIMESTAMP)
    TextDecoded = Column(Text)
    SenderNumber = Column(Text)
    
    def __init__(self, UpdatedInDB, ReceivingDateTime, TextDecoded, SenderNumber):
        self.UpdatedInDB = UpdatedInDB
        self.ReceivingDateTime = ReceivingDateTime
        self.TextDecoded = TextDecoded
        self.SenderNumber = SenderNumber

    def __repr__(self):
        return "<Entries('%s','%s', '%s')>" % (self.ReceivingDateTime, self.TextDecoded, self.SenderNumber)

class Outbox(Base):
    __tablename__ = 'outbox'
    
    ID = Column(Integer, primary_key=True)
    DestinationNumber = Column(Text)
    TextDecoded = Column(Text)
    CreatorID = Column(Text)
    
    def __init__(self, DestinationNumber, TextDecoded, CreatorID):
        self.DestinationNumber = DestinationNumber
        self.TextDecoded = TextDecoded
        self.CreatorID = CreatorID
    
    def __repr__(self):
        return "<Entries('%s','%s', '%s')>" % (self.Destination, self.TextDecoded, self.CreatorID)

class Broadcast(Base):
    __tablename__ = 'message_broadcast'
    
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    phone = Column(Text)
    
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
    
    def __repr__(self):
        return "<Entries('%s','%s')>" % (self.name, self.phone)

class Latest(Base):
    __tablename__ = 'latest'
    
    last_sms = Column(Integer, primary_key=True)
    last_queue = Column(Integer)
    
    def __init__(self, last_sms, last_queue):
        self.last_sms = last_sms
        self.last_queue = last_queue
    
    def __repr__(self):
        return "<Entries('%s', '%s')>" % (self.last_sms, self.last_queue)

Session = sessionmaker(bind=engine)
session = Session()

def get_latest_sms():
    latest = session.query(Latest).all()
    result = latest[0].last_sms
    session.commit()
    return result

def get_latest_queue():
    latest = session.query(Latest).all()
    result = latest[0].last_queue
    session.commit()
    return result
    
def get_sms(id):
    result = session.query(Inbox).filter("id=%s" % id).all()
    session.commit()
    return result

def save_queue(date, sender, message):
    que = Queue(date=date, sender=sender, message=message, status=1)
    session.add(que)
    session.commit()
    
def update_last_queue(val):
    latest = session.query(Latest).all()
    latest[0].last_queue = val
    session.commit()

def save_outbox(destination, message, creator):
    p = Outbox(DestinationNumber=destination, TextDecoded=message, CreatorID=creator)
    session.add(p)
    session.commit()

def get_broadcast():
    broadcast = session.query(Broadcast).all()
    session.commit()
    return broadcast
    
