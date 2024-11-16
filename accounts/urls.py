from django.urls import path
from . import views
urlpatterns = [
path('login/', views.Signin.as_view(), name='login'),
path('logout/',views.Signout.as_view(),name='logout'),
path('signup/',views.Signup.as_view(),name='signup'),
path('profile/<int:pk>/', views.profile, name='profile'),



]
