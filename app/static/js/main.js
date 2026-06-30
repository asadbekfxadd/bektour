/* ═══════════════════════════════════════════
   BEK TOUR — Enterprise JS  |  Mobile-First
   ═══════════════════════════════════════════ */
'use strict';

/* ── Cursor (desktop only) ──────────────── */
(function() {
  if (window.matchMedia('(hover: none)').matches) return;
  const el = document.getElementById('cur');
  if (!el) return;
  const dot = el.querySelector('.cur-dot');
  const ring = el.querySelector('.cur-ring');
  let mx = 0, my = 0, rx = 0, ry = 0;
  document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; dot.style.left = mx+'px'; dot.style.top = my+'px'; });
  (function tick() { rx += (mx-rx)*.12; ry += (my-ry)*.12; ring.style.left = rx+'px'; ring.style.top = ry+'px'; requestAnimationFrame(tick); })();
  const hoverEls = 'a,button,[data-fav],[data-cmp],.calc-svc,.r-card,.vcard,.s-tab';
  document.querySelectorAll(hoverEls).forEach(e => {
    e.addEventListener('mouseenter', () => el.classList.add('big'));
    e.addEventListener('mouseleave', () => el.classList.remove('big'));
  });
})();

/* ── Preloader ──────────────────────────── */
(function() {
  const pl = document.getElementById('preloader');
  const fill = document.getElementById('plFill');
  const pct = document.getElementById('plPct');
  if (!pl) return;
  let n = 0;
  const iv = setInterval(() => {
    n = Math.min(n + Math.random() * 13 + 5, 100);
    if (fill) fill.style.width = n + '%';
    if (pct)  pct.textContent = Math.floor(n) + '%';
    if (n >= 100) { clearInterval(iv); setTimeout(() => pl.classList.add('out'), 480); }
  }, 55);
  window.addEventListener('load', () => { n = 100; setTimeout(() => pl.classList.add('out'), 700); });
})();

/* ── Header ─────────────────────────────── */
const header = document.getElementById('header');
const hasHero = !!document.querySelector('.hero');
function syncHeader() {
  if (!header) return;
  const s = window.scrollY > 50;
  header.classList.toggle('glass', s || !hasHero);
  header.classList.toggle('over',  !s && hasHero);
}
syncHeader();
window.addEventListener('scroll', syncHeader, { passive: true });

/* ── Mobile nav ─────────────────────────── */
const burger = document.getElementById('burger');
const mobNav = document.getElementById('mobNav');
if (burger && mobNav) {
  burger.addEventListener('click', () => {
    const open = mobNav.classList.toggle('open');
    burger.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
  mobNav.querySelectorAll('.mob-nav-a').forEach(a => {
    a.addEventListener('click', () => {
      mobNav.classList.remove('open');
      burger.classList.remove('open');
      document.body.style.overflow = '';
    });
  });
}

/* ── Reveal on scroll ───────────────────── */
const revObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); revObs.unobserve(e.target); } });
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
document.querySelectorAll('.reveal').forEach(el => revObs.observe(el));

/* ── Counter animation ──────────────────── */
function runCount(el) {
  const end = parseInt(el.dataset.n || '0');
  const suf = el.dataset.s || '';
  let cur = 0;
  const step = end / 55;
  const iv = setInterval(() => {
    cur = Math.min(cur + step, end);
    el.textContent = Math.floor(cur).toLocaleString() + suf;
    if (cur >= end) clearInterval(iv);
  }, 16);
}
const cntObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.querySelectorAll('[data-n]').forEach(runCount); cntObs.unobserve(e.target); }
  });
}, { threshold: 0.3 });
document.querySelectorAll('.stats-strip').forEach(s => cntObs.observe(s));

/* ── CALCULATOR ─────────────────────────── */
(function() {
  const totalEl = document.getElementById('calcTotal');
  const perEl   = document.getElementById('calcPer');
  const bdEl    = document.getElementById('calcBd');
  if (!totalEl) return;

  const PRICES = {
    hotel3:   { base: 55,  lbl_en: '3★ Hotel',     lbl_ru: 'Отель 3★',     lbl_uz: '3★ Mehmonxona' },
    hotel4:   { base: 100, lbl_en: '4★ Hotel',     lbl_ru: 'Отель 4★',     lbl_uz: '4★ Mehmonxona' },
    hotel5:   { base: 200, lbl_en: '5★ Hotel',     lbl_ru: 'Отель 5★',     lbl_uz: '5★ Mehmonxona' },
    car:      { base: 60,  lbl_en: 'Car',           lbl_ru: 'Авто',          lbl_uz: 'Avtomobil' },
    guide:    { base: 80,  lbl_en: 'Guide',         lbl_ru: 'Гид',           lbl_uz: 'Gid' },
    transfer: { base: 35,  lbl_en: 'Transfers',     lbl_ru: 'Трансферы',     lbl_uz: 'Transferlar' },
    meals:    { base: 40,  lbl_en: 'Meals (full)',  lbl_ru: 'Питание (полн)','lbl_uz': 'Ovqat' },
    excur:    { base: 50,  lbl_en: 'Excursions',    lbl_ru: 'Экскурсии',     lbl_uz: 'Ekskursiyalar' },
    visa:     { base: 50,  lbl_en: 'Visa Support',  lbl_ru: 'Виза',          lbl_uz: 'Viza' },
    vip:      { base: 150, lbl_en: 'VIP Services',  lbl_ru: 'VIP-сервис',    lbl_uz: 'VIP xizmat' },
  };

  const CITY_MULT = {
    samarkand:1.1, bukhara:1.0, khiva:.9, tashkent:1.05,
    fergana:.85, shahrisabz:.9, nukus:.85, termez:.85, namangan:.8,
  };

  const CURR = { USD: 1, EUR: .92, GBP: .79, AED: 3.67, RUB: 90, UZS: 12700 };
  const CURR_SYM = { USD: '$', EUR: '€', GBP: '£', AED: 'AED', RUB: '₽', UZS: 'so\'m' };

  let selected = new Set(['hotel4', 'guide', 'transfer']);

  document.querySelectorAll('.calc-svc').forEach(btn => {
    const svc = btn.dataset.svc;
    if (selected.has(svc)) btn.classList.add('on');
    btn.addEventListener('click', () => {
      selected.has(svc) ? selected.delete(svc) : selected.add(svc);
      btn.classList.toggle('on', selected.has(svc));
      calc();
    });
  });

  function getVal(id) { const el = document.getElementById(id); return el ? el.value : ''; }

  function calc() {
    const nights  = parseInt(getVal('calcNights'))  || 3;
    const adults  = parseInt(getVal('calcAdults'))  || 2;
    const children= parseInt(getVal('calcChildren'))|| 0;
    const city    = getVal('calcCity')  || 'samarkand';
    const curr    = getVal('calcCurr') || 'USD';
    const mult    = CITY_MULT[city] || 1.0;
    const guests  = adults + children * .5;
    const rate    = CURR[curr] || 1;
    const sym     = CURR_SYM[curr] || '$';
    const lang    = document.documentElement.lang || 'en';
    const lkey    = lang === 'ru' ? 'lbl_ru' : lang === 'uz' ? 'lbl_uz' : 'lbl_en';

    let total = 0; const parts = [];
    selected.forEach(svc => {
      const p = PRICES[svc]; if (!p) return;
      let cost = 0;
      if (['hotel3','hotel4','hotel5'].includes(svc)) cost = p.base * nights * mult;
      else if (svc === 'car')      cost = p.base * nights * mult;
      else if (svc === 'guide')    cost = p.base * nights;
      else if (svc === 'meals')    cost = p.base * nights * guests;
      else if (svc === 'transfer') cost = p.base * 2;
      else if (svc === 'visa')     cost = p.base * adults;
      else if (svc === 'excur')    cost = p.base * guests;
      else if (svc === 'vip')      cost = p.base * nights;
      cost = Math.round(cost * rate);
      total += cost;
      parts.push((p[lkey] || p.lbl_en) + ': ' + sym + cost.toLocaleString());
    });

    const perPerson = adults > 0 ? Math.round(total / adults) : total;

    if (totalEl) totalEl.textContent = sym + total.toLocaleString();
    if (perEl)   perEl.textContent   = sym + perPerson.toLocaleString() + ' / person';
    if (bdEl)    bdEl.textContent    = parts.join('  ·  ');
  }

  ['calcNights','calcAdults','calcChildren','calcCity','calcCurr'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('change', calc);
  });
  calc();
})();

/* ── Search tabs ────────────────────────── */
document.querySelectorAll('.s-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.s-tab').forEach(t => t.classList.remove('on'));
    tab.classList.add('on');
    const inp = document.getElementById('sType');
    if (inp) inp.value = tab.dataset.type || '';
  });
});

/* ── Favorites ──────────────────────────── */
const FK = 'bt_favs_v3';
const getFavs = () => { try { return JSON.parse(localStorage.getItem(FK) || '[]'); } catch { return []; } };
function initFavs() {
  const favs = getFavs();
  document.querySelectorAll('[data-fav]').forEach(btn => {
    if (favs.includes(btn.dataset.fav)) btn.classList.add('liked');
    btn.addEventListener('click', e => {
      e.preventDefault(); e.stopPropagation();
      const id = btn.dataset.fav;
      let list = getFavs();
      const i = list.indexOf(id);
      if (i === -1) { list.push(id); btn.classList.add('liked'); showToast('❤️ Saved to favorites'); }
      else { list.splice(i, 1); btn.classList.remove('liked'); showToast('Removed from favorites'); }
      localStorage.setItem(FK, JSON.stringify(list));
    });
  });
}

/* ── Compare ─────────────────────────────── */
let cmpList = [];
const cmpBar = document.getElementById('cmpBar');
function initCmp() {
  document.querySelectorAll('[data-cmp]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault(); e.stopPropagation();
      const id = btn.dataset.cmp, name = btn.dataset.name || '';
      const i = cmpList.findIndex(x => x.id === id);
      if (i === -1) {
        if (cmpList.length >= 3) { showToast('Max 3 to compare'); return; }
        cmpList.push({ id, name }); btn.classList.add('liked'); showToast('Added to compare');
      } else { cmpList.splice(i, 1); btn.classList.remove('liked'); }
      updateCmpBar();
    });
  });
}
function updateCmpBar() {
  if (!cmpBar) return;
  cmpBar.classList.toggle('up', cmpList.length > 0);
  const el = cmpBar.querySelector('.cmp-chips');
  if (el) el.innerHTML = cmpList.map(x =>
    `<div class="cmp-chip">${x.name}<span class="cmp-x" onclick="removeCmp('${x.id}')">✕</span></div>`
  ).join('');
}
window.removeCmp = id => { cmpList = cmpList.filter(x => x.id !== id); document.querySelectorAll(`[data-cmp="${id}"]`).forEach(b => b.classList.remove('liked')); updateCmpBar(); };
window.clearCmp  = ()  => { cmpList = []; document.querySelectorAll('.liked[data-cmp]').forEach(b => b.classList.remove('liked')); updateCmpBar(); };

/* ── FAQ ─────────────────────────────────── */
function initFAQ() {
  document.querySelectorAll('.faq-q').forEach(q => {
    q.addEventListener('click', () => {
      const item = q.parentElement, was = item.classList.contains('open');
      document.querySelectorAll('.faq-i').forEach(f => f.classList.remove('open'));
      if (!was) item.classList.add('open');
    });
  });
}

/* ── Gallery thumbs ─────────────────────── */
function initGallery() {
  const main = document.getElementById('mainImg');
  if (!main) return;
  document.querySelectorAll('.detail-thumb').forEach(t => {
    t.addEventListener('click', () => {
      const src = t.querySelector('img')?.src.replace(/\/\d+\/\d+$/, '/1200/700');
      if (src) main.src = src;
    });
  });
}

/* ── Toast ───────────────────────────────── */
function showToast(msg, type = 'success') {
  let box = document.querySelector('.toast-wrap');
  if (!box) { box = document.createElement('div'); box.className = 'toast-wrap'; document.body.appendChild(box); }
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;
  el.innerHTML = `<i class="fa fa-${type==='success'?'check-circle':'exclamation-circle'}"></i>${msg}<button onclick="this.parentElement.remove()">✕</button>`;
  box.appendChild(el);
  setTimeout(() => { el.style.opacity = '0'; el.style.transition = 'opacity .3s'; setTimeout(() => el.remove(), 320); }, 3200);
}
window.showToast = showToast;
window.toast = showToast;

/* ── Flash dismiss ──────────────────────── */
document.querySelectorAll('.toast').forEach(t => setTimeout(() => t.remove(), 5000));

/* ── Price calculator on detail ─────────── */
(function() {
  const ciEl = document.getElementById('checkIn');
  const coEl = document.getElementById('checkOut');
  if (!ciEl || !coEl) return;
  const price = parseFloat(document.getElementById('propPrice')?.dataset.price || '0');
  ciEl.min = new Date().toISOString().split('T')[0];
  function calc() {
    const ci = ciEl.value, co = coEl.value;
    if (!ci || !co) return;
    const n = Math.round((new Date(co) - new Date(ci)) / 86400000);
    if (n <= 0) return;
    const total = n * price;
    const bd = document.getElementById('priceBd');
    const nlbl = document.getElementById('nlabel');
    const nprice = document.getElementById('nprice');
    const ntotal = document.getElementById('ntotal');
    if (nlbl)  nlbl.textContent  = n + ' night' + (n > 1 ? 's' : '');
    if (nprice) nprice.textContent = '$' + total.toLocaleString();
    if (ntotal) ntotal.textContent = '$' + total.toLocaleString();
    if (bd) bd.style.display = 'block';
  }
  ciEl.addEventListener('change', () => { if (coEl) coEl.min = ciEl.value; calc(); });
  coEl.addEventListener('change', calc);
})();

/* ── Init ────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initFavs();
  initCmp();
  initFAQ();
  initGallery();
});

/* ── Currency Converter ─────────────────── */
function convertCurr() {
  const amt = parseFloat(document.getElementById('currAmt')?.value || '100');
  const rate = parseFloat(document.getElementById('currFrom')?.value || '1');
  const uzs = Math.round(amt / rate * 12700);
  const el = document.getElementById('currResult');
  if (el) el.textContent = uzs.toLocaleString();
}
window.convertCurr = convertCurr;

/* ── Visa Checker ───────────────────────── */
const VISA_FREE = ['USA','United Kingdom','Germany','France','Italy','Spain','Japan','South Korea','Australia','Canada','UAE','Netherlands','Switzerland','Sweden','Norway','Israel','Singapore','Malaysia','Turkey','Brazil','Argentina','Mexico','Indonesia','Thailand'];
function checkVisa() {
  const country = document.getElementById('visaCountry')?.value;
  const el = document.getElementById('visaResult');
  if (!el || !country) return;
  const lang = document.documentElement.lang || 'en';
  if (VISA_FREE.includes(country)) {
    el.innerHTML = `<div style="color:#16A34A;font-weight:700;font-size:.88rem;margin-bottom:4px;">✓ ${lang==='ru'?'Виза не нужна!':'Visa-free entry!'}</div><div style="font-size:.74rem;color:var(--muted);">${lang==='ru'?'До 30 дней без визы · Только паспорт':'Up to 30 days · Passport only'}</div>`;
  } else {
    el.innerHTML = `<div style="color:#C8A45D;font-weight:700;font-size:.88rem;margin-bottom:4px;">${lang==='ru'?'Нужна электронная виза':'E-Visa Required'}</div><div style="font-size:.74rem;color:var(--muted);">${lang==='ru'?'Онлайн заявка · 3-5 рабочих дней · ~$20':'Online application · 3-5 business days · ~$20'}</div><a href="https://e-visa.gov.uz" target="_blank" style="font-size:.72rem;color:var(--gold);font-weight:600;text-decoration:none;">e-visa.gov.uz →</a>`;
  }
}
window.checkVisa = checkVisa;

/* ── Tour Category Filter ───────────────── */
function filterTours(cat) {
  document.querySelectorAll('.sec-tab').forEach(t => t.classList.remove('on'));
  event.target.closest('.sec-tab').classList.add('on');
  document.querySelectorAll('#toursGrid .tour-card').forEach(card => {
    const match = cat === 'all' || card.dataset.cat === cat;
    card.style.display = match ? '' : 'none';
  });
}
window.filterTours = filterTours;

/* ── Tour grid responsive ───────────────── */
(function() {
  const grid = document.getElementById('toursGrid');
  if (grid) {
    grid.style.gridTemplateColumns = window.innerWidth >= 900 ? 'repeat(3,1fr)' : window.innerWidth >= 560 ? 'repeat(2,1fr)' : '1fr';
    window.addEventListener('resize', () => {
      if (grid) grid.style.gridTemplateColumns = window.innerWidth >= 900 ? 'repeat(3,1fr)' : window.innerWidth >= 560 ? 'repeat(2,1fr)' : '1fr';
    });
  }
})();

/* ════════════════════════════════════════════════════
   IMMERSIVE VIDEO CARD SYSTEM
   Handles: hover-autoplay (desktop), tap-to-play (touch),
   lazy loading, single-active-video, viewport pause.
   Works for .dest-slide-media, .dvideo-card, .dest-hero-media
   ════════════════════════════════════════════════════ */
(function () {
  const isTouch = window.matchMedia('(hover: none)').matches;
  let activeVideo = null;

  function lazyAttachSource(video) {
    if (video.dataset.loaded === '1') return;
    const src = video.dataset.src;
    const srcWebm = video.dataset.srcWebm;
    if (!src && !srcWebm) return;
    if (srcWebm) {
      const sWebm = document.createElement('source');
      sWebm.src = srcWebm; sWebm.type = 'video/webm';
      video.appendChild(sWebm);
    }
    if (src) {
      const sMp4 = document.createElement('source');
      sMp4.src = src; sMp4.type = 'video/mp4';
      video.appendChild(sMp4);
    }
    video.load();
    video.dataset.loaded = '1';
  }

  function playVideo(video) {
    if (!video || !video.dataset.src && !video.dataset.srcWebm) return;
    lazyAttachSource(video);
    if (activeVideo && activeVideo !== video) pauseVideo(activeVideo);
    activeVideo = video;
    video.muted = true;
    const p = video.play();
    if (p && p.catch) p.catch(() => {});
    video.classList.add(video.dataset.readyClass || 'dsm-ready');
  }

  function pauseVideo(video) {
    if (!video) return;
    video.pause();
    video.classList.remove(video.dataset.readyClass || 'dsm-ready');
  }

  /* Card hover (desktop) */
  function initVideoCards(selector, readyClass) {
    document.querySelectorAll(selector).forEach(card => {
      const video = card.querySelector('video');
      if (!video) return;
      video.dataset.readyClass = readyClass;

      if (!isTouch) {
        card.addEventListener('mouseenter', () => playVideo(video));
        card.addEventListener('mouseleave', () => pauseVideo(video));
      } else {
        // Touch: tap toggles play, only one active globally
        card.addEventListener('click', e => {
          if (video.classList.contains(readyClass) && !video.paused) return; // allow link nav through
          e.preventDefault();
          playVideo(video);
        });
      }
    });
  }
  initVideoCards('.dest-slide', 'dsm-ready');
  initVideoCards('.dvideo-card', 'dvc-ready');

  /* Pause any playing card video when scrolled out of view (perf) */
  const cardObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) {
        const v = e.target.querySelector('video');
        if (v && v === activeVideo) pauseVideo(v);
      }
    });
  }, { threshold: 0 });
  document.querySelectorAll('.dest-slide, .dvideo-card').forEach(c => cardObs.observe(c));

  /* Destination hero video: autoplay muted once visible, with mute toggle */
  const heroMedia = document.querySelector('.dest-hero-media');
  if (heroMedia) {
    const heroVideo = heroMedia.querySelector('video');
    if (heroVideo && (heroVideo.dataset.src || heroVideo.dataset.srcWebm)) {
      lazyAttachSource(heroVideo);
      heroVideo.muted = true;
      const playP = heroVideo.play();
      if (playP && playP.then) {
        playP.then(() => {
          heroVideo.classList.add('dh-ready');
          heroMedia.classList.add('dh-playing');
        }).catch(() => {});
      }
    }
    const muteBtn = document.getElementById('destHeroMute');
    if (muteBtn && heroVideo) {
      muteBtn.addEventListener('click', () => {
        heroVideo.muted = !heroVideo.muted;
        muteBtn.innerHTML = heroVideo.muted
          ? '<i class="fa fa-volume-mute"></i>'
          : '<i class="fa fa-volume-up"></i>';
      });
    }
  }

  /* Sticky booking bar reveal on scroll past hero (destination page) */
  const stickyBar = document.getElementById('destStickyBar');
  const destHeroEl = document.querySelector('.dest-hero');
  if (stickyBar && destHeroEl) {
    const heroObs = new IntersectionObserver(entries => {
      entries.forEach(e => stickyBar.classList.toggle('show', !e.isIntersecting));
    }, { threshold: 0 });
    heroObs.observe(destHeroEl);
  }

  /* Chip nav active state + smooth scroll (destination page) */
  document.querySelectorAll('.dest-chip').forEach(chip => {
    chip.addEventListener('click', e => {
      document.querySelectorAll('.dest-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
    });
  });
})();
