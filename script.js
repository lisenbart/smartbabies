// script.js
document.addEventListener('DOMContentLoaded', () => {
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear().toString();

  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const id = a.getAttribute('href'); if (!id || id === '#') return;
      const el = document.querySelector(id); if (!el) return;
      e.preventDefault(); el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  const setText = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
  setText('metricViews', '100k+');
  setText('metricWatch', '3m 20s');
  setText('metricRegions', 'UA, EU, US');

  const form = document.querySelector('.cta-form');
  form?.addEventListener('submit', e => {
    e.preventDefault();
    const email = form.querySelector('input[type="email"]').value.trim();
    if (!email) return;
    alert(`Thanks! We will reach out: ${email}`);
    form.reset();
  });
});
