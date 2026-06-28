from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.models import Villa, Country, Service

main_bp = Blueprint('main', __name__)

@main_bp.route('/lang/<lang>')
def set_lang(lang):
    if lang in ['en', 'ru', 'uz']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))

@main_bp.route('/')
def index():
    featured = Villa.query.filter_by(is_active=True, is_featured=True).limit(6).all()
    countries = Country.query.filter_by(is_popular=True).limit(8).all()
    services = Service.query.filter_by(is_active=True).limit(6).all()
    return render_template('main/index.html', featured=featured, countries=countries, services=services)

@main_bp.route('/search')
def search():
    q = request.args.get('q', '')
    country = request.args.get('country', type=int)
    guests = request.args.get('guests', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort = request.args.get('sort', 'created_at')
    page = request.args.get('page', 1, type=int)

    query = Villa.query.filter_by(is_active=True)
    if q: query = query.filter(Villa.title_en.ilike(f'%{q}%'))
    if country: query = query.filter(Villa.country_id == country)
    if guests: query = query.filter(Villa.guests >= guests)
    if min_price: query = query.filter(Villa.price_per_night >= min_price)
    if max_price: query = query.filter(Villa.price_per_night <= max_price)
    if sort == 'price_asc': query = query.order_by(Villa.price_per_night.asc())
    elif sort == 'price_desc': query = query.order_by(Villa.price_per_night.desc())
    else: query = query.order_by(Villa.created_at.desc())

    villas = query.paginate(page=page, per_page=12, error_out=False)
    countries = Country.query.all()
    return render_template('main/search.html', villas=villas, countries=countries, q=q)

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/contacts')
def contacts():
    return render_template('main/contacts.html')
