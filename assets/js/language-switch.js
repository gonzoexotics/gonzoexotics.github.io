/* Only paired pages share query parameters and section IDs. No redirects or storage. */
(() => {
  const pairedLink = document.querySelector('.language-switch a[data-i18n-pair]');
  if (pairedLink) {
    const target = new URL(pairedLink.getAttribute('href'), window.location.origin);
    target.search = window.location.search;
    target.hash = window.location.hash;
    pairedLink.href = target.pathname + target.search + target.hash;
    window.addEventListener('hashchange', () => {
      target.hash = window.location.hash;
      pairedLink.href = target.pathname + target.search + target.hash;
    });
  }
  const fallback = document.querySelector('.language-switch details');
  if (fallback) {
    document.addEventListener('click', event => {
      if (!fallback.contains(event.target)) fallback.open = false;
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && fallback.open) {
        fallback.open = false;
        fallback.querySelector('summary').focus();
      }
    });
  }
})();
