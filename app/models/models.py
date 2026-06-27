from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='client')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='user', lazy='dynamic')
    agency = db.relationship('Agency', backref='owner', uselist=False)

    def set_password(self, p):
        self.password_hash = generate_password_hash(p)

    def check_password(self, p):
        return check_password_hash(self.password_hash, p)

    @property
    def full_name(self):
        return ((self.first_name or '') + ' ' + (self.last_name or '')).strip() or self.email


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(100), nullable=False)
    name_ru = db.Column(db.String(100))
    code = db.Column(db.String(5))
    image = db.Column(db.String(255))
    is_popular = db.Column(db.Boolean, default=False)
    villas = db.relationship('Villa', backref='country', lazy='dynamic')


class Villa(db.Model):
    __tablename__ = 'villas'
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_ru = db.Column(db.String(200))
    slug = db.Column(db.String(200), unique=True)
    description_en = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    city = db.Column(db.String(100))
    address = db.Column(db.String(300))
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    guests = db.Column(db.Integer)
    area = db.Column(db.Float)
    price_per_night = db.Column(db.Numeric(12, 2))
    price_per_week = db.Column(db.Numeric(12, 2))
    price_per_month = db.Column(db.Numeric(12, 2))
    price_b2b = db.Column(db.Numeric(12, 2))
    cover_image = db.Column(db.String(255))
    has_pool = db.Column(db.Boolean, default=False)
    has_beach = db.Column(db.Boolean, default=False)
    has_wifi = db.Column(db.Boolean, default=False)
    has_ac = db.Column(db.Boolean, default=False)
    has_parking = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Float, default=0.0)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.relationship('VillaImage', backref='villa', lazy='dynamic', cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='villa', lazy='dynamic')
    reviews = db.relationship('Review', backref='villa', lazy='dynamic')


class VillaImage(db.Model):
    __tablename__ = 'villa_images'
    id = db.Column(db.Integer, primary_key=True)
    villa_id = db.Column(db.Integer, db.ForeignKey('villas.id'), nullable=False)
    image_path = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.String(200), nullable=False)
    title_ru = db.Column(db.String(200))
    slug = db.Column(db.String(200), unique=True)
    description_en = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    category = db.Column(db.String(50))
    icon = db.Column(db.String(50))
    image = db.Column(db.String(255))
    price_from = db.Column(db.Numeric(12, 2))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Agency(db.Model):
    __tablename__ = 'agencies'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    name = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    balance = db.Column(db.Numeric(12, 2), default=0)
    credit_limit = db.Column(db.Numeric(12, 2), default=0)
    discount_percent = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='agency', lazy='dynamic')


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    booking_number = db.Column(db.String(20), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    villa_id = db.Column(db.Integer, db.ForeignKey('villas.id'), nullable=False)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'))
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60))
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    guests = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text)
    total_price = db.Column(db.Numeric(12, 2))
    payment_method = db.Column(db.String(20))
    payment_status = db.Column(db.String(20), default='pending')
    status = db.Column(db.String(20), default='new')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    villa_id = db.Column(db.Integer, db.ForeignKey('villas.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    rating = db.Column(db.Integer)
    text = db.Column(db.Text)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
