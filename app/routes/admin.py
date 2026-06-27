from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models.models import db, Villa, Country, Booking, User, Service


from app.routes.main import TRANSLATIONS, TDict
from flask import session as _session

@admin_bp.context_processor
def inject_lang():
    lang = _session.get("lang", "en")
    return dict(lang=lang, t=TDict(TRANSLATIONS.get(lang, TRANSLATIONS["en"])))

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    stats = {
        'villas': Villa.query.count(),
        'bookings': Booking.query.count(),
        'users': User.query.count(),
        'new': Booking.query.filter_by(status='new').count()
    }
    bookings = Booking.query.order_by(Booking.created_at.desc()).limit(10).all()
    return render_template('admin/dashboard.html', stats=stats, bookings=bookings)

@admin_bp.route('/villas')
@login_required
@admin_required
def villas():
    villas = Villa.query.order_by(Villa.created_at.desc()).all()
    return render_template('admin/villas/list.html', villas=villas)

@admin_bp.route('/bookings')
@login_required
@admin_required
def bookings():
    bookings = Booking.query.order_by(Booking.created_at.desc()).paginate(
        page=request.args.get('page', 1, type=int), per_page=20)
    return render_template('admin/bookings/list.html', bookings=bookings)

@admin_bp.route('/bookings/<int:id>/status', methods=['POST'])
@login_required
@admin_required
def booking_status(id):
    booking = Booking.query.get_or_404(id)
    booking.status = request.form.get('status')
    db.session.commit()
    flash('Статус обновлён', 'success')
    return redirect(url_for('admin.bookings'))
