/* BEK TOUR — main.js */

// ── Preloader ────────────────────────────
(function() {
  const loader = document.getElementById('preloader');
  const fill = document.getElementById('preloader-fill');
  const status = document.getElementById('preloader-status');
  if (!loader) return;

  const msgs = ['Loading experience...', 'Preparing villas...', 'Almost ready...'];
  let progress = 0;
  let msgIdx = 0;

  const interval = setInterval(() => {
    progress += Math.random() * 18 + 8;
    if (progress > 100) progress = 100;
    if (fill) fill.style.width = progress + '%';
    if (status && progress > 40 && progress < 90) {
      msgIdx = Math.min(Math.floor(progress / 35), msgs.length - 1);
      status.textContent = msgs[msgIdx];
    }
    if (progress >= 100) {
      clearInterval(interval);
      setTimeout(() => { loader.classList.add('hidden'); }, 300);
    }
  }, 60);

  window.addEventListener('load', () => {
    progress = 100;
    if (fill) fill.style.width = '100%';
    setTimeout(() => { loader.classList.add('hidden'); }, 400);
  });
})();

// ── Sticky header ────────────────────────
const header = document.getElementById('header');
window.addEventListener('scroll', () => {
  if (header) header.classList.toggle('scrolled', window.scrollY > 10);
});

// ── Burger ───────────────────────────────
const burger = document.getElementById('burger');
const nav = document.getElementById('nav');
if (burger && nav) {
  burger.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    document.body.style.overflow = open ? 'hidden' : '';
    burger.classList.toggle('open', open);
  });
}

// ── Flash auto-hide ──────────────────────
document.querySelectorAll('.flash').forEach(el => setTimeout(() => el.remove(), 5000));

// ── Fade-up on scroll ────────────────────
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); observer.unobserve(e.target); } });
}, { threshold: 0.12 });
document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));

// ── Favorites ────────────────────────────
const FAV_KEY = 'bektour_favs';
function getFavs() { try { return JSON.parse(localStorage.getItem(FAV_KEY) || '[]'); } catch { return []; } }

function initFavorites() {
  const favs = getFavs();
  document.querySelectorAll('[data-fav-id]').forEach(btn => {
    if (favs.includes(btn.dataset.favId)) {
      btn.classList.add('favorited');
      btn.querySelector('i').className = 'fa fa-heart';
    }
    btn.addEventListener('click', () => {
      const id = btn.dataset.favId;
      let list = getFavs();
      const idx = list.indexOf(id);
      if (idx === -1) {
        list.push(id); btn.classList.add('favorited');
        showToast('❤️ Added to favorites');
      } else {
        list.splice(idx, 1); btn.classList.remove('favorited');
        showToast('Removed from favorites');
      }
      localStorage.setItem(FAV_KEY, JSON.stringify(list));
    });
  });
}

// ── Compare ──────────────────────────────
let compareList = [];
const compareBar = document.getElementById('compare-bar');

function toggleCompare(btn, id, name) {
  const idx = compareList.findIndex(i => i.id === id);
  if (idx === -1) {
    if (compareList.length >= 3) { showToast('⚖️ Max 3 items'); return; }
    compareList.push({ id, name });
    btn.classList.add('compared');
    showToast('Added to compare');
  } else {
    compareList.splice(idx, 1);
    btn.classList.remove('compared');
  }
  updateCompareBar();
}

function removeCompare(id) {
  compareList = compareList.filter(i => i.id !== id);
  document.querySelectorAll(`[data-cmp-id="${id}"]`).forEach(b => b.classList.remove('compared'));
  updateCompareBar();
}

function clearCompare() {
  compareList = [];
  document.querySelectorAll('.compared').forEach(b => b.classList.remove('compared'));
  updateCompareBar();
}

function updateCompareBar() {
  if (!compareBar) return;
  compareBar.classList.toggle('visible', compareList.length > 0);
  const el = compareBar.querySelector('.compare-items');
  if (el) el.innerHTML = compareList.map(i =>
    `<div class="compare-item">${i.name}<span class="compare-item-remove" onclick="removeCompare('${i.id}')">✕</span></div>`
  ).join('');
}

function initCompare() {
  document.querySelectorAll('[data-cmp-id]').forEach(btn => {
    btn.addEventListener('click', () => toggleCompare(btn, btn.dataset.cmpId, btn.dataset.cmpName));
  });
}

// ── Search tabs ───────────────────────────
function initSearchTabs() {
  document.querySelectorAll('.search-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.search-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const typeInput = document.getElementById('search-type');
      if (typeInput) typeInput.value = tab.dataset.type || '';
    });
  });
}

// ── Toast ─────────────────────────────────
function showToast(msg) {
  const t = document.createElement('div');
  t.style.cssText = 'position:fixed;bottom:80px;left:50%;transform:translateX(-50%);background:#111;color:#fff;padding:9px 20px;border-radius:24px;font-size:.78rem;font-weight:600;z-index:9999;box-shadow:0 4px 20px rgba(0,0,0,.3);pointer-events:none;white-space:nowrap;';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.style.opacity = '0', 2000);
  setTimeout(() => t.remove(), 2400);
}

// ── Init ──────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initFavorites();
  initCompare();
  initSearchTabs();
});
