from django.conf.urls import url
from .views.api import (SignUp, SignIn, EmailCheckView, 
                       ForgotPasswordView, AccountActivationView,
                       ValidateOTPView, ResetPasswordView, ProfileDetailView,
                       ChangePasswordView, EditProfileView, SignOutView, 
                       AddShippingAddress, FbLoginSignup)

urlpatterns = [
    url(r'^register/$', SignUp.as_view(), name="user_register"),
    url(r'^signin/$', SignIn.as_view(), name="user_signin"),
    url(r'^email-check/$', EmailCheckView.as_view(), name="email_check"),
    url(r'^forgot-password/$', ForgotPasswordView.as_view(), name="forgot_password"),
    url(r'^activate-account/$', AccountActivationView.as_view(), name="activate_account"),
    url(r'^validate-otp/$', ValidateOTPView.as_view(), name="validate_otp"),
    url(r'^password-reset/$', ResetPasswordView.as_view(), name="password-reset"),
    url(r'^change-password/$', ChangePasswordView.as_view(),
        name="change-password"),
    url(r'^profile-detail/$', ProfileDetailView.as_view(), name="profile-detail"),
    url(r'^edit-profile/$', EditProfileView.as_view(), name="edit-profile"),
    url(r'^signout/$', SignOutView.as_view(), name="sign-out"),
    url(r'^add-address/$', AddShippingAddress.as_view(), name="add-address"),
    url(r'^fblogin/$', FbLoginSignup.as_view(), name="fb-login")
    # url(r'^get-social-user', GetSocialUser.as_view(), name="get-social-user"),
    # url(r'^social_sign_up/$', views.SocialSignUp.as_view(), name="social_sign_up"),
]

