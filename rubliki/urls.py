from django.conf.urls import patterns, include, url
from rubliki_1.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('rubliki_1.views',
    # Examples:
    # url(r'^$', 'rubliki.views.home', name='home'),
    # url(r'^rubliki/', include('rubliki.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^cabinet/', CabinetView.as_view(), name='cabinet')

    # url(r'^register_ok/', RegistrationCompleteView.as_view(), name='register_ok'),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
