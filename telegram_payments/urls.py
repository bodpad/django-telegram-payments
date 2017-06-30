from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.main, name='dtbp_main'),
    url(r'^settings/$', views.settings, name='dtbp_settings'),
    url(r'^delete/$', views.delete, name='dtbp_delete'),
    url(r'^create/$', views.create, name='dtbp_create'),
    url(r'^webhook/([0-9]{9}:[a-zA-Z0-9]{35})/$', views.webhook, name='dtbp_webhook'),
]