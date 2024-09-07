from django.urls import path
from . import views 

app_name = 'accounts'

urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('forgotPassword/', views.forgotPassword, name="forgotPassword"),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('resetPassword/', views.resetPassword, name="resetPassword"),

    path('my_order/', views.my_order, name="my_order"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('order_detail/<int:order_id>/', views.order_detail, name="order_detail"),
    
]
