from flask import Blueprint, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user, logout_user
from .models import db, User, Vehicle, Transaction, Wallet
from .forms import AddVehicleForm, ConfirmPurchaseForm
from . import logger, blockchain
from datetime import datetime

# Sets blueprint
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route('/', methods=['GET'])
def main():
    """
    Redirects to dashboard if logged in, if not then to login page
    """
    if not current_user.is_anonymous:
        return redirect(
            url_for('main_bp.dashboard', type='v' if current_user.is_vendor else 'u'),
            code=302
        )
    else:
        return redirect(url_for('auth_bp.login'), code=302)


@main_bp.route('/logout/', methods=['GET'])
@login_required
def logout():
    """ Logs out current user """
    logout_user()
    return redirect(url_for('auth_bp.login'), code=302)


@main_bp.route('/<type>/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard(type):
    """
    Handles the vehicle interactions based on user type

    GET - Serves page and vehicle data
        vendor: shows all add vehicles
        user: shows all available vehicles for purchase
    POST - Validates, and commits actions on vehicles
        vendor: adds vehicle
        user: purchases vehicle and adds to blockchain
    """
    # Basic authentication, if the declared usertype does not match database usertype throw forbidden
    is_vendor = True if type == 'v' else False
    if not(current_user.is_vendor == is_vendor):
        return 'Forbidden', 403

    # AddVehicleForm for vendor, ConfirmPurchaseForm for user
    form = AddVehicleForm() if is_vendor else ConfirmPurchaseForm()
    if form.validate_on_submit():
        if isinstance(form, AddVehicleForm):
            # Create and add new vehicle record
            v = Vehicle(
                uid=current_user.id,
                vin=form.vin.data,
                make=form.make.data,
                model=form.model.data,
                year=form.year.data,
                condition=form.condition.data,
                mileage=form.mileage.data,
                cost=form.cost.data
            )
            db.session.add(v)

        elif isinstance(form, ConfirmPurchaseForm):
            # If tampering with vehicle id, throw forbidden error
            v = Vehicle.query.filter_by(id=int(form.vid.data)).first()
            if not v:
                return 'Forbidden', 403

            # Add transaction and get previous block
            blockchain.add_transaction(
                sender=v.uid,
                recipient=current_user.id,
                vin=v.vin,
                make=v.make,
                model=v.model,
                year=v.year,
                condition=v.condition,
                mileage=v.mileage,
                cost=v.cost
            )
            # Get necessary data
            prev_hash = blockchain.hash_block(blockchain.last_block)
            index = len(blockchain.chain)
            nonce = blockchain.pow(index, prev_hash, blockchain.transactions)
            blockchain.append_block(prev_hash, nonce)

            # Create and add a transaction record
            t = Transaction(
                id=blockchain.hash_block(blockchain.last_block),
                vid=v.id,
                uid=current_user.id,
                timestamp=datetime.utcnow(),
                cost=v.cost
            )
            db.session.add(t)
            v.uid = current_user.id

        # Commit changes
        db.session.commit()
        redirect(url_for('main_bp.dashboard', type=type), code=302)

    # Default variable set
    wallet = None
    if is_vendor:
        # Vendor vehicles
        v_data = Vehicle.query.filter_by(uid=current_user.id).all()
    else:
        # Available vehicles
        vehicles_bought = set([t.vid for t in Transaction.query.all()])
        v_data = [v for v in Vehicle.query.all() if v.id not in vehicles_bought]
        wallet = Wallet.query.filter_by(uid=current_user.id).first()

    return render_template(
        'dashboard.html',
        is_vendor=is_vendor,
        v_data=v_data,
        wallet=wallet,
        form=form
    )


@main_bp.route('/chain/view', methods=['GET'])
def chain():
    """
    Shows the current chain, for demo purposes only
    GET - Shows blockchain
    """
    chain_list = blockchain.chain.copy()[:0:-1]  # Gets rid of genesis block

    return render_template(
        'chain.html',
        chain_list=chain_list,
        type='v' if current_user.is_vendor else 'u'
    )


@main_bp.route('/transactions/', methods=['GET'])
def transactions():
    """
    Shows all transactions taken place on current account. Has
    a page for both user types, but only users will see them,
    and will be indicated green if they are the current owner of
    that vehicle.
    """
    t = Transaction.query.filter_by(uid=current_user.id).all()
    owns = [tv.vid for tv in t if current_user.id == Vehicle.query.filter_by(id=tv.vid).first().uid]
    return render_template(
        'transactions.html',
        type='v' if current_user.is_vendor else 'u',
        data=t,
        current_owner=owns
    )

