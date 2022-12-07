
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name= 'home'), 
    path('course/<str:slug>',views.course,name ='course'),
    path('login/',views.signin,name='login'),
    path('signup/',views.register,name = 'register'),
    path('token_send/',views.token_send,name = 'tokensend'),
    path('success/',views.success,name = 'success'),
    path('verify/<auth_token>',views.verify,name = 'verify'),
    path('error/',views.error,name = 'error'),
    path('logout/',views.user_logout,name='logout'),
    path('logout/',views.user_logout,name = 'logout'),
    path('watchlater/',views.watchlater,name = 'readlater'),
    path('delete/<pk>/',views.delete_watchlater,name = 'delete')
]
