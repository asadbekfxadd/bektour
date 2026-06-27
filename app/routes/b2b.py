from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import db, Agency, Booking


from app.routes.main import TRANSLATIONS, TDict
from flask import session as _session

@b2b_bp.context_processor
def inject_lang():
    lang = _session.get("lang", "en")
    return dict(lang=lang, t=TDict(TRANSLATIONS.get(lang, TRANSLATIONS["en"])))

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
@login_required
def register():
    if Agency.query.filter_by(owner_id=current_user.id).first():
        return redirect(url_for('b2b.dashboard'))
    if request.method == 'POST':
        agency = Agency(
            owner_id=current_user.id,
            name=request.form['name'],
            country=request.form.get('country'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
        )
        db.session.add(agency)
        current_user.role = 'agent'
        db.session.commit()
        flash('Заявка отправлена!', 'success')
        return redirect(url_for('b2b.dashboard'))
    return render_template('b2b/register.html')
