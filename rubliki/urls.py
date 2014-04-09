from django.conf.urls import patterns, include, url
from rubliki_1.views import MainView
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rubliki.views.home', name='home'),
    # url(r'^rubliki/', include('rubliki.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^test/', MainView.as_view(), name='main')
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
