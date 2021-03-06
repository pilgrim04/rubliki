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

    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^registration/$', RegistrationView.as_view(), name='registration'),

    url(r'^cabinet/$', CabinetView.as_view(), name='cabinet'),

    url(r'^my_billings/$', BillingView.as_view(), name='billing'),
    url(r'^my_billings/add_new_billing/$', AddBillingView.as_view(), name='add-new-billing'),

    url(r'^my_categories/$', CategoryView.as_view(), name='category'),
    url(r'^my_categories/add_new_category/$', AddCategoryView.as_view(), name='add-new-category'),
    #
    # url(r'^my_categories/(?P<category_name>\w+)/my_subcategories/$', SubcategoryView.as_view(), name='subcategory'),
    # url(r'^my_categories/(?P<category_name>\w+)/my_subcategories/add_new_subcategory/$', AddSubcategoryView.as_view(), name='add-new-subcategory'),

    url(r'^transaction/$', TransactionView.as_view(), name='transaction'),
    url(r'^transaction/transfer/$', TransferView.as_view(), name='transfer'),

    url(r'^statement/$', StatementView.as_view(), name='statement'),
    url(r'^grafiki/$', GrafikiView.as_view(), name='grafiki'),

    url(r'^edit/$', EditProfileView.as_view(), name='edit'),


    # url(r'^register_ok/', RegistrationCompleteView.as_view(), name='register_ok'),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
