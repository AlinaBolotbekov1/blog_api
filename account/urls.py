from django.urls import path
from account.views import *

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view())
    

]

# password 1
# awznpqkjivobqbzy
# password 2
# grzlzxeongcccurt