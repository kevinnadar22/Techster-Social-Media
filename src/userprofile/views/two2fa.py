import random
import re
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from ..models import _UserProfileModel
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import http.client
import json
from ..models import _OTPModel


@login_required(login_url="login")
def get_otp_view(request):
    user = request.user
    profile = _UserProfileModel.objects.get(user=user)
    context = {"profile": profile}

    if profile.is_2fa:
        return HttpResponseRedirect('/user/edit-profile/')
    
    if request.method == "POST":
        otp = request.POST.get('otp')
        try:
            otp_obj = _OTPModel.objects.get(otp=otp)

            if otp_obj.is_verified:
                messages.error(request, 'OTP expired')

            if otp_obj.is_expired:
                messages.error(request, 'OTP expired')

            elif otp_obj is None:
                messages.error(request, 'Invalid OTP, Try again later')

            otp_obj.is_verified = True
            otp_obj.save()
            profile.is_2fa = True
            profile.save()
            messages.success(request, 'Saved Successfully')
            
        except Exception  as e:
            messages.error(request, 'Invalid OTP, Try again later')


    return render(request, "user/2FA.html", context=context)


def get_otp(request):
    if request.method == 'POST':

        data = request.POST.dict()
        otp = random.randint(1000, 999999)
        phone_number = data['phone_number']
        
        conn = http.client.HTTPConnection("2factor.in")
        payload = ""
        headers = { 'content-type': "application/x-www-form-urlencoded" }
        api_key = settings.TWOFACTORIN_API
        conn.request("GET", f"/API/V1/{api_key}/SMS/{phone_number}/{otp}", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = data.decode("utf-8")
        checksum = json.loads(data)
        
        if checksum['Status'] == 'Success':
            otp_obj = _OTPModel.objects.create(otp=otp)
            otp_obj.save()
        else:
            messages.success(request, 'Error in sending OTP')
        return HttpResponse(data)
