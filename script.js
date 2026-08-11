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

document.getElementById('year').textContent = new Date().getFullYear();


// Prosty lightbox galerii
const lightbox=document.querySelector('.lightbox');
if(lightbox){const lbImg=lightbox.querySelector('img');document.querySelectorAll('[data-lightbox]').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();lbImg.src=a.href;lightbox.classList.add('open')}));lightbox.querySelector('button').addEventListener('click',()=>lightbox.classList.remove('open'));lightbox.addEventListener('click',e=>{if(e.target===lightbox)lightbox.classList.remove('open')});}
