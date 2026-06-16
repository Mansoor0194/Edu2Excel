const fs = require('fs');
const path = require('path');

const countries = [
  ['australia', 'Australia'],
  ['austria', 'Austria'],
  ['belgium', 'Belgium'],
  ['bulgaria', 'Bulgaria'],
  ['canada', 'Canada'],
  ['croatia', 'Croatia'],
  ['czech-republic', 'Czech Republic'],
  ['denmark', 'Denmark'],
  ['estonia', 'Estonia'],
  ['finland', 'Finland'],
  ['france', 'France'],
  ['germany', 'Germany'],
  ['greece', 'Greece'],
  ['hungary', 'Hungary'],
  ['iceland', 'Iceland'],
  ['ireland', 'Ireland'],
  ['italy', 'Italy'],
  ['latvia', 'Latvia'],
  ['liechtenstein', 'Liechtenstein'],
  ['lithuania', 'Lithuania'],
  ['luxembourg', 'Luxembourg'],
  ['malta', 'Malta'],
  ['netherlands', 'Netherlands'],
  ['newzealand', 'New Zealand'],
  ['norway', 'Norway'],
  ['poland', 'Poland'],
  ['portugal', 'Portugal'],
  ['romania', 'Romania'],
  ['slovakia', 'Slovakia'],
  ['slovenia', 'Slovenia'],
  ['spain', 'Spain'],
  ['sweden', 'Sweden'],
  ['switzerland', 'Switzerland'],
  ['uk', 'UK'],
  ['usa', 'USA'],
];

const services = [
  ['student-visa', 'Student Visa'],
  ['dependent-visa', 'Dependent Visa'],
  ['work-permit', 'Work Permit'],
  ['pr-visa', 'PR Visa'],
  ['visit-visa', 'Visit Visa'],
  ['business-visa', 'Business Visa'],
  ['travel-and-tourism', 'Travel and Tourism'],
  ['educational-loan', 'Educational Loan'],
  ['insurance', 'Insurance'],
  ['sim-cards', 'SIM Cards'],
  ['forex', 'Forex'],
  ['accommodation', 'Accommodation'],
  ['air-ticket-booking', 'Air Ticket Booking'],
];

function walk(dir, callback) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules' || entry.name === '.git') continue;
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(fullPath, callback);
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      callback(fullPath);
    }
  }
}

function prefixFor(filePath) {
  const relDir = path.relative(process.cwd(), path.dirname(filePath));
  if (!relDir) return './';
  const depth = relDir.split(path.sep).length;
  return '../'.repeat(depth);
}

function isActive(filePath, section) {
  const rel = path.relative(process.cwd(), filePath).replace(/\\/g, '/');
  if (section === 'home') return rel === 'index.html';
  return rel === `${section}/index.html` || rel.startsWith(`${section}/`);
}

function menuHtml(filePath) {
  const prefix = prefixFor(filePath);
  const active = {
    home: isActive(filePath, 'home'),
    about: isActive(filePath, 'about-us'),
    services: isActive(filePath, 'services'),
    esc: isActive(filePath, 'Esc'),
    countries: isActive(filePath, 'countries'),
    contact: isActive(filePath, 'contact-us'),
  };

  const activeLi = (on, extra = '') => `${extra}${on ? ' current-menu-item current_page_item active' : ''}`;
  const activeLink = (on, extra = '') => `${extra}${on ? ' active' : ''}`;

  const countryItems = countries.map(([slug, label], index) => {
    const currentCountry = path.relative(process.cwd(), filePath).replace(/\\/g, '/') === `countries/${slug}/index.html`;
    return `<li id="menu-item-country-${index + 1}" class="menu-item menu-item-type-post_type menu-item-object-awaiken-countries nav-item elementskit-mobile-builder-content${currentCountry ? ' active' : ''}" data-vertical-menu="750px"><a href="${prefix}countries/${slug}/index.html" class=" dropdown-item${currentCountry ? ' active' : ''}">${label}</a></li>`;
  }).join('\n');

  const serviceItems = services.map(([slug, label], index) => {
    const currentService = path.relative(process.cwd(), filePath).replace(/\\/g, '/') === `services/${slug}/index.html`;
    return `<li id="menu-item-service-${index + 1}" class="menu-item menu-item-type-post_type menu-item-object-page nav-item elementskit-mobile-builder-content${currentService ? ' active' : ''}" data-vertical-menu="750px"><a href="${prefix}services/${slug}/index.html" class=" dropdown-item${currentService ? ' active' : ''}">${label}</a></li>`;
  }).join('\n');

  return `<ul id="menu-header-menu" class="elementskit-navbar-nav elementskit-menu-po-center submenu-click-on-icon">
<li id="menu-item-3854" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-home menu-item-3854 nav-item elementskit-mobile-builder-content${activeLi(active.home)}" data-vertical-menu="750px"><a href="${prefix}index.html" class="${activeLink(active.home, 'ekit-menu-nav-link')}">Home</a></li>
<li id="menu-item-3856" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3856 nav-item elementskit-mobile-builder-content${activeLi(active.about)}" data-vertical-menu="750px"><a href="${prefix}about-us/index.html" class="${activeLink(active.about, 'ekit-menu-nav-link')}">About Us</a></li>
<li id="menu-item-3863" class="menu-item menu-item-type-post_type_archive menu-item-object-page menu-item-has-children menu-item-3863 nav-item elementskit-dropdown-has relative_position elementskit-dropdown-menu-default_width elementskit-mobile-builder-content${activeLi(active.services)}" data-vertical-menu="750px"><a href="${prefix}services/index.html" class="${activeLink(active.services, 'ekit-menu-nav-link ekit-menu-dropdown-toggle')}">Services<i aria-hidden="true" class="icon icon-down-arrow1 elementskit-submenu-indicator"></i></a>
<ul class="elementskit-dropdown elementskit-submenu-panel edu-services-nav">
${serviceItems}
</ul>
</li>
<li id="menu-item-3855" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3855 nav-item elementskit-mobile-builder-content${activeLi(active.esc)}" data-vertical-menu="750px"><a href="${prefix}Esc/index.html" class="${activeLink(active.esc, 'ekit-menu-nav-link')}">Esc</a></li>
<li id="menu-item-countries" class="menu-item menu-item-type-post_type_archive menu-item-object-awaiken-countries menu-item-has-children nav-item elementskit-dropdown-has relative_position elementskit-dropdown-menu-default_width elementskit-mobile-builder-content${activeLi(active.countries)}" data-vertical-menu="750px"><a href="${prefix}countries/index.html" class="${activeLink(active.countries, 'ekit-menu-nav-link ekit-menu-dropdown-toggle')}">Countries<i aria-hidden="true" class="icon icon-down-arrow1 elementskit-submenu-indicator"></i></a>
<ul class="elementskit-dropdown elementskit-submenu-panel edu-countries-nav">
${countryItems}
</ul>
</li>
<li id="menu-item-3868" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-has-children menu-item-3868 nav-item elementskit-dropdown-has relative_position elementskit-dropdown-menu-default_width elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="#" class="ekit-menu-nav-link ekit-menu-dropdown-toggle">Pages<i aria-hidden="true" class="icon icon-down-arrow1 elementskit-submenu-indicator"></i></a>
<ul class="elementskit-dropdown elementskit-submenu-panel">
<li id="menu-item-12393" class="menu-item menu-item-type-post_type_archive menu-item-object-awaiken-coaching menu-item-12393 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="${prefix}coaching/index.html" class=" dropdown-item">Coaching</a></li>
<li id="menu-item-3861" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3861 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="${prefix}our-team/index.html" class=" dropdown-item">Our Team</a></li>
<li id="menu-item-3864" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3864 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="${prefix}our-team/nia-jex/index.html" class=" dropdown-item">Team Details</a></li>
<li id="menu-item-10895" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-10895 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="${prefix}faqs/index.html" class=" dropdown-item">FAQs</a></li>
</ul>
</li>
<li id="menu-item-3858" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3858 nav-item elementskit-mobile-builder-content${activeLi(active.contact)}" data-vertical-menu="750px"><a href="${prefix}contact-us/index.html" class="${activeLink(active.contact, 'ekit-menu-nav-link')}">Contact Us</a></li>
</ul>`;
}

const menuPattern = /<ul id="menu-header-menu"[^>]*>[\s\S]*?<\/ul>(\s*<div class="elementskit-nav-identity-panel")/;
let patched = 0;

walk('.', (filePath) => {
  const html = fs.readFileSync(filePath, 'utf8');
  const updated = html.replace(menuPattern, `${menuHtml(filePath)}$1`);
  if (updated !== html) {
    fs.writeFileSync(filePath, updated);
    patched += 1;
    console.log(`Updated ${filePath}`);
  }
});

console.log(`Done. Updated ${patched} files.`);
