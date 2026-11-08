// Shared behaviour for every SnowBeltTech page: header, menus, reveal-on-scroll.
(function(){
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // header border once scrolled
  const top = document.getElementById('top');
  if (top) {
    const onScroll = () => top.classList.toggle('scrolled', window.scrollY > 8);
    onScroll(); window.addEventListener('scroll', onScroll, {passive:true});
  }

  // mobile menu
  const mb = document.querySelector('.menu-btn'), mm = document.getElementById('mobile-menu');
  if (mb && mm) {
    const close = () => { mm.classList.remove('open'); mb.setAttribute('aria-expanded', 'false'); mb.setAttribute('aria-label', 'Open menu'); };
    mb.addEventListener('click', () => {
      const open = mm.classList.toggle('open');
      mb.setAttribute('aria-expanded', String(open)); mb.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    mm.addEventListener('click', e => { if (e.target.closest('a')) close(); });
  }

  // desktop "Services" dropdown: click toggles, Escape / outside click closes
  document.querySelectorAll('.dd').forEach(dd => {
    const btn = dd.querySelector('.dd-btn');
    const set = open => { dd.classList.toggle('open', open); btn.setAttribute('aria-expanded', String(open)); };
    btn.addEventListener('click', e => { e.stopPropagation(); set(!dd.classList.contains('open')); });
    document.addEventListener('click', e => { if (!dd.contains(e.target)) set(false); });
    dd.addEventListener('keydown', e => { if (e.key === 'Escape') { set(false); btn.focus(); } });
    dd.addEventListener('focusout', e => { if (!dd.contains(e.relatedTarget)) set(false); });
  });

  // reveal on scroll
  const els = document.querySelectorAll('.reveal');
  if (reduce || !('IntersectionObserver' in window)) els.forEach(el => el.classList.add('in'));
  else {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), {rootMargin:'0px 0px -8% 0px'});
    els.forEach(el => io.observe(el));
  }
})();
