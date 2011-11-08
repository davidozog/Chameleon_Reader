from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'contents.views.display_books'),
    url(r'^(?P<book_name>[-A-Za-z0-9_]+)/?$',
        'contents.views.display_table_of_contents'),
    url(r'^(?P<book_name>[-A-Za-z0-9_]+)/(?P<article_title>[-A-Za-z0-9_]+)$',
        'contents.views.display_article'),
        # url(r'^tag/?$', 'contents.views.display_tag'),

)
