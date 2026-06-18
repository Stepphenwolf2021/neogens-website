/* NEO GENS — interactions */
(function () {
  // Live clock (LA + local)
  const clockEl = document.querySelector('[data-clock]');
  if (clockEl) {
    const tick = () => {
      const t = new Date().toLocaleTimeString('en-GB', {
        hour: '2-digit', minute: '2-digit', timeZone: 'Asia/Bangkok'
      });
      clockEl.textContent = t + ' ICT';
    };
    tick();
    setInterval(tick, 1000 * 15);
  }

  // Mobile menu
  const btn = document.querySelector('.menu-btn');
  const nav = document.querySelector('.nav');
  if (btn && nav) {
    btn.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      btn.textContent = open ? 'Close' : 'Menu';
      document.body.style.overflow = open ? 'hidden' : '';
    });
    nav.querySelectorAll('a').forEach(a =>
      a.addEventListener('click', () => {
        nav.classList.remove('open');
        btn.textContent = 'Menu';
        document.body.style.overflow = '';
      })
    );
  }

  // Scroll reveal
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.rv').forEach(el => io.observe(el));
})();
