"""
Bek Tour — Uzbekistan Tourism Platform
Seed with internal SVG photo routes (no external dependencies)
"""
from app import create_app
from app.models.models import db, Country, Villa, Service, Review, DestinationMedia
import json

app = create_app()
with app.app_context():
    db.create_all()  # ensures new B2B platform + destination tables exist
    DestinationMedia.query.delete()
    Review.query.delete()
    Villa.query.delete()
    Service.query.delete()
    Country.query.delete()
    db.session.commit()

    countries = [
        Country(name_en='Samarkand', name_ru='Самарканд', code='UZ', is_popular=True,
                image='/photo/samarkand?w=700&h=900',
                slug='samarkand', is_unesco=True,
                subtitle_en='The Pearl of the Silk Road', subtitle_ru='Жемчужина Шёлкового Пути',
                description_en='Samarkand is one of the oldest continuously inhabited cities in Central Asia, founded over 2,750 years ago. Once the capital of Tamerlane\'s empire, its turquoise-domed madrasas and the legendary Registan Square represent the pinnacle of Islamic architecture along the Silk Road.',
                description_ru='Самарканд — один из старейших непрерывно населённых городов Центральной Азии, основанный более 2750 лет назад. Когда-то столица империи Тамерлана, его бирюзовые купола медресе и легендарная площадь Регистан являются вершиной исламской архитектуры Шёлкового пути.',
                best_season_en='April – June', best_season_ru='Апрель – Июнь',
                avg_temp='18–32°C', population='550,000+', area_km2='112 km²',
                founded_year='8th century BC', travel_time_en='4h from Tashkent', travel_time_ru='4ч от Ташкента',
                top_attractions=json.dumps([
                    {'name_en': 'Registan Square', 'name_ru': 'Площадь Регистан', 'image': '/photo/samarkand?w=600&h=800&v=1'},
                    {'name_en': 'Gur-e-Amir Mausoleum', 'name_ru': 'Мавзолей Гур-Эмир', 'image': '/photo/samarkand?w=600&h=800&v=2'},
                    {'name_en': 'Shah-i-Zinda Necropolis', 'name_ru': 'Некрополь Шахи-Зинда', 'image': '/photo/samarkand?w=600&h=800&v=3'},
                ])),
        Country(name_en='Bukhara', name_ru='Бухара', code='UZ', is_popular=True,
                image='/photo/bukhara?w=700&h=500',
                slug='bukhara', is_unesco=True,
                subtitle_en='The Holy City of Central Asia', subtitle_ru='Священный Город Центральной Азии',
                description_en='Bukhara\'s historic center is one of the best-preserved medieval cities in the Islamic world, with over 140 protected monuments. Its labyrinthine bazaars and the towering Kalon Minaret have witnessed 2,500 years of Silk Road trade.',
                description_ru='Исторический центр Бухары — один из наиболее сохранившихся средневековых городов исламского мира, с более чем 140 охраняемыми памятниками. Его лабиринты базаров и возвышающийся минарет Калон видели 2500 лет торговли на Шёлковом пути.',
                best_season_en='March – May', best_season_ru='Март – Май',
                avg_temp='16–35°C', population='280,000+', area_km2='143 km²',
                founded_year='6th century BC', travel_time_en='5h from Tashkent', travel_time_ru='5ч от Ташкента',
                top_attractions=json.dumps([
                    {'name_en': 'Kalon Minaret', 'name_ru': 'Минарет Калон', 'image': '/photo/bukhara?w=600&h=800&v=1'},
                    {'name_en': 'Ark Citadel', 'name_ru': 'Цитадель Арк', 'image': '/photo/bukhara?w=600&h=800&v=2'},
                    {'name_en': 'Lyab-i Hauz', 'name_ru': 'Ляби-Хауз', 'image': '/photo/bukhara?w=600&h=800&v=3'},
                ])),
        Country(name_en='Khiva', name_ru='Хива', code='UZ', is_popular=True,
                image='/photo/khiva?w=700&h=500',
                slug='khiva', is_unesco=True,
                subtitle_en='The Open-Air Museum City', subtitle_ru='Город-музей под открытым небом',
                description_en='Khiva\'s Itchan Kala is a perfectly preserved walled inner city — the first site in Uzbekistan inscribed on the UNESCO World Heritage List. Walking its streets feels like stepping into a living 10th-century oasis.',
                description_ru='Ичан-Кала в Хиве — идеально сохранившийся внутренний город-крепость, первый объект Узбекистана в списке Всемирного наследия ЮНЕСКО. Прогулка по его улицам ощущается как путешествие в живой оазис X века.',
                best_season_en='April – May', best_season_ru='Апрель – Май',
                avg_temp='14–38°C', population='95,000+', area_km2='26 km²',
                founded_year='10th century', travel_time_en='1h flight from Tashkent', travel_time_ru='1ч перелёт из Ташкента',
                top_attractions=json.dumps([
                    {'name_en': 'Itchan Kala Walls', 'name_ru': 'Стены Ичан-Кала', 'image': '/photo/khiva?w=600&h=800&v=1'},
                    {'name_en': 'Kalta Minor Minaret', 'name_ru': 'Минарет Кальта-Минор', 'image': '/photo/khiva?w=600&h=800&v=2'},
                ])),
        Country(name_en='Tashkent', name_ru='Ташкент', code='UZ', is_popular=True,
                image='/photo/tashkent?w=700&h=500',
                slug='tashkent', is_unesco=False,
                subtitle_en='Capital City & Gateway to Amirsay', subtitle_ru='Столица и ворота в Амирсай',
                description_en='Uzbekistan\'s modern capital blends Soviet-era metro art, leafy boulevards and a fast-growing skyline, with the Amirsay mountain resort just an hour away for skiing and hiking.',
                description_ru='Современная столица Узбекистана сочетает искусство метро советской эпохи, тенистые бульвары и быстрорастущий горизонт, а горнолыжный курорт Амирсай находится всего в часе езды.',
                best_season_en='Year-round', best_season_ru='Круглый год',
                avg_temp='8–35°C', population='2,500,000+', area_km2='335 km²',
                founded_year='2nd century BC', travel_time_en='Main international gateway', travel_time_ru='Главные международные ворота',
                top_attractions=json.dumps([
                    {'name_en': 'Chorsu Bazaar', 'name_ru': 'Базар Чорсу', 'image': '/photo/tashkent?w=600&h=800&v=1'},
                    {'name_en': 'Amirsay Mountain Resort', 'name_ru': 'Курорт Амирсай', 'image': '/photo/tashkent?w=600&h=800&v=2'},
                ])),
        Country(name_en='Fergana Valley', name_ru='Ферганская долина', code='UZ', is_popular=True,
                image='/photo/fergana?w=700&h=500',
                slug='fergana', is_unesco=False,
                subtitle_en='Silk & Craftsmanship of the Valley', subtitle_ru='Шёлк и ремёсла долины',
                description_en='The fertile Fergana Valley is the birthplace of Uzbek silk weaving and ceramics, with the historic Margilan silk workshops still producing handmade ikat fabric using centuries-old techniques.',
                description_ru='Плодородная Ферганская долина — родина узбекского шёлкоткачества и керамики, а исторические шёлковые мастерские Маргилана до сих пор производят ткань икат вручную по многовековым технологиям.',
                best_season_en='September – November', best_season_ru='Сентябрь – Ноябрь',
                avg_temp='10–34°C', population='4,000,000+ (valley)', area_km2='22,000 km² (valley)',
                founded_year='Ancient Silk Road hub', travel_time_en='5h from Tashkent', travel_time_ru='5ч от Ташкента',
                top_attractions=json.dumps([
                    {'name_en': 'Margilan Silk Workshops', 'name_ru': 'Шёлковые мастерские Маргилана', 'image': '/photo/fergana?w=600&h=800&v=1'},
                ])),
    ]
    db.session.add_all(countries)
    db.session.flush()
    c_sam, c_bux, c_khv, c_tsh, c_fer = countries

    # Sample video gallery clips per destination (video_url left blank —
    # safe no-op until real footage is added; poster images render immediately)
    media_clips = [
        DestinationMedia(country_id=c_sam.id, media_type='drone', order=1,
                          title_en='Registan at Sunrise', title_ru='Регистан на рассвете',
                          poster_image='/photo/samarkand?w=600&h=450&v=1'),
        DestinationMedia(country_id=c_sam.id, media_type='night', order=2,
                          title_en='Registan Light Show', title_ru='Световое шоу Регистана',
                          poster_image='/photo/samarkand?w=600&h=450&v=2'),
        DestinationMedia(country_id=c_sam.id, media_type='walking', order=3,
                          title_en='Walking the Old Bazaar', title_ru='Прогулка по старому базару',
                          poster_image='/photo/samarkand?w=600&h=450&v=3'),
        DestinationMedia(country_id=c_bux.id, media_type='drone', order=1,
                          title_en='Old City Aerial View', title_ru='Аэросъёмка старого города',
                          poster_image='/photo/bukhara?w=600&h=450&v=1'),
        DestinationMedia(country_id=c_bux.id, media_type='food', order=2,
                          title_en='Traditional Bukharan Plov', title_ru='Традиционный бухарский плов',
                          poster_image='/photo/bukhara?w=600&h=450&v=2'),
        DestinationMedia(country_id=c_khv.id, media_type='drone', order=1,
                          title_en='Ichan Kala Drone Footage', title_ru='Дрон-съёмка Ичан-Кала',
                          poster_image='/photo/khiva?w=600&h=450&v=1'),
        DestinationMedia(country_id=c_tsh.id, media_type='night', order=1,
                          title_en='Modern Skyline at Sunset', title_ru='Современный горизонт на закате',
                          poster_image='/photo/tashkent?w=600&h=450&v=1'),
        DestinationMedia(country_id=c_fer.id, media_type='market', order=1,
                          title_en='Silk Market in Margilan', title_ru='Шёлковый рынок в Маргилане',
                          poster_image='/photo/fergana?w=600&h=450&v=1'),
    ]
    db.session.add_all(media_clips)
    db.session.flush()


    villas = [
        Villa(title_en='Registan View Hotel', title_ru='Отель Регистан',
              slug='registan-view-hotel', country_id=c_sam.id, city='Samarkand',
              description_en='Wake up to views of the magnificent Registan Square — the crown jewel of the Silk Road, 200m from your door.',
              description_ru='Просыпайтесь с видом на Регистан — главную площадь Шёлкового пути.',
              price_per_night=180, bedrooms=1, bathrooms=1, guests=2,
              has_wifi=True, has_ac=True, is_active=True, is_featured=True, rating=4.9,
              cover_image='/photo/samarkand?w=800&h=600'),
        Villa(title_en='Silk Road Boutique Hotel', title_ru='Бутик-отель Шёлковый Путь',
              slug='silk-road-boutique', country_id=c_bux.id, city='Bukhara',
              description_en='A restored 16th-century caravanserai in the heart of ancient Bukhara. Traditional architecture meets modern luxury.',
              description_ru='Отреставрированный каравансарай XVI века в центре древней Бухары.',
              price_per_night=150, bedrooms=1, bathrooms=1, guests=2,
              has_wifi=True, has_ac=True, is_active=True, is_featured=True, rating=4.8,
              cover_image='/photo/bukhara?w=800&h=600'),
        Villa(title_en='Ichan Kala Palace Hotel', title_ru='Дворец Ичан-Кала',
              slug='ichan-kala-palace', country_id=c_khv.id, city='Khiva',
              description_en='Experience living history inside Khiva\'s ancient walled city. Breathtaking views of the Kalta Minor minaret.',
              description_ru='Живая история внутри городской крепости Хивы.',
              price_per_night=130, bedrooms=2, bathrooms=1, guests=4,
              has_wifi=True, has_ac=True, is_active=True, is_featured=True, rating=4.7,
              cover_image='/photo/khiva?w=800&h=600'),
        Villa(title_en='Tashkent Grand Residence', title_ru='Гранд Резиденция Ташкент',
              slug='tashkent-grand-residence', country_id=c_tsh.id, city='Tashkent',
              description_en='Modern luxury villa with private pool near Amirsay mountain resort. City culture meets mountain nature.',
              description_ru='Современная вилла с бассейном рядом с горнолыжным курортом Амирсай.',
              price_per_night=220, bedrooms=3, bathrooms=2, guests=6,
              has_pool=True, has_wifi=True, has_parking=True, has_ac=True,
              is_active=True, is_featured=True, rating=4.9,
              cover_image='/photo/tashkent?w=800&h=600'),
        Villa(title_en='Fergana Silk Haveli', title_ru='Хавели Ферганский Шёлк',
              slug='fergana-silk-haveli', country_id=c_fer.id, city='Fergana',
              description_en='Traditional Uzbek mansion in mulberry gardens — birthplace of Silk Road craftsmanship. Private silk weaving demos.',
              description_ru='Узбекский особняк в шелковичных садах Ферганской долины.',
              price_per_night=100, bedrooms=2, bathrooms=1, guests=4,
              has_wifi=True, has_ac=True, is_active=True, is_featured=True, rating=4.6,
              cover_image='/photo/fergana?w=800&h=600'),
        Villa(title_en='Blue Dome Samarkand Suite', title_ru='Апартаменты Голубой Купол',
              slug='blue-dome-samarkand', country_id=c_sam.id, city='Samarkand',
              description_en='Rooftop views of Samarkand\'s iconic blue-tiled domes. Traditional hammam and authentic plov.',
              description_ru='Вид с крыши на голубые купола Самарканда.',
              price_per_night=160, bedrooms=1, bathrooms=1, guests=2,
              has_wifi=True, has_ac=True, is_active=True, is_featured=False, rating=4.7,
              cover_image='/photo/samarkand?w=800&h=600'),
    ]
    db.session.add_all(villas)
    db.session.flush()

    services = [
        Service(title_en='Airport Transfer', title_ru='Трансфер из аэропорта',
                slug='airport-transfer', category='transfer',
                description_en='Premium airport transfers. Meet & greet. 24/7.', price_from=35, is_active=True),
        Service(title_en='Luxury Car Rental', title_ru='Аренда автомобиля',
                slug='car-rental', category='car',
                description_en='Mercedes, BMW, SUV fleet. Driver optional.', price_from=60, is_active=True),
        Service(title_en='Yacht Charter', title_ru='Аренда яхты',
                slug='yacht-charter', category='yacht',
                description_en='Private yacht on Charvak reservoir.', price_from=200, is_active=True),
        Service(title_en='Private Guide', title_ru='Частный гид',
                slug='private-guide', category='guide',
                description_en='Licensed guides in 10+ languages.', price_from=80, is_active=True),
    ]
    db.session.add_all(services)
    db.session.flush()

    reviews = [
        Review(villa_id=villas[0].id, rating=5, is_approved=True,
               text='The Registan view was beyond words. Bek Tour arranged everything perfectly.'),
        Review(villa_id=villas[1].id, rating=5, is_approved=True,
               text='Bukhara is magical and the hotel made it even more special. Highly recommend!'),
        Review(villa_id=villas[2].id, rating=5, is_approved=True,
               text='Khiva felt like a fairy tale. Best hotel on our whole Central Asia trip.'),
    ]
    db.session.add_all(reviews)
    db.session.commit()

    print('✅ Uzbekistan data seeded!')
    print(f'   Countries: {len(countries)}')
    print(f'   Hotels: {len(villas)}')
    print(f'   Services: {len(services)}')
    print(f'   Destination media clips: {len(media_clips)}')
