(() => {
  'use strict';

  // Lightbox pro [data-zoom] obrázky
  const lb = document.getElementById('lightbox');
  if (lb) {
    const lbImg = document.getElementById('lightboxImg');
    const lbClose = lb.querySelector('.close');

    const open = (src, alt) => {
      lbImg.src = src;
      lbImg.alt = alt || '';
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
    };
    const close = () => {
      lb.classList.remove('open');
      document.body.style.overflow = '';
      setTimeout(() => { lbImg.src = ''; }, 250);
    };

    document.querySelectorAll('[data-zoom]').forEach(el => {
      el.addEventListener('click', (e) => {
        e.preventDefault();
        const img = el.tagName === 'IMG' ? el : el.querySelector('img');
        if (img) open(img.src, img.alt);
      });
    });

    lb.addEventListener('click', (e) => {
      if (e.target === lb || e.target === lbImg) close();
    });
    if (lbClose) lbClose.addEventListener('click', close);
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && lb.classList.contains('open')) close();
    });
  }

  // Filtry bytů na hlavní stránce (dispozice + status)
  const grid = document.getElementById('aptsGrid');
  const state = { disp: 'all', status: 'all' };

  const apply = () => {
    if (!grid) return;
    grid.querySelectorAll('.card-apt').forEach(card => {
      const disp = card.dataset.dispozice || '';
      const status = card.dataset.status || '';
      const dispOk = (state.disp === 'all' || disp.startsWith(state.disp));
      const statusOk = (state.status === 'all' || status === state.status);
      card.style.display = (dispOk && statusOk) ? '' : 'none';
    });
  };

  const setupFilter = (selector, key) => {
    const buttons = document.querySelectorAll(selector + ' button');
    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        state[key] = btn.dataset['filter' + key.charAt(0).toUpperCase() + key.slice(1)];
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        apply();
      });
    });
  };

  setupFilter('.apts .filter:not(.filter-status)', 'disp');
  setupFilter('.apts .filter-status', 'status');
})();