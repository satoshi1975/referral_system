from django.urls import path
from . import views

urlpatterns = [
    path('api/authorize/', views.AuthorizePhoneView.as_view(),
         name='authorize'),       # get or create new user and
    # give him auth code
    path('api/verify/', views.CodeVerificationView.as_view(),
         name='verify'),  # verify user by his phone number
    # and auth code
    path('api/profile/', views.UserProfileView.as_view(),
         name='profile'),  # show current user
    path('api/enter_referral/', views.EnterReferralCodeView.as_view(),
         name='enter_referral'),  # send referral code
    path('api/user/<str:phone_number>/',
         views.UserProfileByPhoneNumber.as_view(),
         name='profile-by-phone'),  # show user by his phone number
    # get or create new user and
    path('send_phone/', views.auth_temp, name='send_phone'),
    # verify user by his phone number
    path('auth_code/', views.verify_auth_code, name='auth_code'),
    # verify user by his phone number
    path('send_invite/', views.send_invite, name='send_invite'),
    # and auth code
    path('home', views.home, name='home'),  # home page

]
