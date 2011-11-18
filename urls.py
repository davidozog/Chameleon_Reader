from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'GameReader.views.home', name='home'),
    url(r'^$', redirect_to, {'url': '/accounts/login/'}),
    # url(r'^GameReader/', include('GameReader.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    #(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/profile/', 'Chameleon_Reader.views.load_profile', name='load_profile'),
    url(r'^book_view/', 'Chameleon_Reader.views.load_book', name='book_view'),
    #url(r'^accounts/profile', redirect_to, {'url':'/notes/list'}),
    url(r'^notes/', include('notes.urls')),
    url(r'^account/', 'Chameleon_Reader.views.load_account', name='account_settings'),
    url(r'^book/', include('contents.urls')),

)
