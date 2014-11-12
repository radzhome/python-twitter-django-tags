python-twitter-django-tags
==========================

Useful python-twitter template tags for use with python-twitter api in your django app

Installing it / adding it to your project:

1. Copy the templatetags folder to the desired django app inside your project
2. Ensure the appliation that you added the folder to is in your INSTALLED_APPS in your settings.py

3. Use the tags inside of your template:

Example Usage:
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
Make sure to use expand_tweet_urls before urlize_tweet_text


Example get_tweets() function that can be used in your view to retrieve tweets.

```python
import twitter
def get_tweets():
    """
    returns twitter feed with settings as described below, contains all related twitter settings
    """
    api = twitter.Api(consumer_key='7ZoKq116f8z35daiin5PoDyxc',
                      consumer_secret='snhQqEtA9BON4vEbSg6ZKsfAM0s51DmDoLw67CUArn0EaZlgJS',
                      access_token_key='44989254-bOXKvUmwxExhk1Mkn3ETVItJCY5Bo3KaLKeilVuJj',
                      access_token_secret='ugtpGQwHqrf3qI8JD2l0l31ETvA1jfKuAUZTMOuLPcyJR')

    return api.GetUserTimeline(screen_name='bakerinc', exclude_replies=True, include_rts=False)  # includes entities
```

Usage in your view:
```python
from your.utils.lib import get_tweets
context['tweets'] = get_tweets()
```
