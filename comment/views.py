from django.shortcuts import render_to_response,render,redirect
from .models import Comment
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm
from django.http import JsonResponse

def update_comment(request):
    #referer = request.META.get("HTTP_REFERER", reverse('home'))
    comment_form = CommentForm(request.POST,user=request.user)
    data = {}

    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        #返回数据
        data['status']= 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.strftime("%Y-%m-%d:%H:%M:%S")
        data['text'] = comment.text
    else :
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
