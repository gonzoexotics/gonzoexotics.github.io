const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();


// Prosty lightbox galerii
const lightbox=document.querySelector('.lightbox');
if(lightbox){const lbImg=lightbox.querySelector('img');document.querySelectorAll('[data-lightbox]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();lbImg.src=a.href;lightbox.classList.add('open')}));lightbox.querySelector('button').addEventListener('click',()=>lightbox.classList.remove('open'));lightbox.addEventListener('click',e=>{if(e.target===lightbox)lightbox.classList.remove('open')});}


// GA4 + prywatnosc: podstawowy Consent Mode.
// Google Analytics nie jest ladowany ani nie wysyla danych przed zgoda uzytkownika.
(() => {
  const GA_MEASUREMENT_ID = 'G-2ZTT829812';
  const CONSENT_KEY = 'gonzo_exotics_analytics_consent';
  const CONSENT_GRANTED = 'granted';
  const CONSENT_DENIED = 'denied';
  let analyticsStarted = false;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function gtag(){ window.dataLayer.push(arguments); };

  window.gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted'
  });

  const readConsent = () => {
    try { return window.localStorage.getItem(CONSENT_KEY); }
    catch (_) { return null; }
  };

  const writeConsent = (value) => {
    try { window.localStorage.setItem(CONSENT_KEY, value); }
    catch (_) {}
  };

  const deleteAnalyticsCookies = () => {
    document.cookie.split(';').forEach((item) => {
      const name = item.split('=')[0].trim();
      if (!/^_ga(?:_|$)|^_gid$|^_gat/.test(name)) return;
      document.cookie = `${name}=; Max-Age=0; path=/; SameSite=Lax`;
      document.cookie = `${name}=; Max-Age=0; path=/; domain=.gonzoexotics.pl; SameSite=Lax`;
      document.cookie = `${name}=; Max-Age=0; path=/; domain=gonzoexotics.pl; SameSite=Lax`;
    });
  };

  const startAnalytics = () => {
    if (analyticsStarted) return;
    analyticsStarted = true;

    window.gtag('consent', 'update', {
      analytics_storage: 'granted',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });

    window.gtag('js', new Date());
    window.gtag('config', GA_MEASUREMENT_ID, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_expires: 31536000,
      cookie_update: false
    });

    const gaScript = document.createElement('script');
    gaScript.async = true;
    gaScript.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(GA_MEASUREMENT_ID)}`;
    gaScript.dataset.gonzoAnalytics = 'true';
    document.head.appendChild(gaScript);
  };

  const removeConsentBanner = () => {
    document.querySelector('.analytics-consent')?.remove();
  };

  const showConsentBanner = () => {
    removeConsentBanner();

    const banner = document.createElement('section');
    banner.className = 'analytics-consent';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-modal', 'false');
    banner.setAttribute('aria-labelledby', 'analytics-consent-title');
    banner.innerHTML = `
      <div class="analytics-consent__copy">
        <strong id="analytics-consent-title">Prywatność i statystyki</strong>
        <p>Chcemy używać opcjonalnego Google Analytics 4, aby mierzyć ruch na stronie i pobrania darmowych materiałów. Analityka uruchomi się dopiero po Twojej zgodzie. Strona działa tak samo po odmowie. <a href="/polityka-prywatnosci.html">Polityka prywatności</a>.</p>
      </div>
      <div class="analytics-consent__actions">
        <button type="button" class="analytics-consent__button analytics-consent__button--secondary" data-analytics-reject>Nie zgadzam się</button>
        <button type="button" class="analytics-consent__button" data-analytics-accept>Akceptuję analitykę</button>
      </div>
    `;
    document.body.appendChild(banner);

    banner.querySelector('[data-analytics-accept]')?.addEventListener('click', () => {
      writeConsent(CONSENT_GRANTED);
      removeConsentBanner();
      startAnalytics();
    });

    banner.querySelector('[data-analytics-reject]')?.addEventListener('click', () => {
      const wasGranted = readConsent() === CONSENT_GRANTED || analyticsStarted;
      writeConsent(CONSENT_DENIED);
      window.gtag('consent', 'update', {
        analytics_storage: 'denied',
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied'
      });
      deleteAnalyticsCookies();
      removeConsentBanner();
      if (wasGranted) window.location.reload();
    });
  };

  const addPrivacySettingsLink = () => {
    const footerLinks = document.querySelector('.footer-links');
    if (!footerLinks || footerLinks.querySelector('[data-privacy-settings]')) return;

    const separator = document.createElement('span');
    separator.setAttribute('aria-hidden', 'true');
    separator.textContent = ' • ';

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'privacy-settings-button';
    button.dataset.privacySettings = 'true';
    button.textContent = 'Ustawienia prywatności';
    button.addEventListener('click', showConsentBanner);

    footerLinks.append(separator, button);
  };

  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[data-ebook-download]');
    if (!link || readConsent() !== CONSENT_GRANTED || !analyticsStarted) return;

    const fileUrl = new URL(link.getAttribute('href'), document.baseURI).href;
    let fileName = fileUrl.split('/').pop()?.split('?')[0] || '';
    try { fileName = decodeURIComponent(fileName); } catch (_) {}

    window.gtag('event', 'ebook_download', {
      ebook_name: link.dataset.ebookName || 'Corallus caninus — 4 filary dobrego środowiska',
      file_name: fileName,
      file_url: fileUrl,
      page_location: window.location.href,
      link_text: link.textContent.replace(/\s+/g, ' ').trim()
    });
  });

  addPrivacySettingsLink();

  const savedConsent = readConsent();
  if (savedConsent === CONSENT_GRANTED) {
    startAnalytics();
  } else if (savedConsent !== CONSENT_DENIED) {
    showConsentBanner();
  }
})();
