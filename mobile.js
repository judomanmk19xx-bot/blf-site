/* BLF Mobile Menu Toggle
   Adds hamburger menu + drawer + backdrop on mobile.
*/
(function() {
  'use strict';

  function init() {
    var btn = document.querySelector('.menu-toggle');
    var menu = document.querySelector('.mobile-menu');
    if (!btn || !menu) return;

    // Create backdrop if not exists
    var backdrop = document.querySelector('.mobile-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.className = 'mobile-backdrop';
      document.body.appendChild(backdrop);
    }

    function openMenu() {
      menu.classList.add('open');
      backdrop.classList.add('open');
      btn.classList.add('active');
      btn.setAttribute('aria-expanded', 'true');
      btn.setAttribute('aria-label', 'メニューを閉じる');
      document.body.style.overflow = 'hidden';
    }
    function closeMenu() {
      menu.classList.remove('open');
      backdrop.classList.remove('open');
      btn.classList.remove('active');
      btn.setAttribute('aria-expanded', 'false');
      btn.setAttribute('aria-label', 'メニューを開く');
      document.body.style.overflow = '';
    }
    function toggleMenu() {
      if (menu.classList.contains('open')) closeMenu();
      else openMenu();
    }

    // Toggle drawer
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      toggleMenu();
    });

    // Close drawer on backdrop click
    backdrop.addEventListener('click', closeMenu);

    // Close drawer when clicking a nav link (smooth scroll)
    var links = menu.querySelectorAll('a');
    links.forEach(function(link) {
      link.addEventListener('click', function() {
        closeMenu();
      });
    });

    // Close drawer when clicking anywhere else on document
    document.addEventListener('click', function(e) {
      if (!menu.classList.contains('open')) return;
      if (menu.contains(e.target) || btn.contains(e.target)) return;
      closeMenu();
    });

    // Close drawer on Escape key
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        closeMenu();
      }
    });

    // Close drawer if window resized to desktop
    var mediaQuery = window.matchMedia('(min-width: 901px)');
    function handleMQ(e) {
      if (e.matches && menu.classList.contains('open')) {
        closeMenu();
      }
    }
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleMQ);
    } else {
      mediaQuery.addListener(handleMQ);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
