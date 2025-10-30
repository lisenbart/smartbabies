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
  var parallaxBg = document.getElementById('parallax-bg');
  
  // Parallax setup для мобільних
  var parallaxSpeed = 0.25; // Легкий ефект - фон рухається на 25% від швидкості скролу
  
  function isMobileView() {
    return window.innerWidth <= 820;
  }
  
  // Parallax effect function
  function updateParallax() {
    if (isMobileView() && parallaxBg) {
      var currentScroll = window.pageYOffset || window.scrollY || document.documentElement.scrollTop;
      var bgOffset = currentScroll * parallaxSpeed;
      
      console.log('Parallax update:', { currentScroll, bgOffset, isMobile: isMobileView() });
      
      // Використовуємо requestAnimationFrame для плавності на iOS
      requestAnimationFrame(function() {
        parallaxBg.style.transform = 'translate3d(0, ' + bgOffset + 'px, 0)';
        parallaxBg.style.webkitTransform = 'translate3d(0, ' + bgOffset + 'px, 0)';
        parallaxBg.style.willChange = 'transform';
        console.log('Parallax applied:', bgOffset + 'px');
      });
    } else {
      console.log('Parallax skipped:', { isMobile: isMobileView(), hasBg: !!parallaxBg });
    }
  }
  
  // Throttled scroll handler для кращої продуктивності на iOS
  var scrollTimeout;
  function handleScroll() {
    if (scrollTimeout) {
      return;
    }
    
    scrollTimeout = requestAnimationFrame(function() {
      var currentScroll = window.pageYOffset || window.scrollY || document.documentElement.scrollTop;
      
      // Header background change
      if (currentScroll > 100) {
        header.style.background = 'rgba(11,18,32,.95)';
      } else {
        header.style.background = 'rgba(11,18,32,.6)';
      }
      
      // Parallax effect
      updateParallax();
      
      scrollTimeout = null;
    });
  }
  
  window.addEventListener('scroll', handleScroll, { passive: true });
  
  // Intersection Observer для підсвітки блоків при потраплянні в центр екрану
  function initCardObserver() {
    if (isMobileView()) {
      var cards = document.querySelectorAll('.card');
      console.log('Initializing card observer:', { cardsCount: cards.length, isMobile: isMobileView() });
      
      if (cards.length > 0 && 'IntersectionObserver' in window) {
        var observerOptions = {
          root: null,
          rootMargin: '-25% 0px -25% 0px', // Зона центру 50% екрану
          threshold: [0, 0.5, 1.0]
        };
        
        var observer = new IntersectionObserver(function(entries) {
          entries.forEach(function(entry) {
            console.log('Card intersection:', { 
              target: entry.target.textContent.substring(0, 30), 
              isIntersecting: entry.isIntersecting,
              ratio: entry.intersectionRatio 
            });
            
            if (entry.isIntersecting) {
              entry.target.classList.add('card-in-center');
              console.log('Card highlighted');
            } else {
              entry.target.classList.remove('card-in-center');
              console.log('Card unhighlighted');
            }
          });
        }, observerOptions);
        
        cards.forEach(function(card) {
          observer.observe(card);
        });
        
        console.log('Card observer initialized for', cards.length, 'cards');
      } else {
        console.log('IntersectionObserver not supported or no cards found');
      }
    } else {
      console.log('Not mobile view, skipping card observer');
    }
  }
  
  // Альтернативний підхід для iOS - scroll-based highlighting
  function initScrollBasedHighlighting() {
    if (isMobileView()) {
      var cards = document.querySelectorAll('.card');
      console.log('Initializing scroll-based highlighting for', cards.length, 'cards');
      
      function checkCardsInCenter() {
        var viewportHeight = window.innerHeight;
        var centerY = viewportHeight / 2;
        
        cards.forEach(function(card) {
          var rect = card.getBoundingClientRect();
          var cardCenterY = rect.top + rect.height / 2;
          var distanceFromCenter = Math.abs(cardCenterY - centerY);
          var isInCenter = distanceFromCenter < 200 && rect.top < viewportHeight && rect.bottom > 0;
          
          if (isInCenter) {
            if (!card.classList.contains('card-in-center')) {
              card.classList.add('card-in-center');
              console.log('Card highlighted via scroll:', card.textContent.substring(0, 30));
            }
          } else {
            if (card.classList.contains('card-in-center')) {
              card.classList.remove('card-in-center');
              console.log('Card unhighlighted via scroll:', card.textContent.substring(0, 30));
            }
          }
        });
      }
      
      // Перевіряємо при скролі
      window.addEventListener('scroll', checkCardsInCenter, { passive: true });
      
      // Перевіряємо при завантаженні
      checkCardsInCenter();
    }
  }
  
  // Ініціалізуємо observer
  initCardObserver();
  
  // Додатково для iOS - scroll-based підхід
  if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
    initScrollBasedHighlighting();
  }
  
  // Обробка resize для оновлення при зміні розміру екрану
  window.addEventListener('resize', function() {
    updateParallax();
    initCardObserver(); // Переініціалізуємо observer при зміні розміру
    if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
      initScrollBasedHighlighting();
    }
  }, { passive: true });
  
  // Початкова ініціалізація
  updateParallax();
  
  // Додаткова перевірка для iOS
  if (/iPad|iPhone|iPod/.test(navigator.userAgent)) {
    console.log('iOS detected, initializing mobile features');
    
    // Множинні спроби ініціалізації для iOS
    setTimeout(function() {
      updateParallax();
      initCardObserver();
    }, 100);
    
    setTimeout(function() {
      updateParallax();
      initCardObserver();
    }, 500);
    
    setTimeout(function() {
      updateParallax();
      initCardObserver();
    }, 1000);
    
    // Додаткова перевірка при завантаженні
    window.addEventListener('load', function() {
      updateParallax();
      initCardObserver();
    });
  }
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
