from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    bids = relationship("Bid", backref="bid",)
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    item = relationship("Item", backref="owner")
    bids = relationship("Bid", backref="bidder")


class Bid(Base):
    __tablename__ = "bid"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    user_id = Column(Integer, ForeignKey('user.id'))
    item_id = Column(Integer, ForeignKey('items.id'))

Base.metadata.create_all(engine)
Jamie = User(username="jgill", password="testing123")
Tim = User(username='tmartin', password="testing1234")
Dan = User(username='dwright', password="testing1235")
Sammy = User(username='sday', password="testing456")
session.add_all([Jamie, Tim, Dan])
session.commit()

clock_radio = Item(name="clock radio",description="alarm buzzing", owner=Jamie)
#table = Item(name="table", description="four legs")
session.add(clock_radio)
session.commit()

tim_bid = Bid(price="30.50", bidder=Tim, bid=clock_radio)
dan_bid = Bid(price="14.67", bidder=Dan, bid=clock_radio)
sammy_bid = Bid(price="19.67", bidder=Sammy, bid=clock_radio)
session.add_all([tim_bid, dan_bid, sammy_bid])
session.commit()

row = session.query(User.username, Item.name).join(Bid, Item).filter(Item.name == "clock radio").order_by(Bid.price).all()
bid_winner = row[-1][-2]
won_prize = row[-1][-1]
print("{} is the bid winner and won a {}".format(bid_winner,won_prize))




