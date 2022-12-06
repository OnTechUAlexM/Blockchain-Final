from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """ User account model """

    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    email = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.String(64),
        primary_key=False,
        unique=False,
        nullable=False
    )
    is_vendor = db.Column(
        db.Boolean,
        default=False,
        unique=False
    )

    def set_password(self, password):
        """ Create hashed password """
        self.password = generate_password_hash(
            password,
            method='sha256',
            salt_length=32
        )

    def check_password(self, password):
        """ Check hashed password """
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User %s>" % (self.username,)


class Wallet(db.Model):
    """ User wallet model"""
    __tablename__ = 'wallets'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    uid = db.Column(
        db.Integer,
        db.ForeignKey(
            'users.id'
        ),
        unique=True
    )
    wallet = db.relationship(
        'User',
        backref=db.backref(
            'wallet',
            lazy=True
        )
    )
    amt = db.Column(
        db.Float,
        default=0.0,
        unique=False
    )

    def get_formatted_amt(self):
        return "${:0,.2f}".format(self.amt)


class Vehicle(db.Model):
    """ Vehicle data model """
    __tablename__ = 'vehicles'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    uid = db.Column(
        db.Integer,
        db.ForeignKey(
            'users.id'
        )
    )
    vin = db.Column(
        db.String(),
        nullable=False
    )
    make = db.Column(
        db.String(),
        nullable=False
    )
    model = db.Column(
        db.String(),
        nullable=False
    )
    year = db.Column(
        db.String(4),
        nullable=False
    )
    condition = db.Column(
        db.String(),
        nullable=False
    )
    mileage = db.Column(
        db.Float,
        nullable=False
    )
    cost = db.Column(
        db.Float,
        default=0.0,
        nullable=False
    )

    vehicle = db.relationship(
        'User',
        backref=db.backref(
            'vehicles',
            lazy=True
        )
    )


    def get_formatted_mileage(self):
        return "{:0,.2f}".format(self.mileage)

    def get_formatted_cost(self):
        return "${:0,.2f}".format(self.cost)


class Transaction(db.Model):
    """ Transaction data model """
    __tablename__ = 'transactions'
    id = db.Column(
        db.String(128),
        primary_key=True
    )
    vid = db.Column(
        db.Integer,
        db.ForeignKey(
            'vehicles.id'
        )
    )
    uid = db.Column(
        db.Integer,
        db.ForeignKey(
            'users.id'
        )
    )
    timestamp = db.Column(
        db.DateTime,
        nullable=False
    )
    cost = db.Column(
        db.Integer,
        nullable=False
    )

    transaction_vehicle = db.relationship(
        'Vehicle',
        backref=db.backref(
            'transactions',
            lazy=True
        )
    )
    transaction_user = db.relationship(
        'User',
        backref=db.backref(
            'transactions',
            lazy=True
        )
    )

    def get_formatted_cost(self):
        return "${:0,.2f}".format(self.cost)
