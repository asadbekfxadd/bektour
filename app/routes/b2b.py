from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user, login_user
from app.models.models import (db, Agency, Booking, User, Property, Room, Tour,
                                 MediaAsset, PartnerCustomer, SupportTicket, Announcement, Villa,
                                 PROPERTY_TYPES, PROPERTY_TYPE_KEYS)
from datetime import datetime, timedelta
from sqlalchemy import func
import json

b2b_bp = Blueprint('b2b', __name__)


def get_agency_or_redirect():
    agency = Agency.query.filter_by(owner_id=current_user.id).first()
    return agency


# ═══════════════════════════════════════════════
# REGISTER (public, no login required to start)
# ═══════════════════════════════════════════════
@b2b_bp.route('/register', methods=['GET', 'POST'])
def register():
    from flask_login import current_user as cu
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        phone   = request.form.get('phone', '').strip()
        country = request.form.get('country', '').strip()

        if not name or not email:
            flash('Please fill agency name and email.', 'error')
            return render_template('b2b/register.html')

        if cu.is_authenticated:
            user = cu
        else:
            user = User.query.filter_by(email=email).first()
            if not user:
                import random, string
                pwd = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                user = User(email=email, phone=phone)
                user.set_password(pwd)
                db.session.add(user)
                db.session.flush()

        if Agency.query.filter_by(owner_id=user.id).first():
            flash('This email is already registered as a partner.', 'error')
            return render_template('b2b/register.html')

        agency = Agency(owner_id=user.id, name=name, country=country, phone=phone, email=email)
        db.session.add(agency)
        user.role = 'agent'
        db.session.commit()

        if not cu.is_authenticated:
            login_user(user)

        flash('B2B application submitted! We will activate your account within 24 hours.', 'success')
        return redirect(url_for('b2b.dashboard'))
    return render_template('b2b/register.html')


@b2b_bp.before_request
def check_auth_except_register():
    if request.endpoint == 'b2b.register':
        return
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login', next=request.path))


# ═══════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════
@b2b_bp.route('/')
def dashboard():
    agency = get_agency_or_redirect()
    if not agency:
        return redirect(url_for('b2b.register'))

    today = datetime.utcnow().date()
    month_start = today.replace(day=1)

    today_bookings = agency.bookings.filter(Booking.created_at >= datetime.combine(today, datetime.min.time())).count()
    month_revenue = db.session.query(func.coalesce(func.sum(Booking.total_price), 0)).filter(
        Booking.agency_id == agency.id, Booking.created_at >= month_start
    ).scalar()

    stats = {
        'today_bookings': today_bookings,
        'month_revenue': float(month_revenue or 0),
        'active_tours': agency.tours.filter_by(status='published').count(),
        'active_properties': agency.properties.filter_by(status='published').count(),
        'new_requests': agency.bookings.filter_by(status='new').count(),
        'open_tickets': agency.tickets.filter_by(status='open').count(),
        'total_customers': agency.customers.count(),
    }

    upcoming_checkins = agency.bookings.filter(
        Booking.check_in >= today, Booking.check_in <= today + timedelta(days=7), Booking.status == 'confirmed'
    ).order_by(Booking.check_in.asc()).limit(5).all()

    upcoming_checkouts = agency.bookings.filter(
        Booking.check_out >= today, Booking.check_out <= today + timedelta(days=7), Booking.status == 'confirmed'
    ).order_by(Booking.check_out.asc()).limit(5).all()

    recent_bookings = agency.bookings.order_by(Booking.created_at.desc()).limit(8).all()
    announcements = Announcement.query.filter_by(is_active=True).order_by(Announcement.created_at.desc()).limit(3).all()

    # Simple 6-month revenue chart data
    chart_labels, chart_data = [], []
    for i in range(5, -1, -1):
        m = (today.replace(day=1) - timedelta(days=i*30))
        label = m.strftime('%b')
        rev = db.session.query(func.coalesce(func.sum(Booking.total_price), 0)).filter(
            Booking.agency_id == agency.id,
            func.extract('month', Booking.created_at) == m.month,
            func.extract('year', Booking.created_at) == m.year
        ).scalar()
        chart_labels.append(label)
        chart_data.append(float(rev or 0))

    return render_template('b2b/dashboard.html', agency=agency, stats=stats,
                            upcoming_checkins=upcoming_checkins, upcoming_checkouts=upcoming_checkouts,
                            recent_bookings=recent_bookings, announcements=announcements,
                            chart_labels=chart_labels, chart_data=chart_data)


# ═══════════════════════════════════════════════
# PROPERTY MANAGEMENT
# ═══════════════════════════════════════════════
@b2b_bp.route('/properties')
def properties():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    props = agency.properties.order_by(Property.created_at.desc()).all()
    return render_template('b2b/properties.html', agency=agency, properties=props)


@b2b_bp.route('/properties/new/type')
def property_type_select():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    groups = {'stay': [], 'outdoor': [], 'venue': [], 'service': []}
    for t in PROPERTY_TYPES:
        groups[t['group']].append(t)
    return render_template('b2b/property_type_select.html', agency=agency, groups=groups)


@b2b_bp.route('/properties/new', methods=['GET', 'POST'])
def property_new():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    if request.method == 'POST':
        p = Property(
            agency_id=agency.id,
            name=request.form.get('name'),
            category=request.form.get('category', 'hotel'),
            description=request.form.get('description'),
            address=request.form.get('address'),
            city=request.form.get('city'),
            check_in_time=request.form.get('check_in_time', '14:00'),
            check_out_time=request.form.get('check_out_time', '12:00'),
            cancellation_policy=request.form.get('cancellation_policy'),
            languages_spoken=request.form.get('languages_spoken'),
            nearby_attractions=request.form.get('nearby_attractions'),
            has_parking='has_parking' in request.form,
            has_restaurant='has_restaurant' in request.form,
            has_pool='has_pool' in request.form,
            has_spa='has_spa' in request.form,
            has_gym='has_gym' in request.form,
            has_wifi='has_wifi' in request.form,
            has_airport_transfer='has_airport_transfer' in request.form,
            has_breakfast='has_breakfast' in request.form,
            seo_title=request.form.get('seo_title'),
            seo_description=request.form.get('seo_description'),
            status='draft',
            cover_image='/photo/' + (request.form.get('city') or 'samarkand').lower() + '?w=800&h=600',
        )
        db.session.add(p)
        db.session.commit()
        flash('Property created as draft. Add rooms and publish when ready.', 'success')
        return redirect(url_for('b2b.property_edit', id=p.id))
    return render_template('b2b/property_form.html', agency=agency, property=None)


@b2b_bp.route('/properties/<int:id>/edit', methods=['GET', 'POST'])
def property_edit(id):
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    p = Property.query.filter_by(id=id, agency_id=agency.id).first_or_404()
    if request.method == 'POST':
        p.name = request.form.get('name')
        p.category = request.form.get('category', p.category)
        p.description = request.form.get('description')
        p.address = request.form.get('address')
        p.city = request.form.get('city')
        p.check_in_time = request.form.get('check_in_time', p.check_in_time)
        p.check_out_time = request.form.get('check_out_time', p.check_out_time)
        p.cancellation_policy = request.form.get('cancellation_policy')
        p.languages_spoken = request.form.get('languages_spoken')
        p.nearby_attractions = request.form.get('nearby_attractions')
        p.has_parking = 'has_parking' in request.form
        p.has_restaurant = 'has_restaurant' in request.form
        p.has_pool = 'has_pool' in request.form
        p.has_spa = 'has_spa' in request.form
        p.has_gym = 'has_gym' in request.form
        p.has_wifi = 'has_wifi' in request.form
        p.has_airport_transfer = 'has_airport_transfer' in request.form
        p.has_breakfast = 'has_breakfast' in request.form
        p.seo_title = request.form.get('seo_title')
        p.seo_description = request.form.get('seo_description')
        p.video_url = request.form.get('video_url')
        p.tour_360_url = request.form.get('tour_360_url')
        p.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Property updated.', 'success')
        return redirect(url_for('b2b.property_edit', id=p.id))
    rooms = p.rooms.all()
    return render_template('b2b/property_form.html', agency=agency, property=p, rooms=rooms)


@b2b_bp.route('/properties/<int:id>/publish', methods=['POST'])
def property_publish(id):
    agency = get_agency_or_redirect()
    p = Property.query.filter_by(id=id, agency_id=agency.id).first_or_404()
    p.status = 'published' if p.status == 'draft' else 'draft'
    db.session.commit()
    flash(f'Property {"published" if p.status=="published" else "set to draft"}.', 'success')
    return redirect(url_for('b2b.properties'))


@b2b_bp.route('/properties/<int:id>/delete', methods=['POST'])
def property_delete(id):
    agency = get_agency_or_redirect()
    p = Property.query.filter_by(id=id, agency_id=agency.id).first_or_404()
    db.session.delete(p)
    db.session.commit()
    flash('Property deleted.', 'success')
    return redirect(url_for('b2b.properties'))


@b2b_bp.route('/properties/<int:id>/rooms/new', methods=['POST'])
def room_new(id):
    agency = get_agency_or_redirect()
    p = Property.query.filter_by(id=id, agency_id=agency.id).first_or_404()
    r = Room(
        property_id=p.id,
        name=request.form.get('name'),
        max_guests=int(request.form.get('max_guests', 2) or 2),
        bed_type=request.form.get('bed_type'),
        size_sqm=float(request.form.get('size_sqm') or 0) or None,
        base_price=float(request.form.get('base_price') or 0) or None,
        weekend_price=float(request.form.get('weekend_price') or 0) or None,
        total_rooms=int(request.form.get('total_rooms', 1) or 1),
        instant_booking='instant_booking' in request.form,
    )
    db.session.add(r)
    db.session.commit()
    flash('Room added.', 'success')
    return redirect(url_for('b2b.property_edit', id=p.id))


@b2b_bp.route('/rooms/<int:id>/delete', methods=['POST'])
def room_delete(id):
    agency = get_agency_or_redirect()
    r = Room.query.get_or_404(id)
    if r.property.agency_id != agency.id:
        return redirect(url_for('b2b.dashboard'))
    pid = r.property_id
    db.session.delete(r)
    db.session.commit()
    return redirect(url_for('b2b.property_edit', id=pid))


# ═══════════════════════════════════════════════
# TOUR MANAGEMENT
# ═══════════════════════════════════════════════
@b2b_bp.route('/tours')
def tours():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    tour_list = agency.tours.order_by(Tour.created_at.desc()).all()
    return render_template('b2b/tours.html', agency=agency, tours=tour_list)


@b2b_bp.route('/tours/new', methods=['GET', 'POST'])
def tour_new():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    if request.method == 'POST':
        t = Tour(
            agency_id=agency.id,
            title=request.form.get('title'),
            category=request.form.get('category', 'private'),
            description=request.form.get('description'),
            duration_days=int(request.form.get('duration_days', 1) or 1),
            destinations=request.form.get('destinations'),
            hotels_included=request.form.get('hotels_included'),
            meals_included=request.form.get('meals_included'),
            transportation=request.form.get('transportation'),
            guide_languages=request.form.get('guide_languages'),
            price_per_person=float(request.form.get('price_per_person') or 0) or None,
            discount_percent=float(request.form.get('discount_percent') or 0),
            min_travelers=int(request.form.get('min_travelers', 1) or 1),
            max_travelers=int(request.form.get('max_travelers', 20) or 20),
            meeting_point=request.form.get('meeting_point'),
            included_services=request.form.get('included_services'),
            excluded_services=request.form.get('excluded_services'),
            cancellation_rules=request.form.get('cancellation_rules'),
            status='draft',
            cover_image='/photo/samarkand?w=800&h=600',
        )
        db.session.add(t)
        db.session.commit()
        flash('Tour created as draft.', 'success')
        return redirect(url_for('b2b.tour_edit', id=t.id))
    return render_template('b2b/tour_form.html', agency=agency, tour=None)


@b2b_bp.route('/tours/<int:id>/edit', methods=['GET', 'POST'])
def tour_edit(id):
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    t = Tour.query.filter_by(id=id, agency_id=agency.id).first_or_404()
    if request.method == 'POST':
        t.title = request.form.get('title')
        t.category = request.form.get('category', t.category)
        t.description = request.form.get('description')
        t.duration_days = int(request.form.get('duration_days', 1) or 1)
        t.destinations = request.form.get('destinations')
        t.hotels_included = request.form.get('hotels_included')
        t.meals_included = request.form.get('meals_included')
        t.transportation = request.form.get('transportation')
        t.guide_languages = request.form.get('guide_languages')
        t.price_per_person = float(request.form.get('price_per_person') or 0) or None
        t.discount_percent = float(request.form.get('discount_percent') or 0)
        t.min_travelers = int(request.form.get('min_travelers', 1) or 1)
        t.max_travelers = int(request.form.get('max_travelers', 20) or 20)
        t.meeting_point = request.form.get('meeting_point')
        t.included_services = request.form.get('included_services')
        t.excluded_services = request.form.get('excluded_services')
        t.cancellation_rules = request.form.get('cancellation_rules')
        t.video_url = request.form.get('video_url')
        t.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Tour updated.', 'success')
        return redirect(url_for('b2b.tour_edit', id=t.id))
    itinerary = []
    if t.itinerary:
        try: itinerary = json.loads(t.itinerary)
        except: itinerary = []
    return render_template('b2b/tour_form.html', agency=agency, tour=t, itinerary=itinerary)


@b2b_bp.route('/tours/<int:id>/itinerary', methods=['POST'])
def tour_itinerary_save(id):
    agency = get_agency_or_redirect()
    t = Tour.query.filter_by(id=id, agency_id=agency.id).first_or_404()
    days = request.form.getlist('day_title[]')
    descs = request.form.getlist('day_desc[]')
    itinerary = [{'day': i+1, 'title': d, 'desc': descs[i] if i < len(descs) else ''} for i, d in enumerate(days)]
    t.itinerary = json.dumps(itinerary)
    db.session.commit()
    flash('Itinerary saved.', 'success')
    return redirect(url_for('b2b.tour_edit', id=t.id))


@b2b_bp.route('/tours/<int:id>/publish', methods=['POST'])
def tour_publish(id):
    agency = get_agency_or_redirect()
    t = Tour.query.filter_by(id=id, agency_id=agency.id).first_or_404()
    t.status = 'published' if t.status == 'draft' else 'draft'
    db.session.commit()
    flash(f'Tour {"published" if t.status=="published" else "set to draft"}.', 'success')
    return redirect(url_for('b2b.tours'))


@b2b_bp.route('/tours/<int:id>/delete', methods=['POST'])
def tour_delete(id):
    agency = get_agency_or_redirect()
    t = Tour.query.filter_by(id=id, agency_id=agency.id).first_or_404()
    db.session.delete(t)
    db.session.commit()
    flash('Tour deleted.', 'success')
    return redirect(url_for('b2b.tours'))


# ═══════════════════════════════════════════════
# MEDIA CENTER
# ═══════════════════════════════════════════════
@b2b_bp.route('/media')
def media():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    folder = request.args.get('folder', '')
    q = agency.media_assets
    if folder:
        q = q.filter_by(folder=folder)
    assets = q.order_by(MediaAsset.uploaded_at.desc()).all()
    folders = db.session.query(MediaAsset.folder).filter_by(agency_id=agency.id).distinct().all()
    folders = [f[0] for f in folders] or ['General']
    return render_template('b2b/media.html', agency=agency, assets=assets, folders=folders, current_folder=folder)


@b2b_bp.route('/media/upload', methods=['POST'])
def media_upload():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))

    file = request.files.get('file')
    file_type = request.form.get('file_type', 'image')
    folder_name = request.form.get('folder', 'General')

    if file and file.filename:
        from app.utils.imagekit import upload_file
        import os
        filename = file.filename
        # Upload to ImageKit under /bektour/<agency_id>/
        ik_folder = f'/bektour/{agency.id}/{folder_name.lower()}'
        url, file_id = upload_file(file, filename, folder=ik_folder)

        if url:
            size_kb = 0
            try:
                file.seek(0, 2)
                size_kb = file.tell() // 1024
            except Exception:
                pass

            asset = MediaAsset(
                agency_id=agency.id,
                filename=filename,
                file_url=url,
                file_type=file_type,
                folder=folder_name,
                file_size_kb=size_kb
            )
            db.session.add(asset)
            db.session.commit()
            flash('✅ File uploaded successfully!', 'success')
        else:
            flash('❌ Upload failed. Check ImageKit settings.', 'error')
    else:
        flash('No file selected.', 'error')

    return redirect(url_for('b2b.media'))


@b2b_bp.route('/media/<int:id>/delete', methods=['POST'])
def media_delete(id):
    agency = get_agency_or_redirect()
    a = MediaAsset.query.filter_by(id=id, agency_id=agency.id).first_or_404()
    db.session.delete(a)
    db.session.commit()
    return redirect(url_for('b2b.media'))


# ═══════════════════════════════════════════════
# BOOKINGS MANAGEMENT
# ═══════════════════════════════════════════════
@b2b_bp.route('/bookings')
def bookings():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    status = request.args.get('status', '')
    view = request.args.get('view', 'list')
    q = agency.bookings
    if status:
        q = q.filter_by(status=status)
    booking_list = q.order_by(Booking.created_at.desc()).all()
    counts = {
        'all': agency.bookings.count(),
        'new': agency.bookings.filter_by(status='new').count(),
        'confirmed': agency.bookings.filter_by(status='confirmed').count(),
        'cancelled': agency.bookings.filter_by(status='cancelled').count(),
        'completed': agency.bookings.filter(Booking.check_out < datetime.utcnow().date()).count(),
    }
    return render_template('b2b/bookings.html', agency=agency, bookings=booking_list,
                            counts=counts, current_status=status, view=view)


@b2b_bp.route('/bookings/<int:id>/status', methods=['POST'])
def booking_status(id):
    agency = get_agency_or_redirect()
    b = Booking.query.filter_by(id=id, agency_id=agency.id).first_or_404()
    b.status = request.form.get('status', b.status)
    db.session.commit()
    flash('Booking status updated.', 'success')
    return redirect(url_for('b2b.bookings'))


# ═══════════════════════════════════════════════
# CUSTOMER MANAGEMENT (CRM)
# ═══════════════════════════════════════════════
@b2b_bp.route('/customers')
def customers():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    q = request.args.get('q', '')
    query = agency.customers
    if q:
        query = query.filter(PartnerCustomer.full_name.ilike(f'%{q}%'))
    customer_list = query.order_by(PartnerCustomer.created_at.desc()).all()
    return render_template('b2b/customers.html', agency=agency, customers=customer_list, q=q)


@b2b_bp.route('/customers/new', methods=['POST'])
def customer_new():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    c = PartnerCustomer(
        agency_id=agency.id,
        full_name=request.form.get('full_name'),
        email=request.form.get('email'),
        phone=request.form.get('phone'),
        nationality=request.form.get('nationality'),
        passport_number=request.form.get('passport_number'),
        notes=request.form.get('notes'),
    )
    db.session.add(c)
    db.session.commit()
    flash('Customer added.', 'success')
    return redirect(url_for('b2b.customers'))


@b2b_bp.route('/customers/<int:id>/delete', methods=['POST'])
def customer_delete(id):
    agency = get_agency_or_redirect()
    c = PartnerCustomer.query.filter_by(id=id, agency_id=agency.id).first_or_404()
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('b2b.customers'))


# ═══════════════════════════════════════════════
# REPORTS
# ═══════════════════════════════════════════════
@b2b_bp.route('/reports')
def reports():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))

    today = datetime.utcnow().date()
    total_revenue = db.session.query(func.coalesce(func.sum(Booking.total_price), 0)).filter_by(agency_id=agency.id).scalar()
    total_bookings = agency.bookings.count()
    confirmed = agency.bookings.filter_by(status='confirmed').count()
    conversion = round((confirmed / total_bookings * 100), 1) if total_bookings else 0

    top_properties = (db.session.query(Villa.title_en, func.count(Booking.id).label('cnt'))
                       .join(Booking, Booking.villa_id == Villa.id)
                       .filter(Booking.agency_id == agency.id)
                       .group_by(Villa.title_en).order_by(func.count(Booking.id).desc()).limit(5).all())

    monthly_labels, monthly_revenue, monthly_bookings = [], [], []
    for i in range(11, -1, -1):
        m = (today.replace(day=1) - timedelta(days=i*30))
        monthly_labels.append(m.strftime('%b %y'))
        rev = db.session.query(func.coalesce(func.sum(Booking.total_price), 0)).filter(
            Booking.agency_id == agency.id,
            func.extract('month', Booking.created_at) == m.month,
            func.extract('year', Booking.created_at) == m.year
        ).scalar()
        cnt = agency.bookings.filter(
            func.extract('month', Booking.created_at) == m.month,
            func.extract('year', Booking.created_at) == m.year
        ).count()
        monthly_revenue.append(float(rev or 0))
        monthly_bookings.append(cnt)

    return render_template('b2b/reports.html', agency=agency,
                            total_revenue=float(total_revenue or 0), total_bookings=total_bookings,
                            conversion=conversion, top_properties=top_properties,
                            monthly_labels=monthly_labels, monthly_revenue=monthly_revenue,
                            monthly_bookings=monthly_bookings)


# ═══════════════════════════════════════════════
# SUPPORT / COMMUNICATION
# ═══════════════════════════════════════════════
@b2b_bp.route('/support')
def support():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    tickets = agency.tickets.order_by(SupportTicket.created_at.desc()).all()
    return render_template('b2b/support.html', agency=agency, tickets=tickets)


@b2b_bp.route('/support/new', methods=['POST'])
def support_new():
    agency = get_agency_or_redirect()
    if not agency: return redirect(url_for('b2b.register'))
    t = SupportTicket(
        agency_id=agency.id,
        subject=request.form.get('subject'),
        message=request.form.get('message'),
        priority=request.form.get('priority', 'normal'),
    )
    db.session.add(t)
    db.session.commit()
    flash('Support ticket submitted. We will respond within 4 hours.', 'success')
    return redirect(url_for('b2b.support'))


# ═══════════════════════════════════════════════
# QUICK SEARCH (Command palette API)
# ═══════════════════════════════════════════════
@b2b_bp.route('/api/search')
def api_search():
    agency = get_agency_or_redirect()
    if not agency: return jsonify([])
    q = request.args.get('q', '').strip()
    if not q or len(q) < 2:
        return jsonify([])
    results = []
    for p in agency.properties.filter(Property.name.ilike(f'%{q}%')).limit(5):
        results.append({'type': 'Property', 'label': p.name, 'url': url_for('b2b.property_edit', id=p.id)})
    for t in agency.tours.filter(Tour.title.ilike(f'%{q}%')).limit(5):
        results.append({'type': 'Tour', 'label': t.title, 'url': url_for('b2b.tour_edit', id=t.id)})
    for c in agency.customers.filter(PartnerCustomer.full_name.ilike(f'%{q}%')).limit(5):
        results.append({'type': 'Customer', 'label': c.full_name, 'url': url_for('b2b.customers')})
    return jsonify(results)


@b2b_bp.route('/upload/image', methods=['POST'])
def upload_image():
    """Generic image upload endpoint - returns JSON with URL."""
    agency = get_agency_or_redirect()
    if not agency:
        return jsonify({'error': 'Unauthorized'}), 401

    file = request.files.get('file')
    if not file or not file.filename:
        return jsonify({'error': 'No file provided'}), 400

    from app.utils.imagekit import upload_file
    folder = request.form.get('folder', f'/bektour/{agency.id}')
    url, file_id = upload_file(file, file.filename, folder=folder)

    if url:
        return jsonify({'url': url, 'file_id': file_id, 'success': True})
    else:
        return jsonify({'error': 'Upload failed'}), 500
