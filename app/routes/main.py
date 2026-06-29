from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from datetime import date
from app.models.models import Villa, Country, Service, Booking, db
from datetime import datetime
import random, string

main_bp = Blueprint('main', __name__)

def gen_booking_number():
    return 'BT-' + ''.join(random.choices(string.digits, k=6))

@main_bp.route('/lang/<lang>')
def set_lang(lang):
    if lang in ['en', 'ru', 'uz']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/')
def index():
    featured  = Villa.query.filter_by(is_active=True, is_featured=True).limit(6).all()
    countries = Country.query.filter_by(is_popular=True).limit(8).all()
    services  = Service.query.filter_by(is_active=True).limit(4).all()
    return render_template('main/index.html', featured=featured, countries=countries, services=services)

@main_bp.route('/search')
def search():
    q         = request.args.get('q', '')
    country   = request.args.get('country', type=int)
    guests    = request.args.get('guests', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort      = request.args.get('sort', 'created_at')
    page      = request.args.get('page', 1, type=int)
    query = Villa.query.filter_by(is_active=True)
    if q:         query = query.filter(Villa.title_en.ilike(f'%{q}%'))
    if country:   query = query.filter(Villa.country_id == country)
    if guests:    query = query.filter(Villa.guests >= guests)
    if min_price: query = query.filter(Villa.price_per_night >= min_price)
    if max_price: query = query.filter(Villa.price_per_night <= max_price)
    if sort == 'price_asc':  query = query.order_by(Villa.price_per_night.asc())
    elif sort == 'price_desc': query = query.order_by(Villa.price_per_night.desc())
    else: query = query.order_by(Villa.created_at.desc())
    villas    = query.paginate(page=page, per_page=12, error_out=False)
    countries = Country.query.all()
    return render_template('main/search.html', villas=villas, countries=countries, q=q)

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        if name and (email or request.form.get('phone')):
            flash('Message sent! We will reply within 2 hours.', 'success')
        else:
            flash('Please fill in your name and contact details.', 'error')
        return redirect(url_for('main.contacts'))
    return render_template('main/contacts.html')

@main_bp.route('/book', methods=['POST'])
def book():
    """Quick booking from any page"""
    try:
        villa_id   = request.form.get('villa_id', type=int)
        first_name = request.form.get('first_name', '').strip()
        phone      = request.form.get('phone', '').strip()
        email      = request.form.get('email', '').strip()
        check_in   = request.form.get('check_in')
        check_out  = request.form.get('check_out')
        guests     = request.form.get('guests', 2, type=int)
        notes      = request.form.get('notes', '')

        if not all([villa_id, first_name, phone, check_in, check_out]):
            flash('Please fill all required fields.', 'error')
            return redirect(request.referrer or url_for('main.index'))

        from flask_login import current_user
        booking = Booking(
            booking_number=gen_booking_number(),
            villa_id=villa_id,
            user_id=current_user.id if current_user.is_authenticated else None,
            first_name=first_name,
            phone=phone,
            email=email,
            check_in=datetime.strptime(check_in, '%Y-%m-%d').date(),
            check_out=datetime.strptime(check_out, '%Y-%m-%d').date(),
            guests=guests,
            notes=notes,
            status='new',
        )
        # calc price
        villa = Villa.query.get(villa_id)
        if villa and villa.price_per_night:
            nights = (booking.check_out - booking.check_in).days
            booking.total_price = float(villa.price_per_night) * max(nights, 1)
        db.session.add(booking)
        db.session.commit()
        flash(f'Booking confirmed! Your reference: {booking.booking_number}', 'success')
        return redirect(url_for('main.booking_confirm', num=booking.booking_number))
    except Exception as e:
        flash('Booking error. Please contact us via WhatsApp.', 'error')
        return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/booking/<num>')
def booking_confirm(num):
    booking = Booking.query.filter_by(booking_number=num).first_or_404()
    return render_template('main/booking_confirm.html', booking=booking)

@main_bp.app_errorhandler(404)
def e404(e):
    return render_template('errors/404.html'), 404

@main_bp.app_errorhandler(500)
def e500(e):
    return render_template('errors/500.html'), 500

@main_bp.route('/sitemap.xml')
def sitemap():
    from flask import Response
    from app.models.models import Villa, Country
    urls = [
        '<url><loc>https://bektour.uz/</loc><changefreq>daily</changefreq><priority>1.0</priority></url>',
        '<url><loc>https://bektour.uz/villas/</loc><changefreq>daily</changefreq><priority>0.9</priority></url>',
        '<url><loc>https://bektour.uz/services/</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>',
        '<url><loc>https://bektour.uz/about</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>',
        '<url><loc>https://bektour.uz/contacts</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>',
    ]
    for v in Villa.query.filter_by(is_active=True).all():
        urls.append(f'<url><loc>https://bektour.uz/villas/{v.slug}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>')
    xml = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(urls) + '</urlset>'
    return Response(xml, mimetype='application/xml')

@main_bp.route('/robots.txt')
def robots():
    from flask import Response
    txt = "User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /auth/\nSitemap: https://bektour.uz/sitemap.xml"
    return Response(txt, mimetype='text/plain')
