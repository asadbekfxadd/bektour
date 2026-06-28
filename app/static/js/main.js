'use strict';

// ── Cursor ──────────────────────────────
const cur = document.getElementById('cur');
const curDot = document.getElementById('curDot');
const curRing = document.getElementById('curRing');
if (cur) {
  let mx=0,my=0,rx=0,ry=0;
  document.addEventListener('mousemove', e => { mx=e.clientX; my=e.clientY; curDot.style.left=mx+'px'; curDot.style.top=my+'px'; });
  function curLoop(){ rx+=(mx-rx)*.12; ry+=(my-ry)*.12; curRing.style.left=rx+'px'; curRing.style.top=ry+'px'; requestAnimationFrame(curLoop); }
  curLoop();
  document.querySelectorAll('a,button,[data-fav],[data-cmp],.calc-svc,.region-card,.vcard').forEach(el=>{
    el.addEventListener('mouseenter',()=>cur.classList.add('big'));
    el.addEventListener('mouseleave',()=>cur.classList.remove('big'));
  });
}

// ── Preloader ──────────────────────────
(function(){
  const pl=document.getElementById('preloader');
  const fill=document.getElementById('plFill');
  const pct=document.getElementById('plPct');
  if(!pl) return;
  let n=0;
  const iv=setInterval(()=>{
    n=Math.min(n+Math.random()*12+5,100);
    if(fill) fill.style.width=n+'%';
    if(pct) pct.textContent=Math.floor(n)+'%';
    if(n>=100){ clearInterval(iv); setTimeout(()=>pl.classList.add('out'),500); }
  },55);
  window.addEventListener('load',()=>{ n=100; setTimeout(()=>pl.classList.add('out'),700); });
})();

// ── Navbar ────────────────────────────
const header = document.getElementById('header');
const isHero = !!document.querySelector('.hero');
function syncHeader(){
  if(!header) return;
  const scrolled = window.scrollY > 60;
  header.classList.toggle('glass', scrolled || !isHero);
  header.classList.toggle('over', !scrolled && isHero);
}
syncHeader();
window.addEventListener('scroll', syncHeader, {passive:true});

// ── Burger ─────────────────────────────
const burger=document.getElementById('burger');
const nav=document.getElementById('nav');
if(burger&&nav){
  burger.addEventListener('click',()=>{
    const open=nav.classList.toggle('open');
    document.body.style.overflow=open?'hidden':'';
  });
}

// ── Reveal on scroll ───────────────────
const revObs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{ if(e.isIntersecting){e.target.classList.add('in');revObs.unobserve(e.target);} });
},{threshold:.08});
document.querySelectorAll('.reveal').forEach(el=>revObs.observe(el));

// ── Counters ────────────────────────────
function runCount(el){
  const end=parseInt(el.dataset.n||'0');
  const suf=el.dataset.s||'';
  let cur=0; const step=end/60;
  const iv=setInterval(()=>{ cur=Math.min(cur+step,end); el.textContent=Math.floor(cur).toLocaleString()+suf; if(cur>=end) clearInterval(iv); },16);
}
const cntObs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{ if(e.isIntersecting){e.target.querySelectorAll('[data-n]').forEach(runCount);cntObs.unobserve(e.target);} });
},{threshold:.3});
document.querySelectorAll('.stats-strip').forEach(s=>cntObs.observe(s));

// ── Trip Calculator ───────────────────
(function(){
  const nights_input = document.getElementById('calcNights');
  const guests_input = document.getElementById('calcGuests');
  const city_select  = document.getElementById('calcCity');
  const total_el     = document.getElementById('calcTotal');
  const breakdown_el = document.getElementById('calcBreakdown');
  if(!total_el) return;

  const PRICES = {
    hotel:   { base: 80,  label_en:'Hotel', label_ru:'Отель', label_uz:'Mehmonxona' },
    villa:   { base: 200, label_en:'Villa', label_ru:'Вилла', label_uz:'Villa' },
    car:     { base: 60,  label_en:'Car Rental', label_ru:'Аренда авто', label_uz:'Avtomobil ijarasi' },
    guide:   { base: 80,  label_en:'Private Guide', label_ru:'Гид', label_uz:'Gid' },
    transfer:{ base: 30,  label_en:'Transfer', label_ru:'Трансфер', label_uz:'Transfer' },
    visa:    { base: 50,  label_en:'Visa Support', label_ru:'Визовая поддержка', label_uz:'Viza yordam' },
    flight:  { base: 400, label_en:'Flight (avg)', label_ru:'Перелёт (ср)', label_uz:'Parvoz (o\'rt)' },
  };

  const CITY_MULT = {
    tashkent:1.0, samarkand:1.1, bukhara:1.0, khiva:0.9,
    namangan:0.85, andijan:0.85, nukus:0.9, termez:0.9,
    fergana:0.85, urgench:0.9, shahrisabz:0.95, jizzakh:0.85,
  };

  let selectedServices = new Set(['hotel','guide']);

  document.querySelectorAll('.calc-svc').forEach(btn=>{
    const svc = btn.dataset.svc;
    if(selectedServices.has(svc)) btn.classList.add('on');
    btn.addEventListener('click',()=>{
      if(selectedServices.has(svc)){
        if(selectedServices.size<=1) return;
        selectedServices.delete(svc);
        btn.classList.remove('on');
      } else {
        selectedServices.add(svc);
        btn.classList.add('on');
      }
      calcTotal();
    });
  });

  function calcTotal(){
    const nights = parseInt(nights_input?.value||'3');
    const guests = parseInt(guests_input?.value||'2');
    const city   = city_select?.value||'samarkand';
    const mult   = CITY_MULT[city]||1.0;
    const lang   = document.documentElement.lang||'en';

    let total = 0;
    let parts = [];

    selectedServices.forEach(svc=>{
      const p = PRICES[svc];
      if(!p) return;
      let cost = 0;
      if(svc==='hotel'||svc==='villa'||svc==='car'||svc==='guide') cost = p.base * nights * mult;
      else if(svc==='transfer') cost = p.base * 2;
      else if(svc==='visa') cost = p.base * guests;
      else if(svc==='flight') cost = p.base * guests;
      cost = Math.round(cost);
      total += cost;
      const label = lang==='ru'?p.label_ru: lang==='uz'?p.label_uz:p.label_en;
      parts.push(label+': $'+cost);
    });

    if(total_el) total_el.textContent = '$'+total.toLocaleString();
    if(breakdown_el) breakdown_el.textContent = parts.join(' · ');
  }

  document.querySelectorAll('#calcNights,#calcGuests,#calcCity').forEach(el=>{
    el&&el.addEventListener('change', calcTotal);
  });
  calcTotal();
})();

// ── Favorites ─────────────────────────
const FK='bt_favs_uz';
const getFavs=()=>{try{return JSON.parse(localStorage.getItem(FK)||'[]')}catch{return[]}};
function initFavs(){
  const favs=getFavs();
  document.querySelectorAll('[data-fav]').forEach(btn=>{
    if(favs.includes(btn.dataset.fav)) btn.classList.add('liked');
    btn.addEventListener('click',e=>{
      e.preventDefault();e.stopPropagation();
      const id=btn.dataset.fav; let list=getFavs();
      const i=list.indexOf(id);
      if(i===-1){list.push(id);btn.classList.add('liked');toast('❤️ Added to favorites');}
      else{list.splice(i,1);btn.classList.remove('liked');toast('Removed from favorites');}
      localStorage.setItem(FK,JSON.stringify(list));
    });
  });
}

// ── Compare ─────────────────────────────
let cmpList=[];
const cmpBar=document.getElementById('cmpBar');
function initCmp(){
  document.querySelectorAll('[data-cmp]').forEach(btn=>{
    btn.addEventListener('click',e=>{
      e.preventDefault();e.stopPropagation();
      const id=btn.dataset.cmp,name=btn.dataset.name||'';
      const i=cmpList.findIndex(x=>x.id===id);
      if(i===-1){
        if(cmpList.length>=3){toast('Max 3 to compare');return;}
        cmpList.push({id,name});btn.classList.add('liked');toast('Added to compare');
      } else {cmpList.splice(i,1);btn.classList.remove('liked');}
      updateCmpBar();
    });
  });
}
function updateCmpBar(){
  if(!cmpBar) return;
  cmpBar.classList.toggle('up',cmpList.length>0);
  const el=cmpBar.querySelector('.cmp-chips');
  if(el) el.innerHTML=cmpList.map(x=>`<div class="cmp-chip">${x.name}<span class="cmp-x" onclick="removeCmp('${x.id}')">✕</span></div>`).join('');
}
window.removeCmp=id=>{cmpList=cmpList.filter(x=>x.id!==id);document.querySelectorAll(`[data-cmp="${id}"]`).forEach(b=>b.classList.remove('liked'));updateCmpBar();};
window.clearCmp=()=>{cmpList=[];document.querySelectorAll('.liked[data-cmp]').forEach(b=>b.classList.remove('liked'));updateCmpBar();};

// ── FAQ ─────────────────────────────────
function initFAQ(){
  document.querySelectorAll('.faq-q').forEach(q=>{
    q.addEventListener('click',()=>{
      const item=q.parentElement,was=item.classList.contains('open');
      document.querySelectorAll('.faq-i').forEach(f=>f.classList.remove('open'));
      if(!was) item.classList.add('open');
    });
  });
}

// ── Toast ──────────────────────────────
function toast(msg,type='success'){
  let box=document.querySelector('.toast-wrap');
  if(!box){box=document.createElement('div');box.className='toast-wrap';document.body.appendChild(box);}
  const el=document.createElement('div');
  el.className=`toast toast-${type}`;
  el.innerHTML=`<i class="fa fa-${type==='success'?'check-circle':'exclamation-circle'}"></i>${msg}<button onclick="this.parentElement.remove()">×</button>`;
  box.appendChild(el);
  setTimeout(()=>{el.style.opacity='0';setTimeout(()=>el.remove(),300);},3500);
}
window.toast=toast;

// ── Flash auto-dismiss ──────────────────
document.querySelectorAll('.toast').forEach(t=>setTimeout(()=>t.remove(),5000));

// ── Search tabs ────────────────────────
document.querySelectorAll('.s-tab').forEach(tab=>{
  tab.addEventListener('click',()=>{
    document.querySelectorAll('.s-tab').forEach(t=>t.classList.remove('on'));
    tab.classList.add('on');
    const inp=document.getElementById('sType');
    if(inp) inp.value=tab.dataset.type||'';
  });
});

// ── Init ────────────────────────────────
document.addEventListener('DOMContentLoaded',()=>{initFavs();initCmp();initFAQ();});
