"""
BekTour Photo Generator — Premium SVG city illustrations
Each city gets a unique architectural illustration
"""
from flask import Blueprint, Response, request

photos_bp = Blueprint('photos', __name__)

def make_city_svg(city, w=800, h=600):
    city = city.lower().replace('-valley','').replace('-','').strip()

    configs = {
        'samarkand': {
            'sky1': '#0a1f3d', 'sky2': '#1a3a6b', 'ground': '#c8a45d',
            'accent': '#e8c87d', 'arch': '#f0d080',
            'label': 'SAMARKAND', 'sublabel': 'REGISTAN SQUARE · UNESCO',
            'shape': 'registan'
        },
        'bukhara': {
            'sky1': '#1a0a30', 'sky2': '#3d1a5a', 'ground': '#8b4a8b',
            'accent': '#c87dc8', 'arch': '#e8a0e8',
            'label': 'BUKHARA', 'sublabel': 'KALON MINARET · 2500 YEARS',
            'shape': 'minaret'
        },
        'khiva': {
            'sky1': '#0d1a10', 'sky2': '#1a3d20', 'ground': '#c87a2a',
            'accent': '#e8a040', 'arch': '#f0c060',
            'label': 'KHIVA', 'sublabel': 'ICHAN KALA · WALLED CITY',
            'shape': 'fortress'
        },
        'tashkent': {
            'sky1': '#0a0d1a', 'sky2': '#1a2040', 'ground': '#2a8a4a',
            'accent': '#40c070', 'arch': '#60e090',
            'label': 'TASHKENT', 'sublabel': 'CAPITAL CITY · AMIRSAY',
            'shape': 'modern'
        },
        'fergana': {
            'sky1': '#200a05', 'sky2': '#4a1a0a', 'ground': '#c84a1a',
            'accent': '#e87040', 'arch': '#f09060',
            'label': 'FERGANA', 'sublabel': 'SILK ROAD · CRAFTSMANSHIP',
            'shape': 'market'
        },
        'shahrisabz': {
            'sky1': '#0a200a', 'sky2': '#1a4020', 'ground': '#6a9a2a',
            'accent': '#90c040', 'arch': '#b0e060',
            'label': 'SHAHRISABZ', 'sublabel': "TIMUR'S BIRTHPLACE · UNESCO",
            'shape': 'palace'
        },
        'nukus': {
            'sky1': '#051520', 'sky2': '#0a2a3a', 'ground': '#2a7a8a',
            'accent': '#40a8b8', 'arch': '#60c8d8',
            'label': 'NUKUS', 'sublabel': 'ARAL SEA · ART MUSEUM',
            'shape': 'desert'
        },
        'termez': {
            'sky1': '#200d05', 'sky2': '#4a1f0a', 'ground': '#d4603a',
            'accent': '#e88060', 'arch': '#f0a080',
            'label': 'TERMEZ', 'sublabel': 'BUDDHIST HERITAGE · ANCIENT',
            'shape': 'temple'
        },
    }

    c = configs.get(city, {
        'sky1': '#061826', 'sky2': '#0d2640', 'ground': '#c8a45d',
        'accent': '#e8c87d', 'arch': '#f0d090',
        'label': city.upper(), 'sublabel': 'UZBEKISTAN · SILK ROAD',
        'shape': 'registan'
    })

    s1, s2 = c['sky1'], c['sky2']
    gr = c['ground']
    ac = c['accent']
    ar = c['arch']
    lbl = c['label']
    sub = c['sublabel']
    cx = w // 2
    cy = h // 2

    # Base gradient sky
    sky = f'''
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{s1}"/>
      <stop offset="100%" stop-color="{s2}"/>
    </linearGradient>
    <linearGradient id="glo" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="transparent"/>
      <stop offset="70%" stop-color="{s1}" stop-opacity="0"/>
      <stop offset="100%" stop-color="{s1}" stop-opacity="0.9"/>
    </linearGradient>
    <radialGradient id="moon" cx="75%" cy="18%" r="8%">
      <stop offset="0%" stop-color="{ac}" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="transparent"/>
    </radialGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#sky)"/>
  <rect width="{w}" height="{h}" fill="url(#moon)"/>'''

    # Stars
    import random
    random.seed(hash(city) % 1000)
    stars = ''
    for _ in range(30):
        sx = random.randint(20, w-20)
        sy = random.randint(10, h//3)
        sr = random.uniform(0.5, 1.5)
        stars += f'<circle cx="{sx}" cy="{sy}" r="{sr}" fill="white" opacity="{random.uniform(0.3,0.9):.1f}"/>'

    # Islamic geometric pattern (subtle background)
    pattern = f'''
  <pattern id="pat" x="0" y="0" width="80" height="80" patternUnits="userSpaceOnUse">
    <polygon points="40,5 55,20 75,20 60,35 65,55 40,45 15,55 20,35 5,20 25,20" 
             fill="none" stroke="{ac}" stroke-width="0.4" opacity="0.06"/>
    <circle cx="40" cy="40" r="12" fill="none" stroke="{ac}" stroke-width="0.3" opacity="0.04"/>
  </pattern>
  <rect width="{w}" height="{h}" fill="url(#pat)"/>'''

    # Architecture based on shape
    if c['shape'] == 'registan':
        arch = f'''
  <!-- Ground -->
  <rect x="0" y="{int(h*0.72)}" width="{w}" height="{int(h*0.28)}" fill="{gr}" opacity="0.15"/>
  <!-- Main portal -->
  <rect x="{cx-90}" y="{int(h*0.28)}" width="180" height="{int(h*0.45)}" fill="{s2}" rx="2"/>
  <path d="M{cx-90} {int(h*0.28)} Q{cx} {int(h*0.10)} {cx+90} {int(h*0.28)}" fill="{ar}" opacity="0.9"/>
  <rect x="{cx-60}" y="{int(h*0.38)}" width="120" height="{int(h*0.35)}" fill="{s1}" rx="2"/>
  <path d="M{cx-60} {int(h*0.38)} Q{cx} {int(h*0.25)} {cx+60} {int(h*0.38)}" fill="{ac}" opacity="0.8"/>
  <!-- Minarets -->
  <rect x="{cx-160}" y="{int(h*0.35)}" width="28" height="{int(h*0.38)}" fill="{ar}" opacity="0.85" rx="2"/>
  <circle cx="{cx-146}" cy="{int(h*0.33)}" r="16" fill="{ac}" opacity="0.9"/>
  <rect x="{cx-151}" y="{int(h*0.20)}" width="10" height="{int(h*0.14)}" fill="{ar}" rx="1"/>
  <rect x="{cx+132}" y="{int(h*0.35)}" width="28" height="{int(h*0.38)}" fill="{ar}" opacity="0.85" rx="2"/>
  <circle cx="{cx+146}" cy="{int(h*0.33)}" r="16" fill="{ac}" opacity="0.9"/>
  <rect x="{cx+141}" y="{int(h*0.20)}" width="10" height="{int(h*0.14)}" fill="{ar}" rx="1"/>
  <!-- Side portals -->
  <rect x="{cx-180}" y="{int(h*0.38)}" width="26" height="{int(h*0.35)}" fill="{s2}" rx="1" opacity="0.8"/>
  <path d="M{cx-180} {int(h*0.38)} Q{cx-167} {int(h*0.30)} {cx-154} {int(h*0.38)}" fill="{ac}" opacity="0.7"/>
  <rect x="{cx+154}" y="{int(h*0.38)}" width="26" height="{int(h*0.35)}" fill="{s2}" rx="1" opacity="0.8"/>
  <path d="M{cx+154} {int(h*0.38)} Q{cx+167} {int(h*0.30)} {cx+180} {int(h*0.38)}" fill="{ac}" opacity="0.7"/>
  <!-- Dome top -->
  <ellipse cx="{cx}" cy="{int(h*0.16)}" rx="44" ry="30" fill="{ac}" opacity="0.9"/>
  <ellipse cx="{cx}" cy="{int(h*0.15)}" rx="34" ry="22" fill="{ar}"/>
  <!-- Tile patterns -->
  <rect x="{cx-88}" y="{int(h*0.50)}" width="176" height="3" fill="{ac}" opacity="0.3"/>
  <rect x="{cx-88}" y="{int(h*0.56)}" width="176" height="2" fill="{ac}" opacity="0.2"/>
  <!-- Crescent -->
  <circle cx="{cx}" cy="{int(h*0.08)}" r="6" fill="{ac}" opacity="0.9"/>'''

    elif c['shape'] == 'minaret':
        arch = f'''
  <rect x="0" y="{int(h*0.70)}" width="{w}" height="{int(h*0.30)}" fill="{gr}" opacity="0.12"/>
  <!-- Main minaret tower -->
  <rect x="{cx-22}" y="{int(h*0.15)}" width="44" height="{int(h*0.58)}" fill="{ar}" opacity="0.9" rx="3"/>
  <!-- Bands on minaret -->
  <rect x="{cx-22}" y="{int(h*0.25)}" width="44" height="6" fill="{ac}" opacity="0.5"/>
  <rect x="{cx-22}" y="{int(h*0.38)}" width="44" height="6" fill="{ac}" opacity="0.5"/>
  <rect x="{cx-22}" y="{int(h*0.51)}" width="44" height="6" fill="{ac}" opacity="0.5"/>
  <!-- Minaret cap -->
  <path d="M{cx-22} {int(h*0.15)} L{cx} {int(h*0.05)} L{cx+22} {int(h*0.15)}" fill="{ac}"/>
  <circle cx="{cx}" cy="{int(h*0.05)}" r="5" fill="{ar}"/>
  <!-- Balcony -->
  <rect x="{cx-28}" y="{int(h*0.62)}" width="56" height="8" fill="{ac}" opacity="0.8" rx="2"/>
  <!-- Mosque base -->
  <rect x="{cx-120}" y="{int(h*0.55)}" width="240" height="{int(h*0.18)}" fill="{s2}" opacity="0.8" rx="3"/>
  <!-- Dome -->
  <ellipse cx="{cx-70}" cy="{int(h*0.52)}" rx="40" ry="26" fill="{ac}" opacity="0.7"/>
  <ellipse cx="{cx+70}" cy="{int(h*0.52)}" rx="40" ry="26" fill="{ac}" opacity="0.7"/>
  <!-- Arch entrance -->
  <rect x="{cx-25}" y="{int(h*0.60)}" width="50" height="{int(h*0.14)}" fill="{s1}"/>
  <path d="M{cx-25} {int(h*0.60)} Q{cx} {int(h*0.52)} {cx+25} {int(h*0.60)}" fill="{ac}" opacity="0.8"/>'''

    elif c['shape'] == 'fortress':
        arch = f'''
  <rect x="0" y="{int(h*0.65)}" width="{w}" height="{int(h*0.35)}" fill="{gr}" opacity="0.15"/>
  <!-- Fortress wall -->
  <rect x="{cx-200}" y="{int(h*0.40)}" width="400" height="{int(h*0.32)}" fill="{ar}" opacity="0.8" rx="2"/>
  <!-- Battlements -->
  {' '.join([f'<rect x="{cx-200+i*40}" y="{int(h*0.33)}" width="20" height="{int(h*0.09)}" fill="{ar}" opacity="0.9"/>' for i in range(10)])}
  <!-- Main gate -->
  <rect x="{cx-40}" y="{int(h*0.42)}" width="80" height="{int(h*0.30)}" fill="{s1}" rx="2"/>
  <path d="M{cx-40} {int(h*0.42)} Q{cx} {int(h*0.30)} {cx+40} {int(h*0.42)}" fill="{ac}" opacity="0.9"/>
  <!-- Towers -->
  <rect x="{cx-205}" y="{int(h*0.28)}" width="40" height="{int(h*0.44)}" fill="{ar}" opacity="0.9" rx="2"/>
  <rect x="{cx+165}" y="{int(h*0.28)}" width="40" height="{int(h*0.44)}" fill="{ar}" opacity="0.9" rx="2"/>
  <path d="M{cx-205} {int(h*0.28)} Q{cx-185} {int(h*0.18)} {cx-165} {int(h*0.28)}" fill="{ac}"/>
  <path d="M{cx+165} {int(h*0.28)} Q{cx+185} {int(h*0.18)} {cx+205} {int(h*0.28)}" fill="{ac}"/>
  <!-- Decorative elements -->
  <rect x="{cx-190}" y="{int(h*0.43)}" width="34" height="3" fill="{ac}" opacity="0.4"/>
  <rect x="{cx+156}" y="{int(h*0.43)}" width="34" height="3" fill="{ac}" opacity="0.4"/>'''

    else:  # generic elegant
        arch = f'''
  <rect x="0" y="{int(h*0.70)}" width="{w}" height="{int(h*0.30)}" fill="{gr}" opacity="0.12"/>
  <!-- Central arch -->
  <rect x="{cx-70}" y="{int(h*0.30)}" width="140" height="{int(h*0.42)}" fill="{ar}" opacity="0.85" rx="3"/>
  <path d="M{cx-70} {int(h*0.30)} Q{cx} {int(h*0.12)} {cx+70} {int(h*0.30)}" fill="{ac}" opacity="0.9"/>
  <rect x="{cx-44}" y="{int(h*0.40)}" width="88" height="{int(h*0.32)}" fill="{s1}" rx="2"/>
  <path d="M{cx-44} {int(h*0.40)} Q{cx} {int(h*0.28)} {cx+44} {int(h*0.40)}" fill="{ac}" opacity="0.7"/>
  <!-- Side pillars -->
  <rect x="{cx-140}" y="{int(h*0.38)}" width="24" height="{int(h*0.34)}" fill="{ar}" opacity="0.7" rx="2"/>
  <rect x="{cx+116}" y="{int(h*0.38)}" width="24" height="{int(h*0.34)}" fill="{ar}" opacity="0.7" rx="2"/>
  <!-- Dome -->
  <ellipse cx="{cx}" cy="{int(h*0.18)}" rx="50" ry="32" fill="{ac}" opacity="0.85"/>
  <ellipse cx="{cx}" cy="{int(h*0.17)}" rx="38" ry="24" fill="{ar}"/>
  <!-- Crescent on top -->
  <circle cx="{cx}" cy="{int(h*0.08)}" r="7" fill="{ac}"/>'''

    # Bottom gradient overlay + text
    overlay = f'''
  <!-- Bottom overlay -->
  <rect width="{w}" height="{h}" fill="url(#glo)"/>
  <!-- City name -->
  <text x="{cx}" y="{h-56}" text-anchor="middle" 
        font-family="Georgia, \'Times New Roman\', serif" 
        font-size="{int(w*0.055)}" font-weight="600" fill="white" 
        opacity="0.96" letter-spacing="4">{lbl}</text>
  <!-- Decorative line -->
  <line x1="{cx-60}" y1="{h-42}" x2="{cx+60}" y2="{h-42}" 
        stroke="{ac}" stroke-width="1" opacity="0.6"/>
  <circle cx="{cx}" cy="{h-42}" r="3" fill="{ac}" opacity="0.8"/>
  <!-- Subtitle -->
  <text x="{cx}" y="{h-24}" text-anchor="middle" 
        font-family="Arial, sans-serif" font-size="{int(w*0.014)}" 
        fill="{ac}" letter-spacing="5" font-weight="500">{sub}</text>'''

    full_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  {sky}
  {stars}
  {pattern}
  {arch}
  {overlay}
</svg>'''
    return full_svg


@photos_bp.route('/photo/<city>')
def city_photo(city):
    w = min(int(request.args.get('w', 800)), 1920)
    h = min(int(request.args.get('h', 600)), 1080)
    svg = make_city_svg(city, w, h)
    return Response(svg, mimetype='image/svg+xml',
                    headers={
                        'Cache-Control': 'public, max-age=604800',
                        'X-Content-Type-Options': 'nosniff'
                    })
