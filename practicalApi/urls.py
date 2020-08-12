from django.conf.urls import url
from practicalApi import views

app_name = 'practicalApi'


urlpatterns = [
    url(r'^$', views.sign_up_page, name='sign_up_page'),
    url(r'^login/$', views.login_up_page, name='login_up_page'),
    url(r'^logout/$', views.logout_up_page, name='logout_up_page'),
    url(r'^homepage/$', views.home_page, name='home_page'),
    url(r'^register/$', views.UserSignUp.as_view(), name='UserSignUp'),
    url(r'^sendOtp/$', views.SendOtp.as_view(), name='SendOtp'),
    url(r'^validateOtp/$', views.ValidateOtp.as_view(), name='ValidateOtp'),
]