/* BEK TOUR — Awwwards 2026 JS */
'use strict';

// ── Custom cursor ─────────────────────────────
(function() {
  const dot  = document.createElement('div');
  const ring = document.createElement('div');
  dot.className = 'cursor-dot';
  ring.className = 'cursor-ring';
  const wrap = document.createElement('div');
  wrap.className = 'cursor';
  wrap.appendChild(dot);
  wrap.appendChild(ring);
  document.body.appendChild(wrap);

  let mx = 0, my = 0, rx = 0, ry = 0;
  document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });

  function tick() {
    rx += (mx - rx) * .14;
    ry += (my - ry) * .14;
    dot.style.left  = mx + 'px';
    dot.style.top   = my + 'px';
    ring.style.left = rx + 'px';
    ring.style.top  = ry + 'px';
    requestAnimationFrame(tick);
  }
  tick();
  document.addEventListener('mouseleave', () => wrap.style.opacity = '0');
  document.addEventListener('mouseenter', () => wrap.style.opacity = '1');
})();

// ── Preloader ─────────────────────────────────
(function() {
  const pl = document.getElementById('preloader');
  if (!pl) return;
  const pct = pl.querySelector('.pl-percent');
  let n = 0;
  const iv = setInterval(() => {
    n = Math.min(n + Math.random() * 14 + 4, 100);
    if (pct) pct.textContent = Math.floor(n) + '%';
    if (n >= 100) { clearInterval(iv); setTimeout(() => pl.classList.add('out'), 400); }
  }, 50);
  window.addEventListener('load', () => { n = 100; setTimeout(() => pl.classList.add('out'), 600); });
})();

// ── Navbar ────────────────────────────────────
const nav = document.querySelector('.nav');
const isHero = !!document.querySelector('.hero');

function syncNav() {
  if (!nav) return;
  if (isHero) {
    nav.classList.toggle('glass', window.scrollY > 60);
    nav.classList.toggle('dark', window.scrollY <= 60);
  } else {
    nav.classList.add('glass');
    nav.classList.remove('dark');
  }
}
syncNav();
window.addEventListener('scroll', syncNav, { passive: true });

// ── Hamburger ─────────────────────────────────
const burger = document.getElementById('burger');
const navLinks = document.getElementById('navLinks');
if (burger && navLinks) {
  burger.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    document.body.style.overflow = open ? 'hidden' : '';
  });
}

// ── Reveal on scroll ──────────────────────────
const io = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: .1 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// ── Stats counter ─────────────────────────────
function runCounter(el) {
  const end = parseInt(el.dataset.n || '0');
  const suf = el.dataset.s || '';
  let cur = 0;
  const step = end / 60;
  const iv = setInterval(() => {
    cur = Math.min(cur + step, end);
    el.textContent = Math.floor(cur).toLocaleString() + suf;
    if (cur >= end) clearInterval(iv);
  }, 16);
}
const statsObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.querySelectorAll('[data-n]').forEach(runCounter); statsObs.unobserve(e.target); }
  });
}, { threshold: .3 });
document.querySelectorAll('.stats-s').forEach(s => statsObs.observe(s));

// ── Favorites ─────────────────────────────────
const FK = 'bt_favs';
const getFavs = () => { try { return JSON.parse(localStorage.getItem(FK) || '[]'); } catch { return []; } };
const setFavs = v => localStorage.setItem(FK, JSON.stringify(v));

function initFavs() {
  const favs = getFavs();
  document.querySelectorAll('[data-fav]').forEach(btn => {
    if (favs.includes(btn.dataset.fav)) btn.classList.add('liked');
    btn.addEventListener('click', e => {
      e.preventDefault(); e.stopPropagation();
      const id = btn.dataset.fav;
      let list = getFavs();
      const i = list.indexOf(id);
      if (i === -1) { list.push(id); btn.classList.add('liked'); toast('❤️ Added to favorites'); }
      else { list.splice(i, 1); btn.classList.remove('liked'); toast('Removed from favorites'); }
      setFavs(list);
    });
  });
}

// ── Compare ───────────────────────────────────
let cmpList = [];
const cmpBar = document.getElementById('cmpBar');

function initCompare() {
  document.querySelectorAll('[data-cmp]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault(); e.stopPropagation();
      const id = btn.dataset.cmp, name = btn.dataset.name || '';
      const i = cmpList.findIndex(x => x.id === id);
      if (i === -1) {
        if (cmpList.length >= 3) { toast('Max 3 to compare'); return; }
        cmpList.push({ id, name }); btn.classList.add('compared'); toast('Added to compare');
      } else { cmpList.splice(i, 1); btn.classList.remove('compared'); }
      updateCmpBar();
    });
  });
}

function updateCmpBar() {
  if (!cmpBar) return;
  cmpBar.classList.toggle('up', cmpList.length > 0);
  const el = cmpBar.querySelector('.cmp-chips');
  if (el) el.innerHTML = cmpList.map(x =>
    `<div class="cmp-chip">${x.name}<span class="cmp-remove" onclick="removeCmp('${x.id}')">✕</span></div>`
  ).join('');
}

window.removeCmp = id => {
  cmpList = cmpList.filter(x => x.id !== id);
  document.querySelectorAll(`[data-cmp="${id}"]`).forEach(b => b.classList.remove('compared'));
  updateCmpBar();
};
window.clearCmp = () => { cmpList = []; document.querySelectorAll('.compared').forEach(b => b.classList.remove('compared')); updateCmpBar(); };

// ── Search tabs ───────────────────────────────
function initTabs() {
  document.querySelectorAll('.s-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.s-tab').forEach(t => t.classList.remove('on'));
      tab.classList.add('on');
      const inp = document.getElementById('sType');
      if (inp) inp.value = tab.dataset.type || '';
    });
  });
}

// ── FAQ ───────────────────────────────────────
function initFAQ() {
  document.querySelectorAll('.faq-q').forEach(q => {
    q.addEventListener('click', () => {
      const item = q.parentElement;
      const was = item.classList.contains('open');
      document.querySelectorAll('.faq-i').forEach(f => f.classList.remove('open'));
      if (!was) item.classList.add('open');
    });
  });
}

// ── Toast ─────────────────────────────────────
function toast(msg, type = 'success') {
  let box = document.querySelector('.toasts');
  if (!box) { box = document.createElement('div'); box.className = 'toasts'; document.body.appendChild(box); }
  const el = document.createElement('div');
  el.className = `toast toast-${type}`;
  el.innerHTML = `<i class="fa fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>${msg}<button onclick="this.parentElement.remove()">✕</button>`;
  box.appendChild(el);
  setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 300); }, 3000);
}
window.toast = toast;

// ── Smooth anchor scroll ──────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const t = document.querySelector(a.getAttribute('href'));
    if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });
});

// ── Flashes ───────────────────────────────────
document.querySelectorAll('.toast').forEach(t => setTimeout(() => t.remove(), 5000));

// ── Init ──────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => { initFavs(); initCompare(); initTabs(); initFAQ(); });
