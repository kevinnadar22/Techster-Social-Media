from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from ..utils import AuthenticationUtils
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login 

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        data = request.POST.dict()
        
        validate_data = AuthenticationUtils(
            password=data['password'],
            cpassword=data['cpassword'],
            username=request.user.username,
            request=request,
        )

        if validate_data.password_validation():
            username = request.user.username
            user = User.objects.get(username=request.user.username)
            messages.success(request, 'Password has been changed')
            user.set_password(data['password'])
            user.save()

            login_user = authenticate(
            username=username,
            password=data['password']
        )
            login(request, login_user)
            return redirect('edit_profile')
    return HttpResponseRedirect('/user/edit-profile/')

