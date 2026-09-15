/* BLF Mobile Menu Toggle
   Adds hamburger menu + drawer on mobile.
   Works on all 21 pages with <button class="menu-toggle">
*/
(function() {
  'use strict';

  function init() {
    var btn = document.querySelector('.menu-toggle');
    var menu = document.querySelector('.mobile-menu');
    if (!btn || !menu) return;

    // Toggle drawer
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      var isOpen = menu.classList.toggle('open');
      btn.classList.toggle('active', isOpen);
      btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      btn.setAttribute('aria-label', isOpen ? 'メニューを閉じる' : 'メニューを開く');
    });

    // Close drawer when clicking a nav link (smooth scroll stays on page)
    var links = menu.querySelectorAll('a[href^="#"]');
    links.forEach(function(link) {
      link.addEventListener('click', function() {
        menu.classList.remove('open');
        btn.classList.remove('active');
        btn.setAttribute('aria-expanded', 'false');
      });
    });

    // Close drawer when clicking outside
    document.addEventListener('click', function(e) {
      if (!menu.classList.contains('open')) return;
      if (menu.contains(e.target) || btn.contains(e.target)) return;
      menu.classList.remove('open');
      btn.classList.remove('active');
      btn.setAttribute('aria-expanded', 'false');
    });

    // Close on Escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        menu.classList.remove('open');
        btn.classList.remove('active');
        btn.setAttribute('aria-expanded', 'false');
      }
    });

    // Close drawer if window resized to desktop
    var mediaQuery = window.matchMedia('(min-width: 901px)');
    function handleMQ(e) {
      if (e.matches && menu.classList.contains('open')) {
        menu.classList.remove('open');
        btn.classList.remove('active');
        btn.setAttribute('aria-expanded', 'false');
      }
    }
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleMQ);
    } else {
      // fallback for old browsers
      mediaQuery.addListener(handleMQ);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
