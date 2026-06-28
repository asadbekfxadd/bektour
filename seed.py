from app import create_app
from app.models.models import db, Country, Villa, Service

app = create_app()
with app.app_context():
    c1 = Country(name_en='Samarkand', name_ru='Самарканд', code='UZ', is_popular=True)
    c2 = Country(name_en='Bukhara', name_ru='Бухара', code='UZ', is_popular=True)
    c3 = Country(name_en='Khiva', name_ru='Хива', code='UZ', is_popular=True)
    c4 = Country(name_en='Tashkent', name_ru='Ташкент', code='UZ', is_popular=True)
    c5 = Country(name_en='Fergana Valley', name_ru='Фергана', code='UZ', is_popular=True)
    db.session.add_all([c1,c2,c3,c4,c5])
    db.session.flush()

    villas = [
        Villa(title_en='Registan View Hotel', slug='registan-view', country_id=c1.id, city='Samarkand', description_en='Luxury hotel with direct views of the Registan Square.', price_per_night=180, bedrooms=1, bathrooms=1, guests=2, has_wifi=True, has_ac=True, is_active=True, is_featured=True),
        Villa(title_en='Silk Road Boutique Hotel', slug='silk-road-boutique', country_id=c2.id, city='Bukhara', description_en='Authentic caravanserai transformed into a luxury boutique hotel.', price_per_night=150, bedrooms=1, bathrooms=1, guests=2, has_wifi=True, has_ac=True, is_active=True, is_featured=True),
        Villa(title_en='Ichan Kala Palace', slug='ichan-kala-palace', country_id=c3.id, city='Khiva', description_en='Historic palace inside the ancient walled city of Khiva.', price_per_night=120, bedrooms=2, bathrooms=1, guests=4, has_wifi=True, has_ac=True, is_active=True, is_featured=True),
        Villa(title_en='Tashkent Grand Residence', slug='tashkent-grand', country_id=c4.id, city='Tashkent', description_en='Modern luxury villa near Amirsay mountain resort.', price_per_night=200, bedrooms=3, bathrooms=2, guests=6, has_pool=True, has_wifi=True, has_parking=True, is_active=True, is_featured=True),
        Villa(title_en='Fergana Silk Villa', slug='fergana-silk', country_id=c5.id, city='Fergana', description_en='Traditional Uzbek mansion surrounded by mulberry gardens.', price_per_night=100, bedrooms=2, bathrooms=1, guests=4, has_wifi=True, has_ac=True, is_active=True, is_featured=True),
    ]
    db.session.add_all(villas)

    services = [
        Service(title_en='Airport Transfer', title_ru='Трансфер', slug='airport-transfer', category='transfer', price_from=35, is_active=True),
        Service(title_en='Car Rental', title_ru='Аренда авто', slug='car-rental', category='car', price_from=60, is_active=True),
        Service(title_en='Yacht Charter', title_ru='Яхта', slug='yacht', category='yacht', price_from=200, is_active=True),
        Service(title_en='Private Guide', title_ru='Гид', slug='private-guide', category='guide', price_from=80, is_active=True),
    ]
    db.session.add_all(services)
    db.session.commit()
    print('Done! Uzbekistan data added.')