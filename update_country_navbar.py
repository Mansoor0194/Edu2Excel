from pathlib import Path
import re

root = Path(r'c:\Users\Manu Mansoor\Desktop\Imigo - Copy')

nav_template = '''<div class="elementor-element elementor-element-0471456 e-con-full e-flex e-con e-child" data-id="0471456" data-element_type="container" data-e-type="container">
                        <div class="elementor-element elementor-element-f4b1d8d header-menu elementor-widget elementor-widget-ekit-nav-menu" data-id="f4b1d8d" data-element_type="widget" data-e-type="widget" data-settings="{&quot;ekit_we_effect_on&quot;:&quot;none&quot;}" data-widget_type="ekit-nav-menu.default">
                            <div class="elementor-widget-container">
                                <nav class="ekit-wid-con ekit_menu_responsive_tablet" data-hamburger-icon="icon icon-menu-11" data-hamburger-icon-type="icon" data-responsive-breakpoint="1024">
                                    <button class="elementskit-menu-hamburger elementskit-menu-toggler" type="button" aria-label="hamburger-icon">
                <i aria-hidden="true" class="ekit-menu-icon icon icon-menu-11"></i>            </button>
                                    <div id="ekit-megamenu-header-menu" class="elementskit-menu-container elementskit-menu-offcanvas-elements elementskit-navbar-nav-default ekit-nav-menu-one-page-no ekit-nav-dropdown-hover">
                                        <ul id="menu-header-menu" class="elementskit-navbar-nav elementskit-menu-po-center submenu-click-on-icon">
                                            <li id="menu-item-3854" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-home menu-item-3854 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="../../index.html" class="ekit-menu-nav-link">Home</a></li>
                                            <li id="menu-item-3856" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3856 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="../../about-us/index.html" class="ekit-menu-nav-link">About Us</a></li>
                                            <li id="menu-item-3863" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3863 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="../../services/index.html" class="ekit-menu-nav-link">Services</a></li>
                                            <li id="menu-item-3855" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3855 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="../../Esc/index.html" class="ekit-menu-nav-link">Esc</a></li>
                                            <li id="menu-item-3868" class="menu-item menu-item-type-custom menu-item-object-custom menu-item-has-children menu-item-3868 nav-item elementskit-dropdown-has relative_position elementskit-dropdown-menu-default_width elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="#" class="ekit-menu-nav-link ekit-menu-dropdown-toggle">Pages<i aria-hidden="true" class="icon icon-down-arrow1 elementskit-submenu-indicator"></i></a>
                                                <ul class="elementskit-dropdown elementskit-submenu-panel">
                                                    <li id="menu-item-3862" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3862 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="../../services/dependent-visa/index.html" class=" dropdown-item">Services Details</a></li>
                                                    <li id="menu-item-12393" class="menu-item menu-item-type-post_type_archive menu-item-object-awaiken-coaching menu-item-12393 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="../../coaching/index.html" class=" dropdown-item">Coaching</a></li>
                                                    <li id="menu-item-12395" class="menu-item menu-item-type-post_type_archive menu-item-object-awaiken-countries menu-item-12395 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="../../countries/index.html" class=" dropdown-item">Countries</a></li>
                                                    <li id="menu-item-12396" class="menu-item menu-item-type-post_type menu-item-object-awaiken-countries menu-item-12396 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="../../countries/{country}/index.html" class=" dropdown-item">Countries Details</a></li>
                                                    <li id="menu-item-3861" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3861 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="#" class=" dropdown-item">Our Team</a></li>
                                                    <li id="menu-item-3864" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3864 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="#" class=" dropdown-item">Team Details</a></li>
                                                    <li id="menu-item-10895" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-10895 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="#" class=" dropdown-item">FAQs</a></li>
                                                </ul>
                                            </li>
                                            <li id="menu-item-3858" class="menu-item menu-item-type-post_type menu-item-object-page menu-item-3858 nav-item elementskit-mobile-builder-content" data-vertical-menu="750px"><a href="../../contact-us/index.html" class="ekit-menu-nav-link">Contact Us</a></li>
                                        </ul>
                                        <div class="elementskit-nav-identity-panel"><button class="elementskit-menu-close elementskit-menu-toggler" type="button">X</button></div>
                                    </div>
                                    <div class="elementskit-menu-overlay elementskit-menu-offcanvas-elements elementskit-menu-toggler ekit-nav-menu--overlay"></div>
                                </nav>
                            </div>
                        </div>
                    </div>'''

pattern = re.compile(
    r'<div class="elementor-element elementor-element-0471456[^>]*>.*?<div class="elementor-element elementor-element-fa39a20[^>]*>',
    re.S,
)

patched = 0
for path in sorted(root.glob('countries/*/index.html')):
    country = path.parent.name
    text = path.read_text(encoding='utf-8')
    if pattern.search(text):
        new_block = nav_template.replace('{country}', country)
        new_text = pattern.sub(new_block + '\n\t\t\t\t\t\t\t\t\t\t\t', text, count=1)
        if new_text != text:
            path.write_text(new_text, encoding='utf-8')
            patched += 1
            print(f'Patched {path}')
    else:
        print(f'Pattern not found in {path}')
print(f'Done. Patched {patched} files.')
