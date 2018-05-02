from django.conf.urls import url
from . import views

app_name='main'

urlpatterns = [
url(r'^$',views.HomeView.as_view(), name='home'),
url(r'^search/$', views.SearchView.as_view(), name='search'),
url(r'^property/(?P<slug>[-\w]+)$', views.PropertyDetail.as_view(), name='property_detail'),
url(r'^increase_stat', views.IncreaseStat.as_view(), name='increase_stat'),
url(r'^offer/$', views.StartNow.as_view(), name='start_now'),
url(r'^request/', views.getFeature, name='ajaxfeature'),
url(r'^recent_listing/$',views.recent, name='recent'),
url(r'^agent_list/$',views.AgentView.as_view(), name='agent_list'),

]