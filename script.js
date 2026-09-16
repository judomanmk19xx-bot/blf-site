// Language switcher - persist choice in localStorage, swap nav links
document.addEventListener('DOMContentLoaded', () => {
  const langLinks = document.querySelectorAll('.lang-switcher a');
  const langParam = new URLSearchParams(window.location.search).get('lang');
  const currentLang = langParam || localStorage.getItem('blf_lang') || 'JP';
  localStorage.setItem('blf_lang', currentLang);
  const langCode = {JP: 'ja', VN: 'vi', EN: 'en'}[currentLang] || 'ja';
  
  // Update <html lang>
  document.documentElement.lang = {JP: 'ja', VN: 'vi', EN: 'en'}[currentLang] || 'ja';
  
  // Mark active
  langLinks.forEach(link => {
    if (link.dataset.lang === currentLang) link.classList.add('active');
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const newLang = link.dataset.lang;
      const newCode = {JP: 'ja', VN: 'vi', EN: 'en'}[newLang];
      localStorage.setItem('blf_lang', newLang);
      const url = new URL(window.location);
      url.searchParams.set('lang', newLang);
      // Swap to lang-specific file if exists
      const path = window.location.pathname.replace(/(_ja|_vi|_en)?\.html$/, '_' + newCode + '.html');
      url.pathname = path;
      window.location.href = url.toString();
    });
  });
  
  // Lang files: vn.html + en.html (no _ja/_vi/_en suffix - file system uses .html directly)
  // No URL rewriting needed
});
// Contact form handler
document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.blf-contact-form');
  if (!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const data = {};
    for (const [k, v] of formData.entries()) data[k] = v;
    data.timestamp = new Date().toISOString();
    data.lang = form.dataset.lang;
    const submissions = JSON.parse(localStorage.getItem('blf_submissions') || '[]');
    submissions.push(data);
    localStorage.setItem('blf_submissions', JSON.stringify(submissions));
    // Static site (GitHub Pages): hand off to email client (spec 5.4 mailto fallback)
    const body = Object.entries(data)
      .filter(([k]) => !['timestamp', 'lang'].includes(k))
      .map(([k, v]) => `${k}: ${v}`).join('\n');
    const subject = `[BLF Website] ${data.company || data.name || 'Inquiry'} (${data.lang || 'ja'})`;
    window.location.href = 'mailto:dam.nt@baclieu-vegetables.vn?subject=' +
      encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    form.querySelectorAll('input, select, textarea, button').forEach(el => el.style.display = 'none');
    form.querySelector('.form-intro').style.display = 'none';
    form.querySelector('.form-thanks').style.display = 'block';
  });
});

// Lazy loading for images
document.addEventListener('DOMContentLoaded', () => {
  const images = document.querySelectorAll('img[data-src]');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          observer.unobserve(img);
        }
      });
    });
    images.forEach(img => observer.observe(img));
  } else {
    // Fallback: load all immediately
    images.forEach(img => {
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
    });
  }
});

// WebP detection + optimization
const supportsWebP = (() => {
  try {
    return document.createElement('canvas').toDataURL('image/webp').indexOf('webp') > -1;
  } catch (e) { return false; }
})();
window.blfSupportsWebP = supportsWebP;

// Hero slideshow - auto-rotate every 5s
document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('.hero-slideshow .slide');
  if (slides.length > 1) {
    let current = 0;
    setInterval(() => {
      slides[current].classList.remove('active');
      current = (current + 1) % slides.length;
      slides[current].classList.add('active');
    }, 5000);
  }
});
