from flask import Flask, session
from flask_login import LoginManager
from flask_migrate import Migrate
from app.models.models import db, User

login_manager = LoginManager()
migrate = Migrate()

TRANSLATIONS = {
    'en': {
        'nav_home': 'Home', 'nav_villas': 'Hotels & Villas', 'nav_services': 'Services',
        'nav_about': 'About', 'nav_contacts': 'Contacts',
        'hero_eyebrow': 'Premium Villa Rentals',
        'hero_title': 'Your <em>Luxury</em><br>Villa Awaits',
        'hero_desc': 'Handpicked villas and hotels across Uzbekistan and worldwide.',
        'btn_browse': 'Browse Villas', 'btn_services': 'Our Services',
        'search_dest': 'Destination', 'search_checkin': 'Check In',
        'search_guests': 'Guests', 'btn_search': 'Search',
        'dest_title': 'Top Uzbekistan Regions', 'dest_sub': 'From the Silk Road to the Aral Sea',
        'feat_title': 'Featured Stays', 'feat_sub': 'Handpicked luxury properties',
        'btn_view': 'View', 'btn_all': 'All Properties',
        'from_label': 'FROM', 'per_night': '/ night',
        'stat_villas': 'Properties', 'stat_countries': 'Countries',
        'stat_guests': 'Happy Guests', 'stat_service': 'Concierge',
        'serv_title': 'Everything You Need', 'serv_sub': 'Complete travel experience in Uzbekistan',
        'serv_transfer': 'Airport Transfer', 'serv_car': 'Car Rental',
        'serv_yacht': 'Yacht Charter', 'serv_guide': 'Private Guide',
        'b2b_title': 'B2B Partnership Program', 'b2b_sub': 'Special rates for travel agencies worldwide.',
        'btn_partner': 'Become a Partner',
        'footer_desc': 'Premium travel experiences in Uzbekistan and worldwide.',
        'login': 'Login', 'register': 'Register', 'logout': 'Logout',
        'profile': 'Profile', 'admin': 'Admin', 'b2b': 'B2B',
    },
    'ru': {
        'nav_home': 'Главная', 'nav_villas': 'Отели и Виллы', 'nav_services': 'Услуги',
        'nav_about': 'О нас', 'nav_contacts': 'Контакты',
        'hero_eyebrow': 'Премиальная аренда вилл',
        'hero_title': 'Ваша <em>Роскошная</em><br>Вилла Ждёт',
        'hero_desc': 'Отборные виллы и отели по всему Узбекистану и миру.',
        'btn_browse': 'Найти жильё', 'btn_services': 'Наши услуги',
        'search_dest': 'Направление', 'search_checkin': 'Заезд',
        'search_guests': 'Гости', 'btn_search': 'Поиск',
        'dest_title': 'Регионы Узбекистана', 'dest_sub': 'От Шёлкового пути до Аральского моря',
        'feat_title': 'Лучшие объекты', 'feat_sub': 'Отборные роскошные объекты',
        'btn_view': 'Подробнее', 'btn_all': 'Все объекты',
        'from_label': 'ОТ', 'per_night': '/ ночь',
        'stat_villas': 'Объектов', 'stat_countries': 'Стран',
        'stat_guests': 'Туристов', 'stat_service': 'Консьерж',
        'serv_title': 'Всё для вашего путешествия', 'serv_sub': 'Полный опыт путешествия по Узбекистану',
        'serv_transfer': 'Трансфер из аэропорта', 'serv_car': 'Аренда авто',
        'serv_yacht': 'Аренда яхты', 'serv_guide': 'Частный гид',
        'b2b_title': 'Программа для агентств', 'b2b_sub': 'Специальные тарифы для турагентств по всему миру.',
        'btn_partner': 'Стать партнёром',
        'footer_desc': 'Премиальный туризм в Узбекистане и по всему миру.',
        'login': 'Войти', 'register': 'Регистрация', 'logout': 'Выйти',
        'profile': 'Профиль', 'admin': 'Админка', 'b2b': 'B2B',
    },
    'uz': {
        'nav_home': 'Bosh sahifa', 'nav_villas': 'Mehmonxona va Villalar', 'nav_services': 'Xizmatlar',
        'nav_about': 'Biz haqimizda', 'nav_contacts': 'Aloqa',
        'hero_eyebrow': 'Premium Villa Ijarasi',
        'hero_title': "Sizning <em>Hashamatli</em><br>Villangiz Kutmoqda",
        'hero_desc': "O'zbekiston va butun dunyoda tanlangan villa va mehmonxonalar.",
        'btn_browse': "Joyni topish", 'btn_services': 'Xizmatlarimiz',
        'search_dest': "Yo'nalish", 'search_checkin': 'Kirish',
        'search_guests': 'Mehmonlar', 'btn_search': 'Qidirish',
        'dest_title': "O'zbekiston viloyatlari", 'dest_sub': "Ipak Yo'lidan Orol dengizigacha",
        'feat_title': 'Tanlangan turar joylar', 'feat_sub': "Eng yaxshi hashamatli ob'ektlar",
        'btn_view': 'Batafsil', 'btn_all': "Barcha ob'ektlar",
        'from_label': 'DAN', 'per_night': '/ kecha',
        'stat_villas': "Ob'ektlar", 'stat_countries': 'Mamlakatlar',
        'stat_guests': 'Sayyohlar', 'stat_service': 'Konsyerj',
        'serv_title': "Sayohatingiz uchun hamma narsa", 'serv_sub': "O'zbekistonda to'liq sayohat tajribasi",
        'serv_transfer': 'Aeroport transferi', 'serv_car': 'Avtomobil ijarasi',
        'serv_yacht': 'Yaxta ijarasi', 'serv_guide': 'Shaxsiy gid',
        'b2b_title': 'B2B Hamkorlik dasturi', 'b2b_sub': 'Sayohat agentliklari uchun maxsus narxlar.',
        'btn_partner': "Hamkor bo'lish",
        'footer_desc': "O'zbekiston va butun dunyoda premium sayohat tajribasi.",
        'login': 'Kirish', 'register': "Ro'yxatdan o'tish", 'logout': 'Chiqish',
        'profile': 'Profil', 'admin': 'Admin', 'b2b': 'B2B',
    }
}

class TDict:
    def __init__(self, d):
        self._d = d
    def __getattr__(self, key):
        return self._d.get(key, key)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.config.Config')

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_globals():
        lang = session.get('lang', 'en')
        return dict(lang=lang, t=TDict(TRANSLATIONS.get(lang, TRANSLATIONS['en'])))

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.villas import villas_bp
    from app.routes.services import services_bp
    from app.routes.admin import admin_bp
    from app.routes.b2b import b2b_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(villas_bp, url_prefix='/villas')
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(b2b_bp, url_prefix='/b2b')

    return app
