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
  setText('metricViews', '120k+/mo');
  setText('metricWatch', '3m 20s');
  setText('metricRegions', 'UA · PL · US');

  // Live YouTube stats via Netlify Function (total views/subscribers)
  fetch('/.netlify/functions/get-youtube-stats')
    .then(function(res) { return res.ok ? res.json() : Promise.reject(res); })
    .then(function(json) {
      if (json && typeof json.viewCount === 'number') {
        var formatted = Intl.NumberFormat('en', { notation: 'compact' }).format(json.viewCount);
        setText('metricViews', formatted + ' total');
      }
      // Optionally show subs in watch metric area if available
      if (json && typeof json.subscriberCount === 'number') {
        var subs = Intl.NumberFormat('en', { notation: 'compact' }).format(json.subscriberCount);
        var watch = document.getElementById('metricWatch');
        if (watch) { watch.textContent = (watch.textContent + ' · ' + subs + ' subs').trim(); }
      }
    })
    .catch(function(){ /* silent fallback to static values */ });

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
  
  // Покращена мобільна функціональність
  function isMobile() {
    return window.innerWidth <= 820;
  }
  
  // Анімація карток при скролі
  function animateCardsOnScroll() {
    var cards = document.querySelectorAll('.card');
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }
      });
    }, { threshold: 0.1 });
    
    cards.forEach(function(card) {
      card.style.opacity = '0';
      card.style.transform = 'translateY(30px)';
      card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      observer.observe(card);
    });
  }
  
  // Ініціалізація анімацій
  if (isMobile()) {
    animateCardsOnScroll();
  }
  
  // Покращена навігація для мобільних
  var navLinks = document.querySelectorAll('.nav a');
  navLinks.forEach(function(link) {
    link.addEventListener('click', function() {
      // Додаємо візуальний фідбек
      this.style.transform = 'scale(0.95)';
      setTimeout(function() {
        link.style.transform = 'scale(1)';
      }, 150);
    });
  });
  
  // Оптимізація для мобільних пристроїв
  if (isMobile()) {
    // Додаємо touch events для кращої інтерактивності
    var cards = document.querySelectorAll('.card');
    cards.forEach(function(card) {
      card.addEventListener('touchstart', function() {
        this.style.transform = 'translateY(-4px) scale(1.02)';
      });
      
      card.addEventListener('touchend', function() {
        this.style.transform = 'translateY(0) scale(1)';
      });
    });
  }
});