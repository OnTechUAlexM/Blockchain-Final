from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap4
from config import Logging
import logging
from blockchain import Blockchain


logging.basicConfig(
    format=Logging.FORMAT,
    datefmt=Logging.DATE_FORMAT
)

# Logging
logger = logging.getLogger()
logger.setLevel(Logging.LEVEL)

# Flask plugins
db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap4()
logger.info("Finding genesis block with difficulty %s..." % (len(Blockchain._difficulty_level)))
blockchain = Blockchain()
logger.info("Done.")


def create_app():
    from .models import User, Vehicle, Transaction, Wallet
    """ Init application """

    logger.info("Initiating Flask app...")
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    logger.info("Done.")

    logger.info("Initializing plugins...")
    logger.info("Database...")
    db.init_app(app)
    logger.info("Login manager...")
    login_manager.init_app(app)
    logger.info("Bootstrap")
    bootstrap.init_app(app)
    logger.info("Done.")

    with app.app_context():
        # Routes
        from . import routes, auth

        # Blueprints
        app.register_blueprint(routes.main_bp)
        app.register_blueprint(auth.auth_bp)

        db.drop_all()

        db.create_all()

        u = User(
            email='user@gmail.com'
        )
        u.set_password('123')
        db.session.add(u)

        uv = User(
            email='vendor@gmail.com',
            is_vendor=True
        )
        uv.set_password('123')
        db.session.add(uv)
        db.session.commit()

        uvid = User.query.filter_by(email='vendor@gmail.com').first()

        v = Vehicle(
            uid=uvid.id,
            vin='1234567543',
            make='Ford',
            model='Fiesta',
            condition='In Repair',
            mileage=150_000.0,
            cost=5000
        )
        v1 = Vehicle(
            uid=uvid.id,
            vin='7654324565',
            make='Ford',
            model='Focus',
            condition='New',
            mileage=150.0,
            cost=12000
        )
        v2 = Vehicle(
            uid=uvid.id,
            vin='345673272312',
            make='Chevy',
            model='Cruise',
            condition='New',
            mileage=17.0,
            cost=8000
        )
        db.session.add_all([v, v1, v2])
        db.session.commit()

        uid = User.query.filter_by(email='user@gmail.com').first()

        w = Wallet(
            uid=uid.id,
            amt=100_000.00
        )
        db.session.add(w)
        db.session.commit()

        return app
