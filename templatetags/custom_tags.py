import re
from django import template

from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
#from django.template import resolve_variable, NodeList
#from django.contrib.auth.models import Group

register = template.Library()

''' fix this so its exact match, not pattern'''


@register.filter()
def twitter_date(value):
    import datetime
    split_date = value.split()
    del split_date[0], split_date[-2]
    value = ' '.join(split_date)  # Fri Nov 07 17:57:59 +0000 2014 is the format
    return datetime.datetime.strptime(value, '%b %d %H:%M:%S %Y')


@register.filter()
def urlize_tweet_text(tweet):
    """ Turn #hashtag and @username in status text to Twitter hyperlinks,
        similar to the ``urlize()`` function in Django.
    """
    try:
        from urllib import quote
    except ImportError:
        from urllib.parse import quote
    hashtag_url = '<a href="https://twitter.com/search?q=%%23%s" target="_blank">#%s</a>'
    user_url = '<a href="https://twitter.com/%s" target="_blank">@%s</a>'
    text = tweet.text
    for hash in tweet.hashtags:
        text = text.replace('#%s' % hash.text, hashtag_url % (quote(hash.text.encode("utf-8")), hash.text))
    for mention in tweet.user_mentions:
        text = text.replace('@%s' % mention.screen_name, user_url % (quote(mention.screen_name), mention.screen_name))
    return text

@register.filter()
def expand_tweet_urls(tweet):
    """ Replace shortened URLs with long URLs in the twitter status
        Should be used before urlize_tweet
    """
    text = tweet.text
    urls = tweet.urls
    for url in urls:
        text = text.replace(url.url, '<a href="%s" target="_blank">%s</a>' % (url.expanded_url, url.url))
    tweet.SetText(text)
    return tweet

@register.filter()
def nbsp(value):
    nbsp_str = "&nbsp;".join(value.split(' '))  # accounts for all spaces
    nbsp_str = re.sub(r'(&nbsp;)(\w)', r' \2', nbsp_str)  # replace with space followed by group 2
    #nbsp_str = mark_safe(re.sub(r'(\w)(&nbsp;)', r'\1 ', nbsp_str))  # replace with group 1 followed by space
    return mark_safe(nbsp_str)

@register.filter  # 1|get_step_class:step
def get_step_class(value, arg):
    if value < arg:
        return 'complete'
    elif value == arg:
        return 'active'
    else:
        return ''

@register.filter
def divide(value, arg):
    return int(value) / int(arg)


@register.filter
def multiply(value, arg):
    return value * arg


@register.simple_tag
def max_date(*args):
    #usage in template: {% max_value date1 date2 %}
    dates = list(args)
    #cleaned_dates = list()
    cleaned_dates = [x for x in dates if x is not None and type(x) != str]
    if not cleaned_dates:
        return None
    return max(cleaned_dates) or None


@register.simple_tag
def active(request, pattern):  # {% active request location_status %}
    # usage:  {% active request alarms_home %}
    """ add active to a tag's class based on url path """
    import re

    try:
        if re.search(pattern, request.path):
            return 'active'
    except AttributeError:
        return 'error_request_template_processor'
    return ''



@register.filter
def getitem(item, string):
    return item.get(string, '')


''' group begins here'''
#from django import template


@register.filter
def phonenumber(value):

    if len(value) == 10:
        phone = '({0}){1}-{2}'.format(value[0:3], value[3:6], value[6:10])
    elif len(value) == 11:
        phone = '+{0}({1}){2}-{3}'.format(value[0], value[1:4], value[4:7], value[7:11])
    else:
        phone = value

    return phone

@register.filter
def get_range(value):
    """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
    """
    return range(value)


@register.filter  # used for pagination
def get_page_range(value):  # 0, 1 (pass 2)
    page_range = range(value)
    page_range.append(value)
    page_range.pop(0)
    return page_range



@register.filter
def subtract(value, arg):
    return value - arg


@register.simple_tag
def get_url_param_value(request, param):  # Check if get param exits in url & return its value
    #request.get_full_path()
    param_value = request.GET.get(param, None)
    return param_value


@register.filter
def get_magnific_popup(img_url):
    from django.templatetags.static import static
    url = static(img_url)
    return mark_safe("<a class='magnific-popup-img' href='{0}'><img src='{0}' class='media'></a>".format(url))



@register.simple_tag(takes_context=True)
def get_admin_change_button(context, model_object):

    if context['request'].user.is_superuser:

        from django.db.models import Model

        if not isinstance(model_object, Model):
            #raise template.TemplateSyntaxError, "'%s' argument must be a model-instance" % model_object
            return ''

        app_label = model_object._meta.app_label
        model_name = model_object._meta.module_name
        instance_id = model_object.pk

        return mark_safe("<a class='{1}' href='{0}'>Edit {2}</a>".format(
            reverse('admin:{0}_{1}_{2}'.format(app_label, model_name, 'change'), args=[instance_id]),
            "btn btn-gray btn-round admin-change-btn {0}-admin-change-btn".format(model_name),
            model_name.title()
        ))
    else:
        return ''

@register.filter
def get_error_class(value):
    """Checks the error list length to output the right class """
    if len(value):
        return 'error-input'
    else:
        return ''

