from flask import Blueprint, render_template, request, abort
from app.models.models import Villa, Country, Review, db

villas_bp = Blueprint('villas', __name__)

@villas_bp.route('/')
def index():
    q         = request.args.get('q', '')
    country   = request.args.get('country', type=int)
    guests    = request.args.get('guests', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    has_pool  = request.args.get('has_pool')
    has_beach = request.args.get('has_beach')
    has_wifi  = request.args.get('has_wifi')
    sort      = request.args.get('sort', 'created_at')
    page      = request.args.get('page', 1, type=int)

    query = Villa.query.filter_by(is_active=True)
    if q:         query = query.filter(Villa.title_en.ilike(f'%{q}%'))
    if country:   query = query.filter(Villa.country_id == country)
    if guests:    query = query.filter(Villa.guests >= guests)
    if min_price: query = query.filter(Villa.price_per_night >= min_price)
    if max_price: query = query.filter(Villa.price_per_night <= max_price)
    if has_pool:  query = query.filter(Villa.has_pool == True)
    if has_beach: query = query.filter(Villa.has_beach == True)
    if has_wifi:  query = query.filter(Villa.has_wifi == True)
    if sort == 'price_asc':  query = query.order_by(Villa.price_per_night.asc())
    elif sort == 'price_desc': query = query.order_by(Villa.price_per_night.desc())
    elif sort == 'rating':   query = query.order_by(Villa.rating.desc())
    else:                    query = query.order_by(Villa.created_at.desc())

    villas    = query.paginate(page=page, per_page=12, error_out=False)
    countries = Country.query.all()
    return render_template('villas/list.html', villas=villas, countries=countries, q=q)

@villas_bp.route('/<slug>')
def detail(slug):
    villa = Villa.query.filter_by(slug=slug, is_active=True).first_or_404()
    # increment views
    try:
        villa.views = (villa.views or 0) + 1
        db.session.commit()
    except:
        db.session.rollback()
    reviews = Review.query.filter_by(villa_id=villa.id, is_approved=True).order_by(Review.created_at.desc()).limit(10).all()
    similar = Villa.query.filter(Villa.country_id==villa.country_id, Villa.id!=villa.id, Villa.is_active==True).limit(3).all()
    return render_template('villas/detail.html', villa=villa, reviews=reviews, similar=similar)
