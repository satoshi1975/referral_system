import time
from .models import UserProfile
from django.contrib.auth import login
import random
import string


def invite_code(request):
    """check referral code"""
    correct_user = request.user
    invite = request.POST.get('referral-code')
    if UserProfile.objects.filter(referral_code=invite).exists():
        user = UserProfile.objects.get(referral_code=invite)
        correct_user.used_referral_code = user
        correct_user.save()
        return {'success': True}
    else:
        return {'success': False}


def auth_phone_number(request):
    """get or create new user in django templates"""
    phone_number = request.POST.get('phone_number')

    if UserProfile.objects.filter(phone_number=phone_number).exists():
        user = UserProfile.objects.get(phone_number=phone_number)
    else:
        user = UserProfile.objects.create(phone_number=phone_number)
    auth_code = str(random.randint(1000, 9999))
    user.auth_code = auth_code

    user.save()
    time.sleep(2)
    return {"success": True, "message": f"Your code: {auth_code}", 'phone': phone_number}


def verify_by_code(request):
    """check auth code and authenticate"""
    phone = request.POST.get('phone')
    auth_code = request.POST.get('auth_code')
    try:
        user = UserProfile.objects.get(phone_number=phone, auth_code=auth_code)
    except:
        return {"success": False, "message": f"Incorrect code"}
    if user.referral_code == None:
        characters = string.ascii_letters + string.digits
        referral_code = ''.join(random.choice(characters) for _ in range(6))
        user.referral_code = referral_code
    user.save()
    login(request, user)
    return {'success': True}
