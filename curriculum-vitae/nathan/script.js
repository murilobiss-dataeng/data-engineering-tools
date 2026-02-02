/**
 * Curriculum Vitae - Site enxuto, comercial
 * PDF gerado a partir dos dados do JSON
 */
let resumeData = null;

async function loadResume() {
  try {
    const res = await fetch('resume.json');
    if (!res.ok) throw new Error('Arquivo não encontrado');
    resumeData = await res.json();
    render();
    initListeners();
  } catch (err) {
    console.error('Erro ao carregar currículo:', err);
    document.body.innerHTML = `
      <div style="padding: 3rem; text-align: center; font-family: system-ui;">
        <h1>Currículo não encontrado</h1>
        <p>Adicione <code>resume.json</code> nesta pasta.</p>
      </div>
    `;
  }
}

function render() {
  const d = resumeData;
  const contact = d.contact || {};

  // Nav
  document.getElementById('nav-name').textContent = (d.name || '').split(' ')[0] || 'CV';

  // Hero
  document.getElementById('hero-name').textContent = d.name || '';
  document.getElementById('hero-title').textContent = d.title || '';
  document.getElementById('hero-tagline').textContent = d.tagline || '';

  const statsEl = document.getElementById('hero-stats');
  statsEl.innerHTML = (d.stats || []).map(s =>
    `<div class="stat"><span class="stat-num">${s.number}</span><span class="stat-label">${s.label}</span></div>`
  ).join('');

  // Photo
  const photoEl = document.getElementById('profile-photo');
  const placeholder = document.getElementById('photo-placeholder');
  if (d.photo) {
    photoEl.src = d.photo;
    photoEl.alt = d.name;
    photoEl.style.display = '';
    placeholder.style.display = 'none';
  } else {
    photoEl.style.display = 'none';
    placeholder.style.display = 'flex';
  }

  // About
  document.getElementById('about-text').textContent = d.summary || '';

  // Experience
  const timelineEl = document.getElementById('timeline');
  timelineEl.innerHTML = (d.experience || []).map(exp => `
    <div class="timeline-item">
      <h3>${exp.role}</h3>
      <div class="company">${exp.company}</div>
      <div class="period">${exp.period}</div>
      <ul>
        ${(exp.achievements || []).map(a => `<li>${a}</li>`).join('')}
      </ul>
      ${exp.keywords?.length ? `<div class="tags">${exp.keywords.map(t => `<span class="tag">${t}</span>`).join('')}</div>` : ''}
    </div>
  `).join('');

  // Skills
  const skillsEl = document.getElementById('skills-grid');
  skillsEl.innerHTML = (d.skills || []).map(cat => `
    <div class="skill-category">
      <h4>${cat.category}</h4>
      <ul>
        ${(cat.items || []).map(s => `<li>${typeof s === 'string' ? s : s.name}</li>`).join('')}
      </ul>
    </div>
  `).join('');

  // Contact cards
  const waNum = String(contact.whatsapp || contact.phone || '').replace(/\D/g, '');
  const waUrl = waNum ? `https://wa.me/${waNum.startsWith('55') ? waNum : '55' + waNum}` : null;
  
  const cards = [];
  
  if (waUrl) {
    cards.push(`
      <a href="${waUrl}" target="_blank" rel="noopener" class="contact-card contact-whatsapp">
        <div class="contact-card-icon">
          <svg viewBox="0 0 24 24" width="28" height="28"><path fill="currentColor" d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
        </div>
        <div class="contact-card-content">
          <span class="contact-card-label">WhatsApp</span>
          <span class="contact-card-value">${contact.phone || 'Enviar mensagem'}</span>
        </div>
      </a>
    `);
  }
  
  if (contact.email) {
    cards.push(`
      <a href="mailto:${contact.email}" class="contact-card contact-email">
        <div class="contact-card-icon">
          <svg viewBox="0 0 24 24" width="28" height="28"><path fill="currentColor" d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
        </div>
        <div class="contact-card-content">
          <span class="contact-card-label">E-mail</span>
          <span class="contact-card-value">${contact.email}</span>
        </div>
      </a>
    `);
  }
  
  if (contact.linkedin) {
    cards.push(`
      <a href="${contact.linkedin}" target="_blank" rel="noopener" class="contact-card contact-linkedin">
        <div class="contact-card-icon">
          <svg viewBox="0 0 24 24" width="28" height="28"><path fill="currentColor" d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.32 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.79M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
        </div>
        <div class="contact-card-content">
          <span class="contact-card-label">LinkedIn</span>
          <span class="contact-card-value">Perfil profissional</span>
        </div>
      </a>
    `);
  }
  
  if (contact.address) {
    cards.push(`
      <div class="contact-card contact-location">
        <div class="contact-card-icon">
          <svg viewBox="0 0 24 24" width="28" height="28"><path fill="currentColor" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
        </div>
        <div class="contact-card-content">
          <span class="contact-card-label">Localização</span>
          <span class="contact-card-value">${contact.address}</span>
        </div>
      </div>
    `);
  }
  
  document.getElementById('contact-cards').innerHTML = cards.join('');

  const btnWaHero = document.getElementById('btn-whatsapp-hero');
  if (btnWaHero) {
    if (waUrl) { btnWaHero.href = waUrl; btnWaHero.style.display = 'inline-flex'; }
    else { btnWaHero.style.display = 'none'; }
  }

  // Footer
  document.getElementById('year').textContent = new Date().getFullYear();
  document.getElementById('footer-name').textContent = d.name || '';
}

function initListeners() {
  // Smooth scroll
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const href = a.getAttribute('href');
      if (href === '#') return;
      e.preventDefault();
      const el = document.getElementById(href.slice(1));
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    });
  });

  // Mobile menu
  document.querySelector('.nav-toggle')?.addEventListener('click', () => {
    document.querySelector('.nav-links')?.classList.toggle('open');
  });
}

document.addEventListener('DOMContentLoaded', loadResume);
