# External Import
from django.conf import settings
from rest_framework import generics, response, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import permissions

# Internal Import
from . import serializers
from . import models
from .utils import Util


class UserRegistrationView(generics.GenericAPIView):
    """ Generic API View for User Registration """

    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request):
        """ Post Request for User Registration and also sending user verification email """
        user = request.data

        # From UserRegistration Serializer
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        current_user_data = serializer.data

        user = models.User.objects.get(email=current_user_data['email'])

        # Token
        token = str(RefreshToken().for_user(user).access_token)

        # Sending Verification URL to the current_user
        current_site = get_current_site(request)
        relative_link = reverse('verify-email')
        absolute_url = f"http://{current_site}{relative_link}?token={token}"
        email_body = f"Namaste {user.username}\n Use link below to verify your account.\n{absolute_url}"
        email_message = {
            'email_body': email_body,
            'email_subject': "Verify Your Email For SlicedTv Account",
            'to_email': user.email
        }
        # Sending from utils.py file
        Util.send_email(email_message)

        return response.Response(current_user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    """ Verifying User Email"""

    def get(self, request):
        """ GET method which takes token which was sent to the user's email after registration """

        token = request.GET.get('token')

        try:
            # Working with received token
            received_token = jwt.decode(token, settings.SECRET_KEY)
            user = models.User.objects.get(id=received_token['user_id'])

            # Changing User status to verified
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return response.Response({'message': 'Email Successfully Activated'})

        except jwt.ExpiredSignatureError as identifier:
            return response.Response({'errors': 'Activation Link Expired'}, status=status.HTTP_400_BAD_REQUEST)
            # ! Should send the user another activation link by asking the user.

        except jwt.exception.DecodeError as identifier:
            return response.Response({'errors': 'Invalid Activation Link'}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(generics.GenericAPIView):
    """Login User in """

    serializer_class = serializers.UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return response.Response(serializer.data, status=status.HTTP_200_OK)


class RequestUserPasswordResetByEmail(generics.GenericAPIView):
    """ Request to reset the password """

    serializer_class = serializers.RequestUserPasswordResetByEmailSerializer

    def post(self, request):
        """ POST method for password Reset """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data['email']
        current_user = models.User.objects.filter(email=email)

        if current_user.exists():
            current_user = current_user.first()
            uidb64 = urlsafe_base64_encode(smart_bytes(current_user.id))
            token = PasswordResetTokenGenerator().make_token(user=current_user)
            # Sending Verification URL to the current_user
            current_site = get_current_site(request=request).domain
            relative_link = reverse(
                'confirm-password-reset', kwargs={'uidb64': uidb64, 'token': token})
            absolute_url = f"http://{current_site}{relative_link}"
            email_body = f"Namaste {current_user.username}\n Use link below to Reset your Password.\n{absolute_url}"
            email_message = {
                'email_body': email_body,
                'email_subject': "Reset your password for SlicedTv Account",
                'to_email': current_user.email
            }
            # Sending from utils.py file
            Util.send_email(email_message)

        # The response will be success even if the email is not found for security reasons
        return response.Response({'success': True, 'meassage': 'Email Sent'}, status=status.HTTP_200_OK)


class ResetPasswordTokenCheckAPI(generics.GenericAPIView):
    """Check if the password reset token is valid"""

    def get(self, request, uidb64, token):
        """ Check if the token is valid  """
        try:
            id = smart_bytes(urlsafe_base64_decode(uidb64))
            current_user = models.User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user=current_user, token=token):
                return response.Response(
                    {'errors': 'Token is not valid, request another'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return response.Response({
                'success': True,
                'message': 'Credentials Valid',
                'uidb64': uidb64,
                'token': token,
            }, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return response.Response(
                {'errors': 'Token is not valid, request another'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangeUserPasswordAPI(generics.GenericAPIView):
    """Change the password after confirming email when user forgot the password"""

    serializer_class = serializers.ChangeUserPasswordAPISerializer

    def patch(self, request):
        """ Change the user password """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return response.Response({'success': True, 'message': 'Password Reset Successful'}, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    """ Change Password when User is Logged In """

    serializer_class = serializers.ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return response.Response({"success": True, "message": "Password Changed Successfully"}, status=status.HTTP_200_OK)


class GetUserSubscriptionTypeAPIView(generics.GenericAPIView):
    """ Provide subscription type of the current user """

    # serializer_class = serializers.GetUserSubscriptionTypeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """ GET Method for subscription """
        current_user = request.user
        subscription_type = current_user.subscription.subscription_type
        return response.Response({"subscription_type": subscription_type})
