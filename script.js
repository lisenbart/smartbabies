document.addEventListener('DOMContentLoaded', function() {
  var yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear().toString();
  }

  var links = document.querySelectorAll('a[href^="#"]');
  links.forEach(function(anchor) {
    anchor.addEventListener('click', function(e) {
      var targetId = anchor.getAttribute('href');
      if (!targetId || targetId === '#') {
        return;
      }
      var target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        var headerOffset = 64;
        var elementPosition = target.getBoundingClientRect().top;
        var offsetPosition = elementPosition + window.pageYOffset - headerOffset;
        
        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth'
        });
      }
    });
  });

  function setText(id, value) {
    var el = document.getElementById(id);
    if (el) {
      el.textContent = value;
    }
  }
  setText('metricViews', '100k+');
  setText('metricWatch', '3m 20s');
  setText('metricRegions', 'UA, EU, US');

  var form = document.querySelector('.cta-form');
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      var emailInput = form.querySelector('input[type="email"]');
      if (emailInput) {
        var email = emailInput.value.trim();
        if (email) {
          alert('Thanks! We will reach out: ' + email);
          form.reset();
        }
      }
    });
  }
  
  var header = document.querySelector('.site-header');
  window.addEventListener('scroll', function() {
    var currentScroll = window.pageYOffset;
    if (currentScroll > 100) {
      header.style.background = 'rgba(11,18,32,.95)';
    } else {
      header.style.background = 'rgba(11,18,32,.6)';
    }
  });
});


/* Traction KPIs */
.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 8px; }
.kpi .kpi-value { font-size: 36px; font-weight: 900; color: var(--primary); margin-bottom: 6px; }
.kpi .kpi-label { color: var(--muted); }

/* Partner logos placeholders */
.partner-logos { display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; margin-top: 22px; }
.logo-pill {
  border: 2px dashed #2b3853; color: #9aa3b2; padding: 10px 14px; border-radius: 999px;
  filter: grayscale(100%) opacity(.9);
}

/* Roadmap timeline */
.timeline { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
.timeline .quarter { background: var(--card); border: 1px solid #1b253a; border-radius: 16px; padding: 18px; }
.timeline .quarter h3 { color: var(--secondary); font-size: 20px; margin-bottom: 8px; }
.timeline .milestones { margin: 0; padding-left: 18px; color: var(--muted); }
.timeline .milestones li::marker { color: var(--accent); }

/* CTA actions row */
.cta-actions { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 8px; }

@media (max-width: 980px) {
  .kpi-grid { grid-template-columns: 1fr; }
  .timeline { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 640px) {
  .timeline { grid-template-columns: 1fr; }
}
