from flask import Blueprint, render_template
from app.models.models import Service

services_bp = Blueprint('services', __name__)

@services_bp.route('/')
def index():
    transfer = Service.query.filter_by(category='transfer', is_active=True).all()
    cars = Service.query.filter_by(category='car', is_active=True).all()
    yachts = Service.query.filter_by(category='yacht', is_active=True).all()
    guides = Service.query.filter_by(category='guide', is_active=True).all()
    return render_template('services/index.html', transfer=transfer, cars=cars, yachts=yachts, guides=guides)

@services_bp.route('/<slug>')
def detail(slug):
    service = Service.query.filter_by(slug=slug, is_active=True).first_or_404()
    return render_template('services/detail.html', service=service)
