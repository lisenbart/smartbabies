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
