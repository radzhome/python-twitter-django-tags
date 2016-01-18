python-twitter-django-tags
==========================

Useful [python-twitter](https://github.com/bear/python-twitter) template tags for use with [python-twitter](https://github.com/bear/python-twitter) api in your django app. Inspired by [django-twitter-tag](https://github.com/coagulant/django-twitter-tag) app. The same type of template integration was desired with [python-twitter](https://github.com/bear/python-twitter).

This code is very compact and easily integrates into your existing projects. As of now, I am not planning to package it as a portable reusable app.

================
Documentation
================

It's pretty straight forward. See [usage](#usage) below.

================
Dependencies
================

python-twitter: https://github.com/bear/python-twitter

django: https://github.com/django/django

================
Installation
================

Install this into one of your existing django projects simply by copying the 'templatetags' folder into one of your existing apps.

1. Install [python-twitter](https://github.com/bear/python-twitter) for your django project
2. Copy the templatetags folder to the desired django app inside your project
3. Ensure the appliation that you added the folder to is in your INSTALLED_APPS in your settings.py

4. Use the tags inside of your template:


================
Usage
================

Example usage, assuming that  `tweets` returns a user timeline (See Setting up your view on how to set this up). 
```html
<div class="block social-block social-twitter">
    {% load twitter_tags %}
    <h1>{% trans "Our Twitter" %}</h1>
    <ul>
        {% for tweet in tweets %}
        <li>
            <div class="tweet-meta">
                <a href="https://www.twitter.com/{{ tweet.user.screen_name }}/status/{{ tweet.id }}" target="_blank">
                    <img src="{{ tweet.user.profile_image_url }}" width="32" height="32" />
                    <h2>{{ tweet.user.name }}<br /><span>@{{ tweet.user.screen_name }} &middot; {{ tweet.created_at|twitter_date }}</span></h2>
                </a>
            </div>
            <p>{{ tweet|expand_tweet_urls|urlize_tweet_text|safe }}</p>
        </li>
        {% endfor %}

    </ul>
    <a href="#" class="btn btn-round btn-red">{% trans "Follow Us" %}</a>
</div>
```
NOTE: Make sure to use expand_tweet_urls before urlize_tweet_text


================
Setting up your View
================

Example get_tweets() function that can be used in your view to retrieve tweets.

```python
import twitter
def get_tweets():
    """
    returns twitter feed with settings as described below, contains all related twitter settings
    """
    api = twitter.Api(consumer_key='yourcustomerkey',
                      consumer_secret='customerkeysecret',
                      access_token_key='accesstokenkey',
                      access_token_secret='accesstokensecret')

    return api.GetUserTimeline(screen_name='twitter_screen_name', exclude_replies=True, include_rts=False)  # includes entities
```

Usage in your view:
```python
from your.utils.lib import get_tweets
context['tweets'] = get_tweets()
```

================
Getting the code
================
The code is hosted at https://github.com/radlws/python-twitter-django-tags. For python twitter, the code is hosted at https://github.com/bear/python-twitter
