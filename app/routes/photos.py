"""
BekTour — Premium SVG City Art
Each city gets a unique, detailed architectural illustration
Based on real Uzbekistan landmarks
"""
from flask import Blueprint, Response, request

photos_bp = Blueprint('photos', __name__)

def svg_samarkand(w, h):
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0a1628"/><stop offset="40%" stop-color="#1a3058"/><stop offset="100%" stop-color="#2a4878"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#f0d080"/><stop offset="100%" stop-color="#c8901a"/>
    </linearGradient>
    <linearGradient id="tile" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#2060a0"/><stop offset="100%" stop-color="#1040780"/>
    </linearGradient>
    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#c8a45d"/><stop offset="100%" stop-color="#8a6030"/>
    </linearGradient>
    <linearGradient id="fade" x1="0" y1="0.5" x2="0" y2="1">
      <stop offset="0%" stop-color="#0a1628" stop-opacity="0"/><stop offset="100%" stop-color="#0a1628" stop-opacity="0.88"/>
    </linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <!-- Sky -->
  <rect width="{w}" height="{h}" fill="url(#sky)"/>
  <!-- Stars -->
  {''.join([f'<circle cx="{int(w*(i*37%100)/100)}" cy="{int(h*0.4*(i*53%100)/100)}" r="{0.8+i%2*0.6:.1f}" fill="white" opacity="{0.3+i%5*0.12:.2f}"/>' for i in range(40)])}
  <!-- Moon glow -->
  <radialGradient id="moon" cx="75%" cy="12%" r="12%"><stop offset="0%" stop-color="#ffe080" stop-opacity="0.5"/><stop offset="100%" stop-color="transparent"/></radialGradient>
  <rect width="{w}" height="{h}" fill="url(#moon)"/>
  <circle cx="{int(w*0.78)}" cy="{int(h*0.1)}" r="{int(w*0.025)}" fill="#ffe080" opacity="0.7" filter="url(#glow)"/>
  <!-- Ground -->
  <rect x="0" y="{int(h*0.72)}" width="{w}" height="{int(h*0.28)}" fill="url(#ground)" opacity="0.25"/>
  <!-- Registan - Left Madrasa (Ulugbek) -->
  <!-- Portal arch -->
  <rect x="{cx-210}" y="{int(h*0.25)}" width="120" height="{int(h*0.5)}" fill="#1e3d6e" rx="2"/>
  <path d="M{cx-210} {int(h*0.25)} Q{cx-150} {int(h*0.06)} {cx-90} {int(h*0.25)}" fill="url(#gold)" opacity="0.9"/>
  <!-- Tile decoration on arch -->
  <path d="M{cx-200} {int(h*0.27)} Q{cx-150} {int(h*0.10)} {cx-100} {int(h*0.27)}" fill="none" stroke="#4090d0" stroke-width="3" opacity="0.6"/>
  <!-- Minaret L1 -->
  <rect x="{cx-240}" y="{int(h*0.30)}" width="24" height="{int(h*0.44)}" fill="url(#gold)" rx="3"/>
  <circle cx="{cx-228}" cy="{int(h*0.28)}" r="14" fill="url(#gold)"/>
  <rect x="{cx-232}" y="{int(h*0.14)}" width="8" height="{int(h*0.15)}" fill="url(#gold)" rx="2"/>
  <circle cx="{cx-228}" cy="{int(h*0.13)}" r="5" fill="#ffe080"/>
  <!-- Registan - Center Madrasa (Tilya-Kori) -->
  <rect x="{cx-70}" y="{int(h*0.18)}" width="140" height="{int(h*0.57)}" fill="#1e3d6e" rx="2"/>
  <path d="M{cx-70} {int(h*0.18)} Q{cx} {int(h*-0.02)} {cx+70} {int(h*0.18)}" fill="url(#gold)"/>
  <rect x="{cx-44}" y="{int(h*0.30)}" width="88" height="{int(h*0.45)}" fill="#0a1628" rx="2"/>
  <path d="M{cx-44} {int(h*0.30)} Q{cx} {int(h*0.18)} {cx+44} {int(h*0.30)}" fill="#3070b0" opacity="0.8"/>
  <!-- Central dome -->
  <ellipse cx="{cx}" cy="{int(h*0.13)}" rx="42" ry="28" fill="#3070b0"/>
  <ellipse cx="{cx}" cy="{int(h*0.12)}" rx="32" ry="20" fill="#4090d0"/>
  <ellipse cx="{cx}" cy="{int(h*0.11)}" rx="18" ry="10" fill="url(#gold)"/>
  <rect x="{cx-3}" y="{int(h*0.03)}" width="6" height="{int(h*0.09)}" fill="url(#gold)" rx="1"/>
  <circle cx="{cx}" cy="{int(h*0.02)}" r="5" fill="#ffe080" filter="url(#glow)"/>
  <!-- Tile work -->
  <rect x="{cx-68}" y="{int(h*0.19)}" width="136" height="6" fill="#4090d0" opacity="0.5"/>
  <rect x="{cx-68}" y="{int(h*0.24)}" width="136" height="3" fill="url(#gold)" opacity="0.4"/>
  <!-- Registan - Right Madrasa (Sher-Dor) -->
  <rect x="{cx+90}" y="{int(h*0.25)}" width="120" height="{int(h*0.5)}" fill="#1e3d6e" rx="2"/>
  <path d="M{cx+90} {int(h*0.25)} Q{cx+150} {int(h*0.06)} {cx+210} {int(h*0.25)}" fill="url(#gold)" opacity="0.9"/>
  <path d="M{cx+100} {int(h*0.27)} Q{cx+150} {int(h*0.10)} {cx+200} {int(h*0.27)}" fill="none" stroke="#4090d0" stroke-width="3" opacity="0.6"/>
  <!-- Minaret R1 -->
  <rect x="{cx+216}" y="{int(h*0.30)}" width="24" height="{int(h*0.44)}" fill="url(#gold)" rx="3"/>
  <circle cx="{cx+228}" cy="{int(h*0.28)}" r="14" fill="url(#gold)"/>
  <rect x="{cx+224}" y="{int(h*0.14)}" width="8" height="{int(h*0.15)}" fill="url(#gold)" rx="2"/>
  <circle cx="{cx+228}" cy="{int(h*0.13)}" r="5" fill="#ffe080"/>
  <!-- Ground plaza -->
  <rect x="0" y="{int(h*0.73)}" width="{w}" height="{int(h*0.27)}" fill="#2a1a08" opacity="0.3"/>
  <!-- Fade bottom -->
  <rect width="{w}" height="{h}" fill="url(#fade)"/>
  <!-- City name -->
  <text x="{cx}" y="{h-52}" text-anchor="middle" font-family="Georgia,serif" font-size="{int(w*0.052)}" font-weight="700" fill="white" letter-spacing="4">SAMARKAND</text>
  <line x1="{cx-80}" y1="{h-38}" x2="{cx+80}" y2="{h-38}" stroke="#C8A45D" stroke-width="1.5" opacity="0.7"/>
  <text x="{cx}" y="{h-20}" text-anchor="middle" font-family="Arial,sans-serif" font-size="{int(w*0.013)}" fill="#C8A45D" letter-spacing="7">REGISTAN SQUARE · UNESCO HERITAGE</text>
</svg>'''

def svg_bukhara(w, h):
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1a0828"/><stop offset="100%" stop-color="#3d1850"/></linearGradient>
    <linearGradient id="tower" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#c87840"/><stop offset="100%" stop-color="#7a4010"/></linearGradient>
    <linearGradient id="fade" x1="0" y1="0.4" x2="0" y2="1"><stop offset="0%" stop-color="#1a0828" stop-opacity="0"/><stop offset="100%" stop-color="#1a0828" stop-opacity="0.9"/></linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#sky)"/>
  {''.join([f'<circle cx="{int(w*(i*41%100)/100)}" cy="{int(h*0.45*(i*59%100)/100)}" r="{0.7+i%3*0.5:.1f}" fill="white" opacity="{0.25+i%6*0.1:.2f}"/>' for i in range(45)])}
  <!-- Glow behind minaret -->
  <radialGradient id="glo" cx="50%" cy="25%" r="20%"><stop offset="0%" stop-color="#c87840" stop-opacity="0.35"/><stop offset="100%" stop-color="transparent"/></radialGradient>
  <rect width="{w}" height="{h}" fill="url(#glo)"/>
  <!-- Kalon Minaret base -->
  <rect x="{cx-28}" y="{int(h*0.55)}" width="56" height="{int(h*0.2)}" fill="url(#tower)" rx="2"/>
  <!-- Decorative bands on minaret -->
  {''.join([f'<rect x="{cx-28}" y="{int(h*(0.55 + i*0.03))}" width="56" height="3" fill="#e8a060" opacity="0.4"/>' for i in range(6)])}
  <!-- Minaret body -->
  <polygon points="{cx-26},{int(h*0.18)} {cx-22},{int(h*0.55)} {cx+22},{int(h*0.55)} {cx+26},{int(h*0.18)}" fill="url(#tower)"/>
  <!-- Minaret bands (14 traditional bands) -->
  {''.join([f'<rect x="{int(cx-26+i*0.3)}" y="{int(h*(0.18+i*0.026))}" width="{int(52-i*0.6)}" height="4" fill="#e8b870" opacity="0.35"/>' for i in range(14)])}
  <!-- Minaret gallery balcony -->
  <rect x="{cx-34}" y="{int(h*0.155)}" width="68" height="10" fill="#e8a060" rx="2"/>
  <!-- Minaret lantern cap -->
  <path d="M{cx-18} {int(h*0.155)} Q{cx} {int(h*0.08)} {cx+18} {int(h*0.155)}" fill="#c87840"/>
  <ellipse cx="{cx}" cy="{int(h*0.095)}" rx="10" ry="7" fill="#e8a060"/>
  <rect x="{cx-2}" y="{int(h*0.04)}" width="4" height="{int(h*0.06)}" fill="#e8c060" rx="1"/>
  <circle cx="{cx}" cy="{int(h*0.038)}" r="4" fill="#ffe080"/>
  <!-- Mosque base -->
  <rect x="{cx-140}" y="{int(h*0.62)}" width="280" height="{int(h*0.15)}" fill="#2a1510" rx="3"/>
  <!-- Mosque arches -->
  {''.join([f'<path d="M{cx-120+i*40} {int(h*0.62)} Q{cx-100+i*40} {int(h*0.56)} {cx-80+i*40} {int(h*0.62)}" fill="none" stroke="#e8a060" stroke-width="2" opacity="0.6"/>' for i in range(6)])}
  <!-- Side structures -->
  <rect x="{cx-170}" y="{int(h*0.45)}" width="26" height="{int(h*0.3)}" fill="#3a1a08" rx="2"/>
  <path d="M{cx-170} {int(h*0.45)} Q{cx-157} {int(h*0.36)} {cx-144} {int(h*0.45)}" fill="#c87840"/>
  <rect x="{cx+144}" y="{int(h*0.45)}" width="26" height="{int(h*0.3)}" fill="#3a1a08" rx="2"/>
  <path d="M{cx+144} {int(h*0.45)} Q{cx+157} {int(h*0.36)} {cx+170} {int(h*0.45)}" fill="#c87840"/>
  <rect width="{w}" height="{h}" fill="url(#fade)"/>
  <text x="{cx}" y="{h-52}" text-anchor="middle" font-family="Georgia,serif" font-size="{int(w*0.052)}" font-weight="700" fill="white" letter-spacing="4">BUKHARA</text>
  <line x1="{cx-70}" y1="{h-38}" x2="{cx+70}" y2="{h-38}" stroke="#c87840" stroke-width="1.5" opacity="0.7"/>
  <text x="{cx}" y="{h-20}" text-anchor="middle" font-family="Arial,sans-serif" font-size="{int(w*0.013)}" fill="#c87840" letter-spacing="7">KALON MINARET · 2500 YEARS OLD</text>
</svg>'''

def svg_khiva(w, h):
    cx, cy = w // 2, h // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0.2" y2="1"><stop offset="0%" stop-color="#0d1e12"/><stop offset="100%" stop-color="#1a3820"/></linearGradient>
    <linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#d4843a"/><stop offset="100%" stop-color="#8a4010"/></linearGradient>
    <linearGradient id="tower" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#e8a050"/><stop offset="100%" stop-color="#a05018"/></linearGradient>
    <linearGradient id="fade" x1="0" y1="0.4" x2="0" y2="1"><stop offset="0%" stop-color="#0d1e12" stop-opacity="0"/><stop offset="100%" stop-color="#0d1e12" stop-opacity="0.9"/></linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#sky)"/>
  {''.join([f'<circle cx="{int(w*(i*43%100)/100)}" cy="{int(h*0.5*(i*61%100)/100)}" r="{0.6+i%3*0.5:.1f}" fill="white" opacity="{0.2+i%7*0.1:.2f}"/>' for i in range(38)])}
  <!-- Walls of Khiva Ichan Kala -->
  <rect x="0" y="{int(h*0.42)}" width="{w}" height="{int(h*0.33)}" fill="url(#wall)" rx="2"/>
  <!-- Battlements (top of wall) -->
  {''.join([f'<rect x="{i*52}" y="{int(h*0.35)}" width="26" height="{int(h*0.08)}" fill="url(#wall)" rx="2"/>' for i in range(w//52 + 2)])}
  <!-- Main gate - Islam Khodja Minaret -->
  <rect x="{cx-18}" y="{int(h*0.10)}" width="36" height="{int(h*0.68)}" fill="url(#tower)" rx="3"/>
  <!-- Minaret stripes -->
  {''.join([f'<rect x="{cx-18}" y="{int(h*(0.10+i*0.044))}" width="36" height="5" fill="#f0b860" opacity="0.4"/>' for i in range(15)])}
  <!-- Minaret cap -->
  <circle cx="{cx}" cy="{int(h*0.085)}" r="22" fill="#d4843a"/>
  <circle cx="{cx}" cy="{int(h*0.075)}" r="16" fill="#e8a050"/>
  <rect x="{cx-3}" y="{int(h*0.02)}" width="6" height="{int(h*0.06)}" fill="#e8c060" rx="1"/>
  <circle cx="{cx}" cy="{int(h*0.018)}" r="5" fill="#ffe080"/>
  <!-- Gate arch -->
  <rect x="{cx-55}" y="{int(h*0.48)}" width="110" height="{int(h*0.27)}" fill="#1a0d05" rx="3"/>
  <path d="M{cx-55} {int(h*0.48)} Q{cx} {int(h*0.35)} {cx+55} {int(h*0.48)}" fill="url(#tower)"/>
  <path d="M{cx-40} {int(h*0.50)} Q{cx} {int(h*0.39)} {cx+40} {int(h*0.50)}" fill="#e8a050" opacity="0.5"/>
  <!-- Tile work on gate -->
  <rect x="{cx-53}" y="{int(h*0.49)}" width="106" height="4" fill="#40a870" opacity="0.5"/>
  <!-- Side towers -->
  <rect x="{cx-190}" y="{int(h*0.30)}" width="40" height="{int(h*0.45)}" fill="url(#tower)" rx="3"/>
  <path d="M{cx-190} {int(h*0.30)} Q{cx-170} {int(h*0.18)} {cx-150} {int(h*0.30)}" fill="#e8a050"/>
  <rect x="{cx+150}" y="{int(h*0.30)}" width="40" height="{int(h*0.45)}" fill="url(#tower)" rx="3"/>
  <path d="M{cx+150} {int(h*0.30)} Q{cx+170} {int(h*0.18)} {cx+190} {int(h*0.30)}" fill="#e8a050"/>
  <rect width="{w}" height="{h}" fill="url(#fade)"/>
  <text x="{cx}" y="{h-52}" text-anchor="middle" font-family="Georgia,serif" font-size="{int(w*0.052)}" font-weight="700" fill="white" letter-spacing="4">KHIVA</text>
  <line x1="{cx-60}" y1="{h-38}" x2="{cx+60}" y2="{h-38}" stroke="#d4843a" stroke-width="1.5" opacity="0.7"/>
  <text x="{cx}" y="{h-20}" text-anchor="middle" font-family="Arial,sans-serif" font-size="{int(w*0.013)}" fill="#d4843a" letter-spacing="7">ICHAN KALA · WALLED CITY · UNESCO</text>
</svg>'''

def svg_tashkent(w, h):
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0.1" y2="1"><stop offset="0%" stop-color="#080d18"/><stop offset="100%" stop-color="#101828"/></linearGradient>
    <linearGradient id="bldg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1a2a3a"/><stop offset="100%" stop-color="#0a1520"/></linearGradient>
    <linearGradient id="fade" x1="0" y1="0.3" x2="0" y2="1"><stop offset="0%" stop-color="#080d18" stop-opacity="0"/><stop offset="100%" stop-color="#080d18" stop-opacity="0.88"/></linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#sky)"/>
  {''.join([f'<circle cx="{int(w*(i*47%100)/100)}" cy="{int(h*0.55*(i*67%100)/100)}" r="{0.5+i%4*0.4:.1f}" fill="white" opacity="{0.2+i%8*0.08:.2f}"/>' for i in range(50)])}
  <!-- City skyline - modern buildings -->
  <!-- Tashkent Tower (TV Tower inspired) -->
  <rect x="{cx-8}" y="{int(h*0.05)}" width="16" height="{int(h*0.65)}" fill="#1a2840"/>
  <ellipse cx="{cx}" cy="{int(h*0.28)}" rx="28" ry="18" fill="#253850"/>
  <rect x="{cx-5}" y="{int(h*0.05)}" width="10" height="{int(h*0.24)}" fill="#203040"/>
  <circle cx="{cx}" cy="{int(h*0.04)}" r="8" fill="#5aaa5a" opacity="0.9"/>
  <!-- Building 1 -->
  <rect x="{cx-170}" y="{int(h*0.32)}" width="60" height="{int(h*0.43)}" fill="url(#bldg)"/>
  {''.join([f'<rect x="{cx-165}" y="{int(h*(0.34+i*0.065))}" width="10" height="8" fill="#5a8ab0" opacity="0.6"/><rect x="{cx-150}" y="{int(h*(0.34+i*0.065))}" width="10" height="8" fill="#5a8ab0" opacity="0.6"/><rect x="{cx-135}" y="{int(h*(0.34+i*0.065))}" width="10" height="8" fill="#5a8ab0" opacity="0.6"/>' for i in range(6)])}
  <!-- Building 2 -->
  <rect x="{cx-100}" y="{int(h*0.22)}" width="46" height="{int(h*0.53)}" fill="url(#bldg)"/>
  <!-- Building 3 -->
  <rect x="{cx+54}" y="{int(h*0.28)}" width="52" height="{int(h*0.47)}" fill="url(#bldg)"/>
  <!-- Building 4 -->
  <rect x="{cx+116}" y="{int(h*0.38)}" width="65" height="{int(h*0.37)}" fill="url(#bldg)"/>
  <!-- Chorsu Bazaar dome -->
  <ellipse cx="{cx-200}" cy="{int(h*0.50)}" rx="45" ry="30" fill="#203858"/>
  <ellipse cx="{cx-200}" cy="{int(h*0.48)}" rx="30" ry="18" fill="#2a4868"/>
  <!-- Ground / street -->
  <rect x="0" y="{int(h*0.72)}" width="{w}" height="{int(h*0.28)}" fill="#0a1020" opacity="0.4"/>
  <!-- Street lights -->
  {''.join([f'<line x1="{50+i*120}" y1="{int(h*0.72)}" x2="{50+i*120}" y2="{int(h*0.62)}" stroke="#4a7a5a" stroke-width="2" opacity="0.6"/><circle cx="{50+i*120}" cy="{int(h*0.62)}" r="4" fill="#aaee88" opacity="0.7"/>' for i in range(w//120+1)])}
  <rect width="{w}" height="{h}" fill="url(#fade)"/>
  <text x="{cx}" y="{h-52}" text-anchor="middle" font-family="Georgia,serif" font-size="{int(w*0.052)}" font-weight="700" fill="white" letter-spacing="4">TASHKENT</text>
  <line x1="{cx-70}" y1="{h-38}" x2="{cx+70}" y2="{h-38}" stroke="#5aaa5a" stroke-width="1.5" opacity="0.7"/>
  <text x="{cx}" y="{h-20}" text-anchor="middle" font-family="Arial,sans-serif" font-size="{int(w*0.013)}" fill="#5aaa5a" letter-spacing="7">CAPITAL CITY · MODERN &amp; ANCIENT</text>
</svg>'''

def svg_generic(city, w, h, color='#C8A45D', sky1='#061826', sky2='#0d2640'):
    cx = w // 2
    label = city.replace('-', ' ').upper()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{sky1}"/><stop offset="100%" stop-color="{sky2}"/></linearGradient>
    <linearGradient id="fade" x1="0" y1="0.4" x2="0" y2="1"><stop offset="0%" stop-color="{sky1}" stop-opacity="0"/><stop offset="100%" stop-color="{sky1}" stop-opacity="0.9"/></linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#sky)"/>
  {''.join([f'<circle cx="{int(w*(i*43%100)/100)}" cy="{int(h*0.5*(i*57%100)/100)}" r="{0.7+i%3*0.5:.1f}" fill="white" opacity="{0.25+i%6*0.1:.2f}"/>' for i in range(40)])}
  <g opacity="0.25">
    <rect x="{cx-80}" y="{int(h*0.28)}" width="160" height="{int(h*0.46)}" fill="{color}" rx="2"/>
    <path d="M{cx-80} {int(h*0.28)} Q{cx} {int(h*0.10)} {cx+80} {int(h*0.28)}" fill="{color}"/>
    <rect x="{cx-52}" y="{int(h*0.38)}" width="104" height="{int(h*0.36)}" fill="{sky1}" rx="2"/>
    <ellipse cx="{cx}" cy="{int(h*0.17)}" rx="40" ry="26" fill="{color}"/>
    <ellipse cx="{cx}" cy="{int(h*0.155)}" rx="28" ry="17" fill="{sky2}"/>
    <rect x="{cx-175}" y="{int(h*0.35)}" width="22" height="{int(h*0.39)}" fill="{color}" rx="2"/>
    <rect x="{cx+153}" y="{int(h*0.35)}" width="22" height="{int(h*0.39)}" fill="{color}" rx="2"/>
  </g>
  <rect width="{w}" height="{h}" fill="url(#fade)"/>
  <text x="{cx}" y="{h-52}" text-anchor="middle" font-family="Georgia,serif" font-size="{int(w*0.05)}" font-weight="700" fill="white" letter-spacing="4">{label}</text>
  <line x1="{cx-60}" y1="{h-38}" x2="{cx+60}" y2="{h-38}" stroke="{color}" stroke-width="1.5" opacity="0.7"/>
  <text x="{cx}" y="{h-20}" text-anchor="middle" font-family="Arial,sans-serif" font-size="{int(w*0.013)}" fill="{color}" letter-spacing="6">UZBEKISTAN · SILK ROAD</text>
</svg>'''


GENERATORS = {
    'samarkand': svg_samarkand,
    'bukhara':   svg_bukhara,
    'khiva':     svg_khiva,
    'tashkent':  svg_tashkent,
}

GENERIC_CONFIGS = {
    'fergana':    ('#c87a2a', '#200a00', '#401500'),
    'shahrisabz': ('#8ab840', '#0a1a05', '#152808'),
    'nukus':      ('#40a8b8', '#051218', '#0a2030'),
    'termez':     ('#d4603a', '#180800', '#301005'),
    'namangan':   ('#d04040', '#180808', '#300808'),
}

@photos_bp.route('/photo/<city>')
def city_photo(city):
    w = min(int(request.args.get('w', 800)), 1920)
    h = min(int(request.args.get('h', 600)), 1080)
    city_key = city.lower().replace('-valley','').replace('-','').replace(' ','').strip()

    gen = GENERATORS.get(city_key)
    if gen:
        svg = gen(w, h)
    else:
        cfg = GENERIC_CONFIGS.get(city_key, ('#C8A45D', '#061826', '#0d2640'))
        svg = svg_generic(city_key, w, h, *cfg)

    return Response(svg, mimetype='image/svg+xml',
                    headers={'Cache-Control': 'public, max-age=604800'})
