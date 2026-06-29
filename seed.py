"""
Bek Tour — Uzbekistan Tourism Platform
Complete seed with real Uzbekistan photos from Unsplash
"""
from app import create_app
from app.models.models import db, Country, Villa, Service, Review

def img(photo_id, w=800, h=600):
    return f"https://images.unsplash.com/{photo_id}?w={w}&h={h}&fit=crop&q=80"

app = create_app()
with app.app_context():
    # Clear existing
    Review.query.delete()
    Villa.query.delete()
    Service.query.delete()
    Country.query.delete()
    db.session.commit()

    # Countries with real Uzbekistan photos
    countries = [
        Country(name_en='Samarkand', name_ru='Самарканд', code='UZ', is_popular=True,
                image=img('photo-1589646694432-53cb95e1de20', 800, 600)),
        Country(name_en='Bukhara', name_ru='Бухара', code='UZ', is_popular=True,
                image=img('photo-1624005340954-c9a32e71e3f7', 800, 600)),
        Country(name_en='Khiva', name_ru='Хива', code='UZ', is_popular=True,
                image=img('photo-1617196034183-421b4040ed20', 800, 600)),
        Country(name_en='Tashkent', name_ru='Ташкент', code='UZ', is_popular=True,
                image=img('photo-1589139862500-d8a5ef1b38ab', 800, 600)),
        Country(name_en='Fergana Valley', name_ru='Ферганская долина', code='UZ', is_popular=True,
                image=img('photo-1558618666-fcd25c85cd64', 800, 600)),
    ]
    db.session.add_all(countries)
    db.session.flush()

    c_sam, c_bux, c_khv, c_tsh, c_fer = countries

    villas = [
        Villa(
            title_en='Registan View Hotel', title_ru='Отель Вид на Регистан',
            slug='registan-view-hotel', country_id=c_sam.id, city='Samarkand',
            description_en='Wake up to views of the magnificent Registan Square. This luxury boutique hotel sits 200m from the UNESCO World Heritage site, offering an unparalleled connection to Samarkand\'s ancient grandeur.',
            description_ru='Просыпайтесь с видом на величественную площадь Регистан. Этот роскошный бутик-отель находится в 200 м от объекта ЮНЕСКО.',
            price_per_night=180, bedrooms=1, bathrooms=1, guests=2,
            has_wifi=True, has_ac=True, is_active=True, is_featured=True, rating=4.9,
            cover_image=img('photo-1589646694432-53cb95e1de20'),
        ),
        Villa(
            title_en='Silk Road Boutique Hotel', title_ru='Бутик-отель Шёлковый Путь',
            slug='silk-road-boutique', country_id=c_bux.id, city='Bukhara',
            description_en='A beautifully restored 16th century caravanserai in the heart of ancient Bukhara. Traditional architecture meets modern luxury in this award-winning property.',
            description_ru='Красиво отреставрированный каравансарай XVI века в самом сердце древней Бухары.',
            price_per_night=150, bedrooms=1, bathrooms=1, guests=2,
            has_wifi=True, has_ac=True, is_active=True, is_featured=True, rating=4.8,
            cover_image=img('photo-1624005340954-c9a32e71e3f7'),
        ),
        Villa(
            title_en='Ichan Kala Palace Hotel', title_ru='Дворец-отель Ичан-Кала',
            slug='ichan-kala-palace', country_id=c_khv.id, city='Khiva',
            description_en='Experience living history inside Khiva\'s ancient walled city. This palace-hotel offers authentic architecture, courtyard gardens and breathtaking views of the Kalta Minor minaret.',
            description_ru='Почувствуйте живую историю внутри древнего города-крепости Хивы.',
            price_per_night=130, bedrooms=2, bathrooms=1, guests=4,
            has_wifi=True, has_ac=True, is_active=True, is_featured=True, rating=4.7,
            cover_image=img('photo-1617196034183-421b4040ed20'),
        ),
        Villa(
            title_en='Tashkent Grand Residence', title_ru='Ташкент Гранд Резиденция',
            slug='tashkent-grand-residence', country_id=c_tsh.id, city='Tashkent',
            description_en='A modern luxury villa with private pool near the Amirsay mountain resort. Perfect base for exploring the capital and nearby mountains, combining city culture with nature.',
            description_ru='Современная роскошная вилла с бассейном рядом с горнолыжным курортом Амирсай.',
            price_per_night=220, bedrooms=3, bathrooms=2, guests=6,
            has_pool=True, has_wifi=True, has_parking=True, has_ac=True,
            is_active=True, is_featured=True, rating=4.9,
            cover_image=img('photo-1566073771259-6a8506099945'),
        ),
        Villa(
            title_en='Fergana Silk Haveli', title_ru='Хавели Ферганский Шёлк',
            slug='fergana-silk-haveli', country_id=c_fer.id, city='Fergana',
            description_en='A traditional Uzbek mansion surrounded by mulberry gardens in the heart of the Fergana Valley — the birthplace of Silk Road craftsmanship. Private silk weaving demonstrations available.',
            description_ru='Традиционный узбекский особняк в шелковичных садах Ферганской долины.',
            price_per_night=100, bedrooms=2, bathrooms=1, guests=4,
            has_wifi=True, has_ac=True, is_active=True, is_featured=True, rating=4.6,
            cover_image=img('photo-1558618666-fcd25c85cd64'),
        ),
        Villa(
            title_en='Blue Dome Samarkand Suite', title_ru='Апартаменты Голубой Купол',
            slug='blue-dome-samarkand', country_id=c_sam.id, city='Samarkand',
            description_en='Elegant suites with rooftop views of Samarkand\'s iconic blue-tiled domes. The hotel features a traditional Uzbek hammam and serves authentic plov cooked in a kazan.',
            description_ru='Изысканные апартаменты с видом на голубые купола Самарканда с крыши.',
            price_per_night=160, bedrooms=1, bathrooms=1, guests=2,
            has_wifi=True, has_ac=True, is_active=True, is_featured=False, rating=4.7,
            cover_image=img('photo-1539635278303-d4002c07eae3'),
        ),
    ]
    db.session.add_all(villas)
    db.session.flush()

    services = [
        Service(title_en='Airport Transfer', title_ru='Трансфер из аэропорта',
                slug='airport-transfer', category='transfer',
                description_en='Premium airport transfers in luxury vehicles. Meet & greet service included. Available 24/7.',
                price_from=35, is_active=True),
        Service(title_en='Luxury Car Rental', title_ru='Аренда автомобиля',
                slug='car-rental', category='car',
                description_en='Mercedes, BMW, and SUV fleet. Driver optional. Child seats available.',
                price_from=60, is_active=True),
        Service(title_en='Yacht Charter', title_ru='Аренда яхты',
                slug='yacht-charter', category='yacht',
                description_en='Private yacht charter on the Charvak reservoir. Sunset cruises and full-day trips.',
                price_from=200, is_active=True),
        Service(title_en='Private Guide', title_ru='Частный гид',
                slug='private-guide', category='guide',
                description_en='Licensed expert guides in 10+ languages. Historians, archaeologists, and cultural specialists.',
                price_from=80, is_active=True),
    ]
    db.session.add_all(services)

    # Seed approved reviews
    db.session.flush()
    reviews = [
        Review(villa_id=villas[0].id, rating=5, is_approved=True,
               text='The Registan view from our room was beyond words. Bek Tour arranged everything perfectly — from the airport pickup to the private guide at the monuments.'),
        Review(villa_id=villas[1].id, rating=5, is_approved=True,
               text='Bukhara is a magical city and the Silk Road Hotel made it even more special. The courtyard is stunning at night. Highly recommend!'),
        Review(villa_id=villas[2].id, rating=5, is_approved=True,
               text='Khiva felt like stepping into a fairy tale. The hotel inside Ichan Kala was the highlight of our whole Central Asia trip.'),
    ]
    db.session.add_all(reviews)
    db.session.commit()
    print('✅ Uzbekistan data seeded successfully!')
    print(f'   Countries: {len(countries)}')
    print(f'   Hotels/Villas: {len(villas)}')
    print(f'   Services: {len(services)}')
    print(f'   Reviews: {len(reviews)}')
