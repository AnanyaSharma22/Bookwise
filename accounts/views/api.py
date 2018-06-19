from collections import OrderedDict
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
# from social.apps.django_app import load_strategy
# from social.apps.django_app.utils import load_backend
# from social.backends.oauth import BaseOAuth1, BaseOAuth2
# from social.exceptions import AuthAlreadyAssociated
from oauth2_provider.models import AccessToken
from ..models import Address
from bookstore.core.permissions import (PublicTokenAccessPermission,
                                       PrivateTokenAccessPermission,
                                       PublicPrivateTokenAccessPermission)
from accounts import message
from accounts.models import User, UserSecurityToken
from accounts.serializers import (RegisterUserSerialiser, LoginUserSerializer,
                                 EmailCheckSerializer, ForgotPasswordSerializer,
                                 AccountActivationSerializer, ValidateOTPSerializer,
                                 ResetPasswordSerializer, ProfileDetailSerializer,
                                 ChangePasswordSerializer, EditProfileSerializer,
                                 SignOutUserSerializer, ShippingAddressSerializer,
                                 FbsignupSerializer)
User = get_user_model()

class TwoRecordPagination(PageNumberPagination):
    ''' Two Record Pagination '''
    page_size = 20

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class SignUp(generics.UpdateAPIView):
    '''
    API for registering new user
    '''
    queryset = User.objects.all()
    serializer_class = RegisterUserSerialiser
    permission_classes = (PublicTokenAccessPermission, )

    def get_object(self):
        email = self.request.data['email']
        obj = get_user_model().objects.get(email__exact=email)
        return obj

    def update(self, request, *args, **kwargs):
        ''' update '''
        try:
            return super(SignUp, self).update(request, *args, **kwargs)
        except get_user_model().DoesNotExist:
            return Response({'message': message.USER_ACCOUNT_NOT_EXISTS}, status=settings.HTTP_API_ERROR)


class SignIn(generics.CreateAPIView):
    '''handling signin request'''
    queryset = User.objects.all()
    serializer_class = LoginUserSerializer
    permission_classes = (PublicTokenAccessPermission, )


class EmailCheckView(generics.views.APIView):
    queryset = User.objects.all()
    serializer_class = EmailCheckSerializer
    permission_classes = (PublicTokenAccessPermission, )

    def post(self, request, *args, **kwargs):
        try:
            user_instance = get_user_model().objects.get(email__iexact=request.data['email'])
            if not user_instance.is_active:
                return Response({'email': request.data['email']}, status.HTTP_200_OK)
            else:
                return Response({'email': message.ALREADY_REGISTER_USER}, settings.HTTP_API_ERROR)
        except get_user_model().DoesNotExist:
            return Response({'email': request.data['email']}, status.HTTP_200_OK)
    
    # def update(self, request, *args, **kwargs):
    #     try:
    #         # return super(EmailVerifyView, self).update(request, *args, **kwargs)
    #         #import pdb; pdb.set_trace()
    #         # self.obj = self.get_object()
    #         return Response(message.ALREADY_REGISTER_USER, status.HTTP_400_BAD_REQUEST)
    #     except get_user_model().DoesNotExist:
    #         user_instance = super(EmailVerifyView, self).update(request, *args, **kwargs)
    #         # user_instance.is_active = False
    #         # user_instance.save()
            # return Response(request.data['email'], status.HTTP_200_OK)



class AccountActivationView(generics.CreateAPIView):
    serializer_class = AccountActivationSerializer
    permission_classes = (PublicTokenAccessPermission, )


class ForgotPasswordView(generics.CreateAPIView):
    '''
        API for Forgot Password
    '''
    serializer_class = ForgotPasswordSerializer
    permission_classes = (PublicTokenAccessPermission, )


class ValidateOTPView(generics.UpdateAPIView):
    '''
        API for Validation of OTP
    '''
    serializer_class = ValidateOTPSerializer
    permission_classes = (PublicTokenAccessPermission, )

    def get_object(self):
        ''' Get Object '''
        return UserSecurityToken.objects.get(extras=self.request.data['email'],
                                             token=self.request.data['otp'])

    def update(self, request, *args, **kwargs):
        ''' update '''
        try:
            kwargs['partial'] = True
            return super(ValidateOTPView, self).update(request, *args, **kwargs)
        except UserSecurityToken.DoesNotExist:
            return Response({'detail': message.OTP_INVALID}, status=settings.HTTP_API_ERROR)


class ResetPasswordView(generics.UpdateAPIView):
    '''
        API for Reset Password
    '''
    serializer_class = ResetPasswordSerializer
    permission_classes = (PublicTokenAccessPermission, )

    def get_object(self):
        return UserSecurityToken.objects.get(extras=self.request.data['email'],
                                             token=self.request.data['otp'])

    def update(self, request, *args, **kwargs):
        try:
            return super(ResetPasswordView, self).update(request, *args, **kwargs)
        except UserSecurityToken.DoesNotExist:
            return Response({'message': message.OTP_INVALID}, status=settings.HTTP_API_ERROR)

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = (PrivateTokenAccessPermission, )

    def get_object(self):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": [message.OLD_PASSOWRD_MISMATCH]},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response([message.MESSAGE_CHANGE_PASSWORD_SUCCESS], status=status.HTTP_200_OK)
        return Response([serializer.errors], status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailView(generics.RetrieveAPIView):
    '''
      API for Profile Detail
    '''
    queryset = User.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = (PrivateTokenAccessPermission, )
 
    def get_object(self):
        # pk = self.request.query_params['id']
        # obj = get_user_model().objects.get(pk=pk)
        # return obj
        return self.request.user

class EditProfileView(generics.UpdateAPIView):
    '''
      API for Profile Detail
    '''
    queryset = User.objects.all()
    serializer_class = EditProfileSerializer
    permission_classes = (PrivateTokenAccessPermission, )
 
    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        return super(EditProfileView, self).update(request, *args, **kwargs)
        # except .DoesNotExist:
        #     return Response({'message': message.OTP_INVALID}, status=settings.HTTP_API_ERROR
        
class SignOutView(generics.UpdateAPIView):
    '''
    API for Expire Access Token to Sign out the User
    '''
    queryset = User.objects.all()
    serializer_class = SignOutUserSerializer
    permission_classes = (PrivateTokenAccessPermission, )

    def get_object(self):
        '''
        Get Object
        '''
        token = self.request.META['HTTP_AUTHORIZATION']
        token_type, token = token.split(' ')
        if token:
            try:
                access_token = AccessToken.objects.filter(token=token).get()
            except AccessToken.DoesNotExist:
                return None
        return access_token
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(SignOutView, self).update(request, *args, **kwargs)

class AddShippingAddress(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = ShippingAddressSerializer
    permission_classes = (PrivateTokenAccessPermission,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        return super(AddShippingAddress, self).update(request, *args, **kwargs)

class FbLoginSignup(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = FbsignupSerializer
    permission_classes = (PublicTokenAccessPermission,)

    # def get_object(self):
    #     #import pdb; pdb.set_trace()
    #     request_data = self.request.data
    #     fb_id = request_data['fb_id']
    #     try:
    #         obj = get_user_model().objects.get(fb_id__iexact=fb_id)
    #         return obj 
    #     except get_user_model().DoesNotExist:
    #         email = fb_id + '@fb.com'
    #         obj = get_user_model().objects.create(email=email, **request_data)
    #         return obj
    
    # def update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return super(FbLoginSignup, self).update(request, *args, **kwargs)


