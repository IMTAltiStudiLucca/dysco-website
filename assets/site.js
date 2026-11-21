// Menu highlight, header shadow, back-to-top button and gentle reveal of content. The page works without it.
(function () {
  var links = document.querySelectorAll('.nav a');
  var toggle = document.getElementById('menu-toggle');
  var header = document.querySelector('.site-header');
  var top = document.querySelector('.to-top');
  links.forEach(function (a) {
    a.addEventListener('click', function () { if (toggle) toggle.checked = false; });
  });
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle('scrolled', y > 8);
    if (top) top.classList.toggle('show', y > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (!('IntersectionObserver' in window)) return;

  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      links.forEach(function (a) {
        a.classList.toggle('active', a.getAttribute('href') === '#' + en.target.id);
      });
    });
  }, { rootMargin: '-35% 0px -60% 0px' });
  document.querySelectorAll('.page-section').forEach(function (s) { spy.observe(s); });

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var reveal = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); reveal.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  var groups = {};
  document.querySelectorAll('.page-head, .prose, .card, .person, .rows li, .figure, .spinoff').forEach(function (el) {
    if (el.getBoundingClientRect().top < window.innerHeight) return;
    var key = el.parentElement;
    groups[key] = (groups[key] || 0);
    el.style.transitionDelay = Math.min(groups[key]++ * 50, 250) + 'ms';
    el.classList.add('reveal');
    reveal.observe(el);
  });
})();
