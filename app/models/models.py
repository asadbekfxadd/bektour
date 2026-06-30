from datetime import datetime
import json
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

    # ── Destination experience fields (additive) ──
    slug = db.Column(db.String(120), unique=True)
    video_url = db.Column(db.String(400))          # MP4 hero/card video
    video_webm_url = db.Column(db.String(400))      # optional WebM variant
    poster_image = db.Column(db.String(255))         # explicit poster, falls back to `image`
    subtitle_en = db.Column(db.String(200))
    subtitle_ru = db.Column(db.String(200))
    description_en = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    is_unesco = db.Column(db.Boolean, default=False)
    best_season_en = db.Column(db.String(120))
    best_season_ru = db.Column(db.String(120))
    avg_temp = db.Column(db.String(40))              # e.g. "18–32°C"
    population = db.Column(db.String(40))            # e.g. "550,000+"
    area_km2 = db.Column(db.String(40))
    founded_year = db.Column(db.String(40))           # e.g. "742 AD" or "VI century BC"
    travel_time_en = db.Column(db.String(80))
    travel_time_ru = db.Column(db.String(80))
    top_attractions = db.Column(db.Text)               # JSON list of {name_en,name_ru,image}
    media_clips = db.relationship('DestinationMedia', backref='country', lazy='dynamic',
                                   order_by='DestinationMedia.order', cascade='all, delete-orphan')

    @property
    def display_slug(self):
        return self.slug or (self.name_en or '').lower().replace(' valley', '').replace(' ', '-')

    @property
    def attractions_list(self):
        if not self.top_attractions:
            return []
        try:
            return json.loads(self.top_attractions)
        except Exception:
            return []


class DestinationMedia(db.Model):
    """Themed video/photo clips for a destination page gallery
    (drone, walking tour, night, food, festival, market, hotel, historical)."""
    __tablename__ = 'destination_media'
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    media_type = db.Column(db.String(30), default='drone')  # drone, walking, night, food, festival, historical, market, hotel
    title_en = db.Column(db.String(150))
    title_ru = db.Column(db.String(150))
    video_url = db.Column(db.String(400))
    poster_image = db.Column(db.String(255))
    duration_sec = db.Column(db.Integer)
    order = db.Column(db.Integer, default=0)


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


# ═══════════════════════════════════════════════════
# B2B PARTNER PLATFORM MODELS
# ═══════════════════════════════════════════════════

class Property(db.Model):
    """Partner-managed properties: hotels, resorts, villas, guesthouses etc."""
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='hotel')  # hotel, resort, villa, guesthouse, apartment, hostel, camping, glamping, sanatorium, mountain_resort, eco_resort
    description = db.Column(db.Text)
    address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    cover_image = db.Column(db.String(255))
    gallery = db.Column(db.Text)  # JSON list of image URLs
    video_url = db.Column(db.String(255))
    tour_360_url = db.Column(db.String(255))
    check_in_time = db.Column(db.String(20), default='14:00')
    check_out_time = db.Column(db.String(20), default='12:00')
    cancellation_policy = db.Column(db.Text)
    languages_spoken = db.Column(db.String(200))
    nearby_attractions = db.Column(db.Text)
    has_parking = db.Column(db.Boolean, default=False)
    has_restaurant = db.Column(db.Boolean, default=False)
    has_pool = db.Column(db.Boolean, default=False)
    has_spa = db.Column(db.Boolean, default=False)
    has_gym = db.Column(db.Boolean, default=False)
    has_wifi = db.Column(db.Boolean, default=True)
    has_airport_transfer = db.Column(db.Boolean, default=False)
    has_breakfast = db.Column(db.Boolean, default=False)
    has_lunch = db.Column(db.Boolean, default=False)
    has_dinner = db.Column(db.Boolean, default=False)
    seo_title = db.Column(db.String(200))
    seo_description = db.Column(db.String(300))
    status = db.Column(db.String(20), default='draft')  # draft, published
    rating = db.Column(db.Float, default=0.0)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    rooms = db.relationship('Room', backref='property', lazy='dynamic', cascade='all, delete-orphan')


class Room(db.Model):
    """Room categories within a property"""
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    max_guests = db.Column(db.Integer, default=2)
    bed_type = db.Column(db.String(80))
    size_sqm = db.Column(db.Float)
    base_price = db.Column(db.Numeric(12, 2))
    weekend_price = db.Column(db.Numeric(12, 2))
    high_season_price = db.Column(db.Numeric(12, 2))
    cover_image = db.Column(db.String(255))
    gallery = db.Column(db.Text)
    total_rooms = db.Column(db.Integer, default=1)
    instant_booking = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Tour(db.Model):
    """Partner-managed tour packages"""
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='private')  # private, vip, luxury, adventure, business, family, historical, food, mountain, desert, weekend, custom
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(255))
    gallery = db.Column(db.Text)
    video_url = db.Column(db.String(255))
    duration_days = db.Column(db.Integer, default=1)
    destinations = db.Column(db.String(300))  # comma-separated city list
    hotels_included = db.Column(db.Text)
    meals_included = db.Column(db.String(100))  # e.g. "Breakfast, Lunch"
    transportation = db.Column(db.String(150))
    guide_languages = db.Column(db.String(200))
    price_per_person = db.Column(db.Numeric(12, 2))
    discount_percent = db.Column(db.Float, default=0)
    min_travelers = db.Column(db.Integer, default=1)
    max_travelers = db.Column(db.Integer, default=20)
    meeting_point = db.Column(db.String(300))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    included_services = db.Column(db.Text)
    excluded_services = db.Column(db.Text)
    cancellation_rules = db.Column(db.Text)
    itinerary = db.Column(db.Text)  # JSON: [{"day":1,"title":"...","desc":"..."}]
    status = db.Column(db.String(20), default='draft')
    rating = db.Column(db.Float, default=0.0)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MediaAsset(db.Model):
    """Media center file storage references"""
    __tablename__ = 'media_assets'
    id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(400))
    file_type = db.Column(db.String(30))  # image, video, drone, 360, pdf, document, logo, certificate
    folder = db.Column(db.String(120), default='General')
    file_size_kb = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class PartnerCustomer(db.Model):
    """CRM customer profiles managed by a partner agency"""
    __tablename__ = 'partner_customers'
    id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    nationality = db.Column(db.String(80))
    passport_number = db.Column(db.String(50))
    notes = db.Column(db.Text)
    loyalty_points = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Numeric(12, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SupportTicket(db.Model):
    """Partner support tickets"""
    __tablename__ = 'support_tickets'
    id = db.Column(db.Integer, primary_key=True)
    agency_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='open')  # open, answered, closed
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Announcement(db.Model):
    """Platform-wide announcements shown to all partners"""
    __tablename__ = 'announcements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)




# ═══════════════════════════════════════════════════
# PROPERTY TYPE TAXONOMY (Partner Hub 2.0)
# ═══════════════════════════════════════════════════
PROPERTY_TYPES = [
    {'key': 'hotel',            'icon': 'fa-hotel',            'group': 'stay'},
    {'key': 'boutique_hotel',   'icon': 'fa-star',             'group': 'stay'},
    {'key': 'luxury_hotel',     'icon': 'fa-gem',              'group': 'stay'},
    {'key': 'resort',           'icon': 'fa-umbrella-beach',   'group': 'stay'},
    {'key': 'spa_resort',       'icon': 'fa-spa',              'group': 'stay'},
    {'key': 'eco_resort',       'icon': 'fa-leaf',             'group': 'stay'},
    {'key': 'villa',            'icon': 'fa-house-chimney',    'group': 'stay'},
    {'key': 'holiday_house',    'icon': 'fa-house',            'group': 'stay'},
    {'key': 'guesthouse',       'icon': 'fa-house-user',       'group': 'stay'},
    {'key': 'apartment',        'icon': 'fa-building',         'group': 'stay'},
    {'key': 'hostel',           'icon': 'fa-bed',              'group': 'stay'},
    {'key': 'camping',          'icon': 'fa-campground',       'group': 'outdoor'},
    {'key': 'glamping',         'icon': 'fa-tent',             'group': 'outdoor'},
    {'key': 'mountain_resort',  'icon': 'fa-mountain',         'group': 'outdoor'},
    {'key': 'sanatorium',       'icon': 'fa-heart-pulse',      'group': 'stay'},
    {'key': 'restaurant',       'icon': 'fa-utensils',         'group': 'venue'},
    {'key': 'conference_hall',  'icon': 'fa-chalkboard-user',  'group': 'venue'},
    {'key': 'event_venue',      'icon': 'fa-champagne-glasses','group': 'venue'},
    {'key': 'transfer_company', 'icon': 'fa-shuttle-van',      'group': 'service'},
    {'key': 'travel_agency',    'icon': 'fa-suitcase-rolling', 'group': 'service'},
    {'key': 'tour_operator',    'icon': 'fa-route',            'group': 'service'},
    {'key': 'guide',            'icon': 'fa-person-walking-luggage', 'group': 'service'},
]
PROPERTY_TYPE_KEYS = [t['key'] for t in PROPERTY_TYPES]


# ═══════════════════════════════════════════════════
# Property completion & onboarding helpers
# ═══════════════════════════════════════════════════
def _property_completion(self):
    """Returns 0-100 completion score for a property listing."""
    gallery_count = 0
    if self.gallery:
        try:
            gallery_count = len(json.loads(self.gallery))
        except Exception:
            gallery_count = 1 if self.gallery else 0
    checks = [
        bool(self.name),
        bool(self.description and len(self.description) >= 40),
        bool(self.city and self.address),
        bool(self.cover_image),
        gallery_count >= 3,
        bool(self.video_url),
        self.rooms.count() > 0,
        any([self.has_wifi, self.has_pool, self.has_spa, self.has_gym, self.has_restaurant]),
        bool(self.cancellation_policy),
        self.status == 'published',
    ]
    return round(sum(checks) / len(checks) * 100)

Property.completion_percent = property(_property_completion)


def _agency_onboarding_steps(self):
    """Returns ordered onboarding checklist with completion booleans."""
    has_property = self.properties.count() > 0
    first_prop = self.properties.first()
    has_photos = bool(first_prop and first_prop.gallery)
    has_video = bool(first_prop and first_prop.video_url)
    has_rooms = bool(first_prop and first_prop.rooms.count() > 0)
    has_pricing = bool(first_prop and first_prop.rooms.filter(Room.base_price.isnot(None)).count() > 0)
    has_published = self.properties.filter_by(status='published').count() > 0
    has_booking = self.bookings.count() > 0

    steps = [
        {'key': 'verify',   'label_en': 'Verify company',            'label_ru': 'Подтвердить компанию',       'done': self.status == 'active'},
        {'key': 'property', 'label_en': 'Add first property',        'label_ru': 'Добавить первый объект',     'done': has_property},
        {'key': 'photos',   'label_en': 'Upload photos',              'label_ru': 'Загрузить фото',             'done': has_photos},
        {'key': 'video',    'label_en': 'Upload drone video',         'label_ru': 'Загрузить дрон-видео',       'done': has_video},
        {'key': 'rooms',    'label_en': 'Add rooms',                  'label_ru': 'Добавить номера',            'done': has_rooms},
        {'key': 'pricing',  'label_en': 'Configure pricing',          'label_ru': 'Настроить цены',             'done': has_pricing},
        {'key': 'calendar', 'label_en': 'Configure availability',     'label_ru': 'Настроить календарь',        'done': has_rooms},
        {'key': 'publish',  'label_en': 'Publish property',           'label_ru': 'Опубликовать объект',        'done': has_published},
        {'key': 'booking',  'label_en': 'Receive first booking',      'label_ru': 'Получить первое бронирование','done': has_booking},
    ]
    done_count = sum(1 for s in steps if s['done'])
    percent = round(done_count / len(steps) * 100)
    return {'steps': steps, 'done_count': done_count, 'total': len(steps), 'percent': percent}

Agency.onboarding = property(_agency_onboarding_steps)
