import requests
from bs4 import BeautifulSoup, Comment
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def pars_page(url, templ):

    page = requests.get(url)

    soup_page = BeautifulSoup(page.content, 'html.parser')
    page = str(case_teml(templ, soup_page))

    return mark_safe(page)


def case_teml(templ, soup_page):
    if templ == 'wikipedia':
        return tmpl4_wikipedia(soup_page)
    elif templ == 'only text':
        return tmpl1_text_from_html(soup_page)
    elif templ == 'only image':
        return tmpl2_img_from_html(soup_page)
    elif templ == 'original':
        return tmpl3_original(soup_page)
    elif templ == 'stackoverflow':
        return tmpl5_stackoverflow(soup_page)
    elif templ == 'template':
        return tmpl6_without_text(soup_page)
    elif templ == 'bbc':
        return tmpl7_bbc(soup_page)
    elif templ == 'habr':
        return tmpl8_habr(soup_page)




def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def tmpl1_text_from_html(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def tmpl2_img_from_html(soup):
    images = ''
    for img in soup.findAll('img'):
        images += '<img src="' + img.get('src') + '">'
    return images

def tmpl3_original(soup_page):
    return str(soup_page)

def tmpl4_wikipedia(soup_page):
    for div in soup_page.find_all("div", { 'id':
                                               ['mw-panel',
                                                'siteSub',
                                                'jump-to-nav',
                                                'toc']
                                           }):
        div.decompose()

    for div in soup_page.find_all("td", {'class': 'infobox-below' }):
        div.decompose()

    for div in soup_page.find_all("sup", {'class': 'reference' }):
        div.decompose()

    for div in soup_page.find_all("span", {'class': 'mw-editsection' }):
        div.decompose()

    for div in soup_page.find_all("div", {'class': 'hatnote noprint dabhide' }):
        div.decompose()

    for div in soup_page.find_all("a", {'class': 'mw-jump-link' }):
        div.decompose()

    for a in soup_page.findAll('a'):
        a.replaceWithChildren()

    return soup_page


def tmpl5_stackoverflow(soup_page):
    for s in soup_page.select('header'):
        s.extract()

    for s in soup_page.select('footer'):
        s.extract()

    for s in soup_page.select('form'):
        s.extract()

    for div in soup_page.find_all("div", {'class': ['py24 bg-black-750 fc-black-200 sm:pt24 sm:pb24 ps-relative js-dismissable-hero',
                                                    'left-sidebar js-pinned-left-sidebar ps-relative',
                                                    'ml12 aside-cta grid--cell print:d-none sm:ml0 sm:mb12 sm:order-first sm:as-end',
                                                    'show-votes',
                                                    'no-answers',
                                                    'post-layout--right js-post-comments-component',
                                                    'mt16 grid gs8 gsy fw-wrap jc-end ai-start pt4 mb16',
                                                    'grid s-btn-group js-filter-btn',
                                                    'grid fw-wrap ai-start jc-end gs8 gsy',
                                                    ] }):
        div.decompose()

    for div in soup_page.find_all("h2", {'class': ['bottom-notice'] }):
        div.decompose()

    for div in soup_page.find_all("aside", {'class': ['s-notice s-notice__info js-post-notice mb16']}):
        div.decompose()

    return soup_page


def tmpl6_without_text(soup_page):
    page = str(soup_page)
    newpage = ''

    ch = list(page)
    dev = True


    for c in ch:
        if c == '<':
            dev = True
        elif c == '>':
            dev = False
            newpage+=c

        if dev:
            newpage+=c
    print(str(newpage))
    return newpage


def tmpl7_bbc(soup_page):
    for s in soup_page.select('section'):
        s.extract()

    for s in soup_page.select('header'):
        s.extract()

    for s in soup_page.select('footer'):
        s.extract()

    return soup_page


def tmpl8_habr(soup_page):
    for div in soup_page.find_all("div", { 'class':
                                               ['layout__row layout__row_services',
                                                'layout__row layout__row_navbar',
                                                'page-header_bordered page-header_tall',
                                                'layout__row layout__row_navbar',
                                                'sidebar',
                                                'post-additionals post-additionals_company',
                                                'default-block default-block_content',
                                                'promo-block promo-block_vacancies',
                                                'comments-section',
                                                'layout__row layout__row_promo-blocks',
                                                'layout__row layout__row_footer-links',
                                                'layout__row layout__row_footer']
                                           }):
        div.decompose()

    for div in soup_page.find_all("a", {'class': ['layout__elevator']}):
        div.decompose()

    return soup_page