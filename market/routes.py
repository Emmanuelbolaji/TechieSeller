from market import app
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user
from paystackapi.transaction import Transaction
from paystackapi.paystack import Paystack
import os


# Initialize Paystack
paystack_secret_key = os.environ.get('PAYSTACK_SECRET_KEY', 'sk_test_0c662741e291677d7fc0d2d0a3ca797295bf07ad')
paystack_public_key = os.environ.get('PAYSTACK_PUBLIC_KEY', 'pk_test_dc9b923da300329f265acef77ffe8adcebbb76d0')
paystack = Paystack(secret_key=paystack_secret_key)


@app.route('/')
@app.route('/home')
def home_page():
    """
    Route to display the home page.

    Returns:
        Route to display the home page.
    """
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
def market_page():
    """
    Route to display the market page where items are listed.
    Authenticated users can see items they own.

    Returns:
        Rendered market.html template with available and owned items.
    """
    items = Item.query.filter_by(owner=None)
    owned_items = []
    if current_user.is_authenticated:
        owned_items = Item.query.filter_by(owner=current_user.id)
    return render_template('market.html', items=items, owned_items=owned_items)


@app.route('/payment/<int:item_id>', methods=['GET'])
@login_required
def payment(item_id):
    """
    Route to display the payment page for a specific item.

    Args:
        item_id (int): The ID of the item being purchased.

    Returns:
        Rendered payment.html template with the item details and Paystack public key.
    """
    item = Item.query.get_or_404(item_id)
    return render_template('payment.html', item=item, paystack_public_key=paystack_public_key)


@app.route('/payment-callback/<int:item_id>')
@login_required
def payment_callback(item_id):
    """
    Route to handle the payment callback from Paystack.
    Verifies the payment status and assigns ownership of the item to the user if successful.

    Args:
        item_id (int): The ID of the item being purchased.

    Returns:
        Redirects to the market page after processing the payment.
    """
    reference = request.args.get('reference')
    if reference:
        try:
            response = Transaction.verify(reference=reference)
            if response['status'] and response['data']['status'] == 'success':
                item = Item.query.get_or_404(item_id)
                item.owner = current_user.id
                db.session.commit()
                flash(f"Congratulations! You purchased {item.name}", category='success')
            else:
                flash("Payment was not successful. Please try again.", category='danger')
        except Exception as e:
            flash(f"An error occurred: {str(e)}", category='danger')
    else:
        flash("No reference provided. Unable to verify payment.", category='danger')
    return redirect(url_for('market_page'))


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    """
    Route to handle user registration.
    Creates a new user and logs them in if the form is valid.

    Returns:
        Rendered register.html template with the registration form.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                email_address=form.email_address.data,
                password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """
    Route to handle user login.
    Authenticates the user and redirects to the market page upon successful login.

    Returns:
        Rendered login.html template with the login form.
    """
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
                );
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match! Please try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    """
    Route to log the user out and redirect to the home page.

    Returns:
        Redirects to the home page after logout.
    """
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/initialize-payment/<int:item_id>', methods=['POST'])
@login_required
def initialize_payment(item_id):
    """
    Route to initialize a payment with Paystack.
    Returns an authorization URL for the user to complete the payment.

    Args:
        item_id (int): The ID of the item being purchased.

    Returns:
        JSON response with the authorization URL if successful, or an error message.
    """
    item = Item.query.get_or_404(item_id)
    try:
        response = paystack.transaction.initialize(
                reference=f'purchase_{item.id}_{current_user.id}',
                amount=item.price * 100,  # Paystack uses kobo (100 kobo = 1 Naira)
                email=current_user.email_address,
                callback_url=url_for('payment_callback', item_id=item.id, _external=True)
                )

        if response['status']:
            return jsonify({
                'status': 'success',
                'authorization_url': response['data']['authorization_url']
                })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Unable to initialize payment'
                }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
            }), 500
