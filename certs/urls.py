from django.conf.urls import url
from . import views


app_name = 'certs'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^show_ca/$', views.CAIndexView.as_view(), name='ca_index'),
    url(r'^create_ca/$', views.CreateCertificateCAView.as_view(), name='ca_create'),
    url(r'^create/$', views.CreateCertificateView.as_view(), name='create'),
    url(r'^show_ca/ca_(?P<pk>[0-9]+)/$', views.CADetailView.as_view(), name='ca_detail'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
]
