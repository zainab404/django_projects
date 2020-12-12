from django.conf.urls import url
from basicapp import views
from django.urls import path

#TEMPLATE URLS
app_name = 'basicapp'

urlpatterns = [
    url(r'^register/',views.register,name='register'),
    url(r'^userlogin/$',views.user_login, name="user_login")
    ]
