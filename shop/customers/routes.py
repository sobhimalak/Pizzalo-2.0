from flask import render_template,session,request,redirect,url_for,flash,current_app,send_from_directory, current_app
from flask_login import login_required, current_user, logout_user, login_user
from shop import app,db, photos, search, bcrypt, login_manager
from .forms import CustomerRegisterForm, CustomerLoginForm
from .models import Register, CustomerOrder
import secrets
import os



@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, username=form.username.data, email=form.email.data, password=hash_password, country=form.country.data,city=form.city.data, address=form.address.data, postal_code=form.postal_code.data)
        db.session.add(register)
        flash(f'Welcome {form.name.data} Thank you for registering', 'success')
        db.session.commit()
        return redirect(url_for('customer/login.html'))
    return render_template('customer/register.html', form=form)

@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'You are now logged in','success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash(f'Incorrect email or password','danger')
        return redirect(url_for('customerLogin'))
    return render_template('customer/login.html', form = form)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/getoder')
@login_required
def get_order():
    if current_user.is_authenticated():
        customer_id = current_user.id
        invoice = secrets.token.hex(5)
        try:
            order = CustomerOrder(invoice, customer_id, orders=session['Shoppingcart'])
            db.session.add()()
        except Exception as e:
            print(e)
            flash(f'Something went Wrong while get order','danger')
            return redirect(url_for('getCart'))