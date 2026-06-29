from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user, login_user
from app.models.models import db, Agency, Booking, User

b2b_bp = Blueprint('b2b', __name__)

@b2b_bp.route('/')
@login_required
def dashboard():
    agency = Agency.query.filter_by(owner_id=current_user.id).first()
    if not agency:
        return redirect(url_for('b2b.register'))
    bookings = agency.bookings.order_by(Booking.created_at.desc()).limit(10).all()
    return render_template('b2b/dashboard.html', agency=agency, bookings=bookings)

@b2b_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Allow both logged-in and guest users
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        phone   = request.form.get('phone', '').strip()
        country = request.form.get('country', '').strip()

        if not name or not email:
            flash('Please fill agency name and email.', 'error')
            return render_template('b2b/register.html')

        # Create user if not logged in
        if current_user.is_authenticated:
            user = current_user
        else:
            user = User.query.filter_by(email=email).first()
            if not user:
                import random, string
                pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                user = User(email=email, phone=phone)
                user.set_password(pwd)
                db.session.add(user)
                db.session.flush()

        if Agency.query.filter_by(owner_id=user.id).first():
            flash('This email is already registered as a partner.', 'error')
            return render_template('b2b/register.html')

        agency = Agency(owner_id=user.id, name=name, country=country, phone=phone, email=email)
        db.session.add(agency)
        user.role = 'agent'
        db.session.commit()

        if not current_user.is_authenticated:
            login_user(user)

        flash('B2B application submitted! We will activate your account within 24 hours.', 'success')
        return redirect(url_for('b2b.dashboard'))
    return render_template('b2b/register.html')
