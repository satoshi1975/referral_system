import random
import string
import time
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer, ShowOtherProfileSerializer
from referral_system import services


def home(request):
    """main page view"""

    context = {
        'user': request.user,
        'invite_list': UserProfile.objects.filter(used_referral_code=request.user),
    }
    return render(request, 'home.html', context=context)


def send_invite(request):
    """send invite code"""
    return JsonResponse(services.invite_code(request))


def auth_temp(request):
    """create or get user by phone number"""
    return JsonResponse(services.auth_phone_number(request))


def verify_auth_code(request):
    """verify user by auth code"""
    return JsonResponse(services.verify_by_code(request))


class AuthorizePhoneView(APIView):
    """Send phone number for get or create user"""

    def post(self, request):
        auth_code = str(random.randint(1000, 9999))
        time.sleep(2)
        try:
            user, create = UserProfile.objects.get_or_create(
                phone_number=request.data['phone_number'])
            user.auth_code = auth_code
            user.save()
            return Response({'message': f'Authorization code: {auth_code}'})
        except:
            return Response({'message': 'Invalid phone number'})


class CodeVerificationView(APIView):
    """verify user by his phone and auth_code"""

    def post(self, request):
        phone_number = request.data.get('phone_number')
        auth_code = request.data.get('auth_code')

        try:
            user = UserProfile.objects.get(
                phone_number=phone_number, auth_code=auth_code)
        except UserProfile.DoesNotExist:
            return Response({'message': 'Incorrect code or number'})

        if user.referral_code == None:
            characters = string.ascii_letters + string.digits
            referral_code = ''.join(random.choice(characters)
                                    for _ in range(6))
            user.referral_code = referral_code
        user.save()
        login(request, user)

        return Response({'message': 'Code verified'})


class UserProfileByPhoneNumber(APIView):
    """get user's phone and referral code by his phone"""

    def get(self, request, phone_number):
        try:
            user_profile = UserProfile.objects.get(phone_number=phone_number)
            serializer = ShowOtherProfileSerializer(user_profile)
            return Response(serializer.data)

        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found'}, status=status.HTTP_404_NOT_FOUND)


class EnterReferralCodeView(APIView):
    """send another user's referral code"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        referral_code = request.data.get('referral_code')
        try:
            user = UserProfile.objects.get(referral_code=referral_code)
        except:
            return Response({'message': "Incorrect invite code"})
        if user != request.user:
            if request.user.used_referral_code == None:
                request.user.used_referral_code = user
                request.user.save()
                return Response({'message': 'Invitation code activated'})
            else:
                return Response({'message': 'You have already used an invitation code'})
        else:
            return Response({'message': "You can't use your code"})


class UserProfileView(generics.ListAPIView):
    """show current user data"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = UserProfile.objects.get(phone_number=request.user.phone_number)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
