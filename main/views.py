from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from django import forms
from django.contrib.auth.forms import UserCreationForm
from chat.main.forms import SearchForm

from chat.main.models import Msg,UserProfile
from django.contrib.auth.models import User 
from django.db.models import Q

from django.utils import simplejson 
from django.core import serializers
import settings
import Image
import datetime

def chat_room(request):
    error = False
    form = SearchForm()
    titles = []
    if request.method == 'POST':
        if request.user.is_authenticated():
            if not request.POST.get('message', ''):
                error = True
            else:
                if request.POST['msg_id'] == '':
                    msg_id = None
                else:
                    msg_id = request.POST['msg_id']
                if request.POST['user_id'] == '':
                    user_id = None
                else:
                    user_id = request.POST['user_id']    
                new_msg = Msg.objects.create(user = request.user,title =  request.POST['title'],content = request.POST['message'],date = datetime.datetime.now(),reply_msg = msg_id,reply_user = user_id)
                return HttpResponseRedirect("/")
    msgs = Msg.objects.order_by("-date")
    title_msgs = Msg.objects.exclude(title="").values('title').distinct()
    for t_msg in title_msgs:
        titles.append(t_msg['title'])
    titles.reverse()
    return render_to_response('home.html',{'msgs': msgs,'titles':titles,'error': error,'form': form},context_instance=RequestContext(request))

def refresh(request):
    if True:       
        # a = [{"fields":{"username":"test"}}]
        # result = simplejson.dumps(a)
        # return HttpResponse(result, mimetype="application/json")
        result = []
        last_id = request.GET['last_msg_id']
        msgs = Msg.objects.filter(pk__gt = last_id).order_by("date")
        for msg in msgs:
            message = {}
            message['id'] = msg.pk
            message['user_id'] = msg.user.pk
            message['username'] = msg.user.username
            message['avatar'] = msg.user.get_profile().profile_img.url
            message['title'] = msg.title
            message['content'] = msg.content
            message['date'] = msg.date.strftime('%Y-%m-%d %H:%M:%S')
            message['fav_num'] = msg.fav_num
            result.append(message)
        json_result = simplejson.dumps(result)
        return HttpResponse(json_result, mimetype="application/json")
        # return HttpResponse(serializers.serialize('json', result), mimetype="application/json")
    return HttpResponse()

def reply(request):
    if request.user.is_authenticated():
        reply_to = request.user.pk
        r_msg = Msg.objects.filter(reply_user = reply_to).order_by("-date")
        return render_to_response('reply.html',{'msgs': r_msg},context_instance=RequestContext(request))
    return HttpResponseRedirect("/")

def msg_session(request):
    msg_id = request.GET.get('msg_id', '')
    if msg_id:
        msg = Msg.objects.get(pk = msg_id)
        r_msg = Msg.objects.get(pk = msg.reply_msg)
        return render_to_response('statuses.html',{'msg':msg,'r_msg':r_msg},context_instance=RequestContext(request))
    return HttpResponseRedirect("/")
    
def favorite(request):
    if request.user.is_authenticated():
        msg_id = request.GET['msg_id']
        f_msg = Msg.objects.get(pk = msg_id)
        if request.user in f_msg.fav.all():
            return render_to_response('fav.html')
        else:
            f_msg.fav_num += 1
            f_msg.fav.add(request.user)
            f_msg.save()
        return HttpResponseRedirect("/myfav/")
    return HttpResponseRedirect("/")

def myfavorite(request):
    if request.user.is_authenticated():
        favs = request.user.fav.order_by("-date")
        return render_to_response('fav.html',{'msgs':favs},context_instance=RequestContext(request))
    return HttpResponseRedirect("/")
    
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            result = Msg.objects.filter(Q (content__icontains = cd['search']) | Q (title__icontains = cd['search'])).order_by("-date")
            return render_to_response('search.html',{'msgs': result,'form': form},context_instance=RequestContext(request))
        else:
            return render_to_response('search.html',{'form': form},context_instance=RequestContext(request))
    return HttpResponseRedirect("/")

def search_title(request,title):
    # form = SearchForm()
    result = Msg.objects.filter(title__icontains = title).order_by("-date")
    return render_to_response('search.html',{'msgs': result},context_instance=RequestContext(request))
    
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            try:
                profile = new_user.get_profile()
            except:
            #if there is no profile record existed, then create a new record first
                profile = UserProfile(user = new_user)
                profile.save()
            return HttpResponseRedirect("/accounts/login/")
    else:
        form = UserCreationForm()
    return render_to_response("registration/register.html", {
        'form': form,
    })
   
# def profile(request):
    # form = PictureForm()
    # return render_to_response('profile.html',{'form': form},context_instance=RequestContext(request))
    
def upload(request):
    image = request.FILES.get('image', None)
    if image:
        img = Image.open(image)
        img.thumbnail((48,48),Image.ANTIALIAS)
        abs_name = '%s_%s_%s' % (str(request.user), str(datetime.datetime.today()).replace(':', '-')[:-7], image.name)
        url='profile_img/'+abs_name
        name=settings.MEDIA_ROOT+'/'+url
        img.save(name,"jpeg")
        profile = UserProfile.objects.get(user = request.user)
        profile.profile_img = url
        profile.save()
    return HttpResponseRedirect("/")