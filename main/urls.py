from django.conf.urls import url
from . import views

app_name='main'

urlpatterns = [
url(r'^$',views.HomeView.as_view(), name='home'),
url(r'^search/$', views.SearchView.as_view(), name='search'),
url(r'^property-detail/$', views.PropertyDetail.as_view(), name='detail'),
]