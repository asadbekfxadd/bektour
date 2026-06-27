from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.models import Villa, Country, Service

main_bp = Blueprint('main', __name__)

TRANSLATIONS = {
    'en': {
        'nav_home': 'Home', 'nav_villas': 'Villas', 'nav_services': 'Services',
        'nav_about': 'About', 'nav_contacts': 'Contacts',
        'hero_eyebrow': 'Premium Villa Rentals',
        'hero_title': 'Your <em>Luxury</em><br>Villa Awaits',
        'hero_desc': 'Handpicked villas across 50+ countries. Private pools, beachfront locations, world-class service.',
        'btn_browse': 'Browse Villas', 'btn_services': 'Our Services',
        'search_dest': 'Destination', 'search_checkin': 'Check In',
        'search_guests': 'Guests', 'btn_search': 'Search',
        'dest_title': 'Top Locations', 'dest_sub': 'From tropical islands to European coastlines',
        'feat_title': 'Featured Villas', 'feat_sub': 'Handpicked luxury properties',
        'btn_view': 'View Villa', 'btn_all': 'All Villas',
        'from_label': 'FROM', 'per_night': '/ night',
        'stat_villas': 'Luxury Villas', 'stat_countries': 'Countries',
        'stat_guests': 'Happy Guests', 'stat_service': 'Concierge Service',
        'serv_title': 'Everything You Need', 'serv_sub': 'Complete luxury experience',
        'serv_transfer': 'Airport Transfer', 'serv_car': 'Car Rental',
        'serv_yacht': 'Yacht Charter', 'serv_guide': 'Private Guide',
        'b2b_title': 'B2B Partnership Program', 'b2b_sub': 'Special rates for travel agencies worldwide.',
        'btn_partner': 'Become a Partner',
        'footer_desc': 'Premium villa rentals worldwide. Your luxury getaway starts here.',
        'login': 'Login', 'register': 'Register', 'logout': 'Logout',
        'profile': 'Profile', 'admin': 'Admin', 'b2b': 'B2B',
    },
    'ru': {
        'nav_home': 'Главная', 'nav_villas': 'Виллы', 'nav_services': 'Услуги',
        'nav_about': 'О нас', 'nav_contacts': 'Контакты',
        'hero_eyebrow': 'Премиальная аренда вилл',
        'hero_title': 'Ваша <em>Роскошная</em><br>Вилла Ждёт',
        'hero_desc': 'Отборные виллы в 50+ странах. Частные бассейны, пляжные локации, первоклассный сервис.',
        'btn_browse': 'Смотреть виллы', 'btn_services': 'Наши услуги',
        'search_dest': 'Направление', 'search_checkin': 'Заезд',
        'search_guests': 'Гости', 'btn_search': 'Поиск',
        'dest_title': 'Топ направлений', 'dest_sub': 'От тропических островов до европейских побережий',
        'feat_title': 'Избранные виллы', 'feat_sub': 'Отборные роскошные объекты',
        'btn_view': 'Подробнее', 'btn_all': 'Все виллы',
        'from_label': 'ОТ', 'per_night': '/ ночь',
        'stat_villas': 'Роскошных вилл', 'stat_countries': 'Стран',
        'stat_guests': 'Довольных гостей', 'stat_service': 'Консьерж сервис',
        'serv_title': 'Всё что нужно', 'serv_sub': 'Полный роскошный опыт',
        'serv_transfer': 'Трансфер из аэропорта', 'serv_car': 'Аренда авто',
        'serv_yacht': 'Аренда яхты', 'serv_guide': 'Частный гид',
        'b2b_title': 'Программа для агентств', 'b2b_sub': 'Специальные тарифы для турагентств.',
        'btn_partner': 'Стать партнёром',
        'footer_desc': 'Премиальная аренда вилл по всему миру.',
        'login': 'Войти', 'register': 'Регистрация', 'logout': 'Выйти',
        'profile': 'Профиль', 'admin': 'Админка', 'b2b': 'B2B',
    },
    'uz': {
        'nav_home': 'Bosh sahifa', 'nav_villas': 'Villalar', 'nav_services': 'Xizmatlar',
        'nav_about': 'Biz haqimizda', 'nav_contacts': 'Aloqa',
        'hero_eyebrow': 'Premium Villa Ijarasi',
        'hero_title': 'Sizning <em>Hashamatli</em><br>Villangiz Kutmoqda',
        'hero_desc': "50+ mamlakatda tanlangan villalar. Shaxsiy hovuzlar, qirg'oq joylashuvi.",
        'btn_browse': "Villalarni ko'rish", 'btn_services': 'Xizmatlarimiz',
        'search_dest': "Yo'nalish", 'search_checkin': 'Kirish',
        'search_guests': 'Mehmonlar', 'btn_search': 'Qidirish',
        'dest_title': 'Top manzillar', 'dest_sub': "Tropik orollardan Yevropa qirg'oqlarigacha",
        'feat_title': 'Tanlangan villalar', 'feat_sub': 'Eng yaxshi hashamatli ob\'ektlar',
        'btn_view': 'Batafsil', 'btn_all': 'Barcha villalar',
        'from_label': 'DAN', 'per_night': '/ kecha',
        'stat_villas': 'Hashamatli villalar', 'stat_countries': 'Mamlakatlar',
        'stat_guests': 'Mamnun mehmonlar', 'stat_service': 'Konsyerj xizmati',
        'serv_title': 'Sizga kerak bo\'lgan hamma narsa', 'serv_sub': "To'liq hashamatli tajriba",
        'serv_transfer': 'Aeroport transferi', 'serv_car': 'Avtomobil ijarasi',
        'serv_yacht': 'Yaxta ijarasi', 'serv_guide': 'Shaxsiy gid',
        'b2b_title': 'B2B Hamkorlik dasturi', 'b2b_sub': 'Sayohat agentliklari uchun maxsus narxlar.',
        'btn_partner': "Hamkor bo'lish",
        'footer_desc': 'Butun dunyoda premium villa ijarasi.',
        'login': 'Kirish', 'register': "Ro'yxatdan o'tish", 'logout': 'Chiqish',
        'profile': 'Profil', 'admin': 'Admin', 'b2b': 'B2B',
    }
}

class TDict:
    def __init__(self, d):
        self._d = d
    def __getattr__(self, key):
        return self._d.get(key, key)

@main_bp.route('/lang/<lang>')
def set_lang(lang):
    if lang in ['en', 'ru', 'uz']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('main.index'))

@main_bp.context_processor
def inject_lang():
    lang = session.get('lang', 'en')
    return dict(lang=lang, t=TDict(TRANSLATIONS.get(lang, TRANSLATIONS['en'])))

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
