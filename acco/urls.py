from django.conf.urls import url
from . import views

app_name='login'

urlpatterns = [
url(r'^login/$',views.LoginView.as_view(), name='login'),
url(r'^logout/$', views.user_logout, name='logout'),
]