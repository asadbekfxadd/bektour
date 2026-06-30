"""
Bek Tour — Uzbekistan Tourism Platform
Seed with internal SVG photo routes (no external dependencies)
"""
from app import create_app
from app.models.models import db, Country, Villa, Service, Review

app = create_app()
with app.app_context():
    db.create_all()  # ensures new B2B platform tables exist
    Review.query.delete()
    Villa.query.delete()
    Service.query.delete()
    Country.query.delete()
    db.session.commit()

    countries = [
        Country(name_en='Samarkand', name_ru='Самарканд', code='UZ', is_popular=True,
                image='/photo/samarkand?w=700&h=900'),
        Country(name_en='Bukhara', name_ru='Бухара', code='UZ', is_popular=True,
                image='/photo/bukhara?w=700&h=500'),
        Country(name_en='Khiva', name_ru='Хива', code='UZ', is_popular=True,
                image='/photo/khiva?w=700&h=500'),
        Country(name_en='Tashkent', name_ru='Ташкент', code='UZ', is_popular=True,
                image='/photo/tashkent?w=700&h=500'),
        Country(name_en='Fergana Valley', name_ru='Ферганская долина', code='UZ', is_popular=True,
                image='/photo/fergana?w=700&h=500'),
    ]
    db.session.add_all(countries)
    db.session.flush()
    c_sam, c_bux, c_khv, c_tsh, c_fer = countries

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
