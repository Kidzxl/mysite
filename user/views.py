from django.http import JsonResponse
from django.shortcuts import render_to_response,render,redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import *
from .models import Profile
from django.core.mail import send_mail
import datetime
import time
import string
import random

def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from',reverse('home')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)

def register(request):
    if request.method == "POST":
        reg_form = RegForm(request.POST,request=request)
        print(11)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']
            #创建用户
            user =User.objects.create_user(username=username,email=email,password=password)
            user.save()
            #清除 session
            del request.session['register_code']
            #登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from',reverse('home')))

def user_info(request):
    context = {}

    return render(request,'user/user_info.html',context)

def change_nickname(request):
    return_to = request.GET.get('from',reverse('home'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST,user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile,created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(return_to)
    else :
        form = ChangeNicknameForm()

    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['form_title'] = "修改昵称"
    context['submit_text'] = '修改'
    context['return_back_url']=return_to
    return render(request,'form.html',context)

def bind_email(request):
    return_to = request.GET.get('from', reverse('home'))
    if request.method == 'POST':
        print("post")
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清除 session
            del request.session['bind_email_code']
            return redirect(return_to)
    else:
        print("get")
        form = BindEmailForm()

    context = {}
    context['form'] = form
    context['page_title'] = '绑定邮箱'
    context['form_title'] = "绑定邮箱"
    context['submit_text'] = '绑定'
    context['return_back_url'] = return_to
    return render(request, 'user/bind_email.html', context)

def send_verification_code(request):
    send_for = request.GET.get("send_for",'')
    email = request.GET.get('email','')
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters +string.digits,4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time',0)
        if now-send_code_time <30 :
            data['staus'] = 'ERROR'
        else:
            request.session[send_for]=code
            request.session['send_code_time'] = now
            send_mail(
                '绑定邮箱',
                '验证码: %s' % code,
                '1440244289@qq.com',
                [email],
                fail_silently=False,
            )
            data['status']= "SUCCESS"
    else:
        data['status'] = "ERROR"
    return JsonResponse(data)

def change_password(request):
    redirect_to = reverse('home')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            print(new_password)
            user.save()
            auth.logout(request)
            return redirect(redirect_to)
    else:
        form = ChangePasswordForm()

    context = {}
    context['form'] = form
    context['page_title'] = '修改密码'
    context['form_title'] = "修改密码"
    context['submit_text'] = '修改'
    context['return_back_url'] = redirect_to
    return render(request, 'form.html', context)

def forgot_password(request):
    redirect_to = reverse('login')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            print(new_password)
            user.save()
            print(user.get_password)
            # 清除 session
            del request.session['forgot_password_code']
            return redirect(redirect_to)
    else:
        print("get")
        form = ForgotPasswordForm()

    context = {}
    context['form'] = form
    context['page_title'] = '重置密码'
    context['form_title'] = "重置密码"
    context['submit_text'] = '重置'
    context['return_back_url'] = redirect_to
    return render(request, 'user/forgot_password.html', context)