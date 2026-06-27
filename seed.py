from app import create_app
from app.models.models import db, Country, Villa, Service

app = create_app()
with app.app_context():
    c1 = Country(name_en='Maldives', name_ru='Maldivlar', code='MV', is_popular=True)
    c2 = Country(name_en='Bali', name_ru='Bali', code='ID', is_popular=True)
    c3 = Country(name_en='Dubai', name_ru='Dubai', code='AE', is_popular=True)
    c4 = Country(name_en='Mykonos', name_ru='Mykonos', code='GR', is_popular=True)
    c5 = Country(name_en='Santorini', name_ru='Santorini', code='GR', is_popular=True)
    c6 = Country(name_en='Phuket', name_ru='Phuket', code='TH', is_popular=True)
    db.session.add_all([c1,c2,c3,c4,c5,c6])
    db.session.flush()

    villas = [
        Villa(title_en='Sunset Paradise Villa', slug='sunset-paradise', country_id=c1.id, city='North Male', description_en='A stunning overwater villa with direct ocean access and private infinity pool.', price_per_night=850, price_per_week=5500, bedrooms=4, bathrooms=4, guests=8, area=420, has_pool=True, has_beach=True, has_wifi=True, has_ac=True, is_active=True, is_featured=True),
        Villa(title_en='Royal Bali Retreat', slug='royal-bali', country_id=c2.id, city='Seminyak', description_en='Luxury tropical villa surrounded by rice fields with a private pool.', price_per_night=450, price_per_week=2800, bedrooms=3, bathrooms=3, guests=6, area=350, has_pool=True, has_wifi=True, has_ac=True, is_active=True, is_featured=True),
        Villa(title_en='Dubai Marina Penthouse', slug='dubai-marina', country_id=c3.id, city='Dubai Marina', description_en='Ultra-luxury penthouse with panoramic views of the Dubai skyline.', price_per_night=1200, price_per_week=7500, bedrooms=5, bathrooms=5, guests=10, area=600, has_pool=True, has_ac=True, has_wifi=True, has_parking=True, is_active=True, is_featured=True),
        Villa(title_en='Mykonos Blue Villa', slug='mykonos-blue', country_id=c4.id, city='Mykonos Town', description_en='Iconic whitewashed villa with breathtaking Aegean sea views.', price_per_night=680, price_per_week=4200, bedrooms=3, bathrooms=2, guests=6, area=280, has_pool=True, has_beach=True, has_wifi=True, is_active=True, is_featured=True),
        Villa(title_en='Caldera Santorini Villa', slug='caldera-santorini', country_id=c5.id, city='Oia', description_en='Cliffside villa with legendary caldera views and private hot tub.', price_per_night=920, price_per_week=5800, bedrooms=2, bathrooms=2, guests=4, area=200, has_pool=True, has_beach=False, has_wifi=True, has_ac=True, is_active=True, is_featured=True),
        Villa(title_en='Phuket Oceanfront Estate', slug='phuket-oceanfront', country_id=c6.id, city='Patong Beach', description_en='Spacious beachfront estate with multiple pools and tropical gardens.', price_per_night=750, price_per_week=4800, bedrooms=6, bathrooms=6, guests=12, area=800, has_pool=True, has_beach=True, has_wifi=True, has_ac=True, has_parking=True, is_active=True, is_featured=False),
    ]
    db.session.add_all(villas)

    services = [
        Service(title_en='Airport Transfer', title_ru='Трансфер из аэропорта', slug='airport-transfer', category='transfer', price_from=50, is_active=True),
        Service(title_en='Car Rental', title_ru='Аренда автомобиля', slug='car-rental', category='car', price_from=150, is_active=True),
        Service(title_en='Yacht Charter', title_ru='Аренда яхты', slug='yacht-charter', category='yacht', price_from=500, is_active=True),
        Service(title_en='Private Guide', title_ru='Частный гид', slug='private-guide', category='guide', price_from=80, is_active=True),
    ]
    db.session.add_all(services)
    db.session.commit()
    print('Done! Data added successfully.')
