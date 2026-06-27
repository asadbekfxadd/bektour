/* BEK TOUR — Premium JS 2026 */

// ── Preloader ──────────────────────────────
window.addEventListener('load', () => {
  setTimeout(() => {
    const p = document.getElementById('preloader');
    if (p) p.classList.add('done');
  }, 1800);
});

// ── Particles in hero ─────────────────────
function createParticles() {
  const container = document.querySelector('.hero-particles');
  if (!container) return;
  for (let i = 0; i < 20; i++) {
    const p = document.createElement('div');
    p.className = 'hero-particle';
    p.style.left = Math.random() * 100 + '%';
    p.style.animationDuration = (8 + Math.random() * 12) + 's';
    p.style.animationDelay = (Math.random() * 8) + 's';
    p.style.opacity = Math.random() * 0.6 + 0.2;
    container.appendChild(p);
  }
}
createParticles();

// ── Navbar scroll ─────────────────────────
const navbar = document.getElementById('navbar');
const isHeroPage = document.querySelector('.hero');

function updateNavbar() {
  if (!navbar) return;
  if (isHeroPage) {
    if (window.scrollY > 60) {
      navbar.classList.add('scrolled');
      navbar.classList.remove('hero-mode');
    } else {
      navbar.classList.remove('scrolled');
      navbar.classList.add('hero-mode');
    }
  } else {
    navbar.classList.add('scrolled');
  }
}
updateNavbar();
window.addEventListener('scroll', updateNavbar);

// ── Hamburger ─────────────────────────────
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');
if (hamburger && navMenu) {
  hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('open');
    document.body.style.overflow = navMenu.classList.contains('open') ? 'hidden' : '';
  });
}

// ── Toast auto-dismiss ────────────────────
document.querySelectorAll('.toast').forEach(t => setTimeout(() => t.remove(), 5000));

// ── Reveal on scroll ──────────────────────
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); revealObserver.unobserve(e.target); } });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ── Counter animation ─────────────────────
function animateCounter(el) {
  const target = parseInt(el.dataset.target || el.textContent);
  const suffix = el.dataset.suffix || '';
  let current = 0;
  const step = target / 60;
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = Math.floor(current).toLocaleString() + suffix;
    if (current >= target) clearInterval(timer);
  }, 16);
}
const counterObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.querySelectorAll('[data-counter]').forEach(animateCounter);
      counterObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.3 });
document.querySelectorAll('.stats-section').forEach(el => counterObserver.observe(el));

// ── Favorites ─────────────────────────────
const FAV_KEY = 'bektour_favs_v2';
function getFavs() { try { return JSON.parse(localStorage.getItem(FAV_KEY) || '[]'); } catch { return []; } }
function saveFavs(f) { localStorage.setItem(FAV_KEY, JSON.stringify(f)); }

function initFavorites() {
  const favs = getFavs();
  document.querySelectorAll('[data-fav]').forEach(btn => {
    const id = btn.dataset.fav;
    if (favs.includes(id)) btn.classList.add('liked');
    btn.addEventListener('click', e => {
      e.preventDefault();
      let list = getFavs();
      const idx = list.indexOf(id);
      if (idx === -1) { list.push(id); btn.classList.add('liked'); showToast('❤️ Added to favorites'); }
      else { list.splice(idx, 1); btn.classList.remove('liked'); showToast('Removed from favorites'); }
      saveFavs(list);
    });
  });
}

// ── Compare ───────────────────────────────
let comparing = [];
const compareBar = document.getElementById('compareBar');

function initCompare() {
  document.querySelectorAll('[data-compare]').forEach(btn => {
    btn.addEventListener('click', e => {
      e.preventDefault();
      const id = btn.dataset.compare;
      const name = btn.dataset.name || 'Item';
      const idx = comparing.findIndex(i => i.id === id);
      if (idx === -1) {
        if (comparing.length >= 3) { showToast('Max 3 items to compare'); return; }
        comparing.push({ id, name });
        btn.classList.add('compared');
        showToast('Added to compare');
      } else {
        comparing.splice(idx, 1);
        btn.classList.remove('compared');
      }
      updateCompareBar();
    });
  });
}

function updateCompareBar() {
  if (!compareBar) return;
  compareBar.classList.toggle('show', comparing.length > 0);
  const el = compareBar.querySelector('.compare-items');
  if (el) el.innerHTML = comparing.map(i =>
    `<div class="compare-chip">${i.name}<span class="compare-chip-remove" onclick="removeCompare('${i.id}')">✕</span></div>`
  ).join('');
}

function removeCompare(id) {
  comparing = comparing.filter(i => i.id !== id);
  document.querySelectorAll(`[data-compare="${id}"]`).forEach(b => b.classList.remove('compared'));
  updateCompareBar();
}

function clearCompare() {
  comparing = [];
  document.querySelectorAll('.compared').forEach(b => b.classList.remove('compared'));
  updateCompareBar();
}

// ── Search tabs ───────────────────────────
function initTabs() {
  document.querySelectorAll('.search-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.search-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const input = document.getElementById('searchType');
      if (input) input.value = tab.dataset.type || '';
    });
  });
}

// ── FAQ ───────────────────────────────────
function initFAQ() {
  document.querySelectorAll('.faq-question').forEach(q => {
    q.addEventListener('click', () => {
      const item = q.parentElement;
      const wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    });
  });
}

// ── Toast ─────────────────────────────────
function showToast(msg, type = 'success') {
  const t = document.createElement('div');
  t.className = `toast toast-${type}`;
  t.innerHTML = `<i class="fa ${type==='success'?'fa-check-circle':'fa-exclamation-circle'}"></i>${msg}<button onclick="this.parentElement.remove()">✕</button>`;
  let container = document.querySelector('.toasts');
  if (!container) { container = document.createElement('div'); container.className = 'toasts'; document.body.appendChild(container); }
  container.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

// ── Smooth scroll for anchors ─────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
  });
});

// ── Init all ──────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initFavorites();
  initCompare();
  initTabs();
  initFAQ();
});
