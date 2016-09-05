from django.conf.urls import url
from . import views


app_name = 'certs'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create_ca/$', views.CertificateCreateCAView.as_view(), name='create_ca'),
    url(r'^create/$', views.CertificateCreateView.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # url(r'^test/$', views.get_name, name='test'),
]
