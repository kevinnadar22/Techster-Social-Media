from difflib import SequenceMatcher
import json
import re
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import *
from django.core.mail import EmailMessage
from info import *
import os

class AuthenticationUtils():
    def __init__(self, 
    username=None, 
    password=None, 
    cpassword=None, 
    email=None, 
    first_name=None, 
    last_name=None, 
    user=None, 
    request=None):

        self.username = username
        self.password = password
        self.cpassword = cpassword
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.user = user
        self.request = request

    def set_first_last_name(self):
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.save()

    def username_validation(self):
        username_check_pass = True
        username_already_check = User.objects.filter(username=self.username).exists()

        if username_already_check:
            username_check_pass = False
            messages.error(self.request, "Username already in use")

        if 5 >= len(self.username) <= 20:
            username_check_pass = False
            messages.error(self.request, "Username must be at least 20 characters")
        
        elif not re.match("^[a-zA-Z0-9_.-]+$", self.username):
            username_check_pass = False
            messages.error(
                self.request, "Username should contain only alpha-numeric characters", )

        return username_check_pass
        
    
    def password_validation(self):

        password_check_pass = True

        if self.password != self.cpassword:
            password_check_pass = False
            messages.error(self.request, "Password Does not Match",
                            )

        elif 7 >= len(self.password):
            password_check_pass = False
            messages.error(
                self.request, "Your password must contain at least 8 characters",)

        elif similar(self.username, self.password):
            password_check_pass = False
            messages.error(
                self.request, "Username and Password are too similar",)

        return password_check_pass
    
    def email_validation(self):
        email_check_pass = True
        if User.objects.filter(email=self.email).exists():
            email_check_pass = False
            messages.error(self.request, "Email Address already in use")

        return email_check_pass
                

def similar(a, b):
    ratio = SequenceMatcher(None, a, b).ratio()
    if 0.49 < ratio:
        return True

def get_data(request):
    return json.dumps(request.POST)


def send_email(request, user, subject, email_template, email_type='html', ):
    email = request.POST.get('email')
    token = generate_token.make_token(user)
    current_site = get_current_site(request)
    body = render_to_string(email_template,
                            {
                                'name': request.user,
                                "domain": current_site,
                                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                                "token": token,
                                'email_token': urlsafe_base64_encode(force_bytes(email))
                            })

    send_email = EmailMessage(
        subject,
        body,
        EMAIL_HOST_USER,
        [email],
    )
    send_email.content_subtype = email_type
    send_email.send()
    return token

