python-twitter-django-tags
==========================

Useful python-twitter template tags for use with python-twitter api in your django app


Example Usage:
``
<div class="block social-block social-twitter">
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
``

Make sure to use expand_tweet_urls before urlize_tweet_text
