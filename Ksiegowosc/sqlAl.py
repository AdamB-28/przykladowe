from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ksiegowosc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_action = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())

class AccountBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)

    @classmethod
    def get_balance(cls):
        balance = cls.query.first()
        return balance.balance

    @classmethod
    def update_balance(cls, change):
        balance = cls.query.first()
        balance.balance = change
        db.session.commit()

initial_inventory_items = {
    "rower": [1000, 2],
    "odblask": [20, 10],
    "koło": [130, 4],
    "kask": [210, 5]
}

@event.listens_for(AccountBalance.__table__, 'after_create')
def insert_initial_data(*args, **kwargs):
    #Balans
    db.session.add(AccountBalance(balance=10000))    
    #magazyn
    for name, (price, quantity) in initial_inventory_items.items():
        db.session.add(InventoryItem(name=name, price=price, quantity=quantity))
    
    db.session.commit()

with app.app_context():
    db.create_all()
