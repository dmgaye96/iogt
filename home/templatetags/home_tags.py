from django import template
from django.urls import translate_url
from wagtail.core.models import Locale, Site

from home.models import SectionIndexPage, Section, Article, FooterIndexPage, PageLinkPage, LocaleDetail
from iogt.settings.base import LANGUAGES

register = template.Library()


@register.inclusion_tag('home/tags/language_switcher.html', takes_context=True)
def language_switcher(context, page):
    if page:
        translations = []
        pages = page.get_translations(inclusive=True).select_related('locale', 'locale__locale_detail')
        for page in pages:
            try:
                if page.locale.locale_detail.is_active:
                    translations.append(page)
            except LocaleDetail.DoesNotExist:
                translations.append(page)
        context.update({
            'translations': translations,
        })


    default_locales = []
    locales = Locale.objects.select_related('locale_detail').all()
    for locale in locales:
        try:
            if locale.locale_detail.is_active:
                default_locales.append(locale)
        except LocaleDetail.DoesNotExist:
            default_locales.append(locale)
    context.update({'default_locales': default_locales})

    return context


@register.inclusion_tag('home/tags/previous-next-buttons.html')
def render_previous_next_buttons(page):
    return {
        'next_sibling': page.get_next_siblings().not_type(PageLinkPage).live().first(),
        'previous_sibling': page.get_prev_siblings().not_type(PageLinkPage).live().first()
    }


@register.inclusion_tag('home/tags/footer.html', takes_context=True)
def render_footer(context):
    return {
        'footers': FooterIndexPage.get_active_footers(),
        'request': context['request'],
    }


@register.inclusion_tag('home/tags/top_level_sections.html', takes_context=True)
def render_top_level_sections(context):
    return {
        'top_level_sections': SectionIndexPage.get_top_level_sections(),
        'request': context['request'],
    }


@register.inclusion_tag('home/tags/section_progress.html')
def render_user_progress(user_progress, show_count=True):
    return {
        **user_progress,
        'show_count': show_count,
    }


@register.inclusion_tag('home/tags/is_complete.html', takes_context=True)
def render_is_complete(context, page):
    if isinstance(page, (Section, Article)):
        context.update({
            'is_complete': page.is_complete(context['request'])
        })
    return context


@register.simple_tag
def locale_set(locale, url):
    for item in LANGUAGES:
        code = item[0]
        url = url.replace(f"/{code}/", "")
    return f'/{locale}/{url}'


@register.simple_tag
def translated_home_page_url(language_code):
    locale = Locale.objects.get(language_code=language_code)
    default_home_page = Site.objects.filter(is_default_site=True).first().root_page
    home_page = default_home_page.get_translation_or_none(locale)
    page = home_page or default_home_page
    return page.url


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    path = context['request'].path
    return translate_url(path, lang)


@register.simple_tag
def is_first_content(page, value):
    is_first_content = False
    if value == 0 and page.get_parent().specific.larger_image_for_top_page_in_list_as_in_v1:
        is_first_content = True

    return is_first_content


@register.simple_tag
def get_page(page):
    return page.get_page()


@register.inclusion_tag('wagtailadmin/shared/field_as_li.html')
def render_external_link_with_help_text(field):
    field.help_text = f'If you are linking back to a URL on your own IoGT site, be sure to remove the domain and ' \
                      f'everything before it. For example "http://sd.goodinternet.org/url/" should instead be "/url/".'

    return {'field': field, 'red_help_text': True}


@register.inclusion_tag('wagtailadmin/shared/field_as_li.html')
def render_redirect_from_with_help_text(field):
    field.help_text = f'A relative path to redirect from e.g. /en/youth. ' \
                      f'See "https://docs.wagtail.io/en/stable/editor_manual/managing_redirects.html" for more details.'

    return {'field': field, 'red_help_text': True}
