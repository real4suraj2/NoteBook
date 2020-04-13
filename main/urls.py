from django.urls import path,include
from django.conf.urls import url
from django.views.generic import TemplateView
from . import views
app_name = "main"

urlpatterns = [
    path('', views.homepage, name = "homepage"),
    path('register/',views.register,name = 'register'),
    path('logout/',views.logout_request,name = 'logout'),
    path('login/',views.login_request,name= 'login'),
    path('account/',views.account,name='account'),
    path('account/edit/', views.edit_profile, name='edit_profile'),
	path('change_password/', views.change_password, name='change_password'),
	path('activate/<uidb64>/<token>/',views.activate,name='activate'),
	path('search/',views.search,name='search'),
	path('send_push/', views.send_push,name='send_push'),
	path('push-notifications/',views.push_notifications,name='push_notifications'),
    path('sw.js', TemplateView.as_view(template_name='sw.js', content_type='application/x-javascript')),
    path('<single_slug>/',views.single_slug,name= 'single_slug'),
	]
