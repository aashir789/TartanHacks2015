"""
Definition of urls for DjangoWebProject.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^favorites', 'app.views.favorites', name='favorites'),
    url(r'^retrieve', 'app.views.retrieve', name='retrieve'),
    url(r'^register', 'app.views.register', name='register'),
    url(r'^addfav', 'app.views.add_favorite', name='add'),
    url(r'^profile', 'app.views.user_profile', name='profile'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'app/login.html'},name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),
                       
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
