from django.urls import path
from magicauth import views as magicauth_views


urlpatterns = [
    path('login/', magicauth_views.magic_link, name='magicauth-login'),
    path('email-sent/', magicauth_views.email_sent, name='magicauth-email-sent'),
    path('code/<str:key>/', magicauth_views.validate_token, name='magicauth-validate-token'),

]