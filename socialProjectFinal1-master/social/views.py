from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User, auth
from accounts.models import permittedlist, userpermission, resolvedlist
from django.contrib.auth.decorators import login_required
from social.models import Post
from datetime import datetime
from django_private_chat.models import Dialog,Message
#django private chat override

from django.views import generic
from braces.views import LoginRequiredMixin

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django_private_chat import models
from django_private_chat import utils
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Q

class myDialogListView(LoginRequiredMixin, generic.ListView):
    template_name = 'django_private_chat/dialogs.html'
    model = models.Dialog
    ordering = 'modified'

    def get_queryset(self):
        dialogs = models.Dialog.objects.filter(Q(owner=self.request.user) | Q(opponent=self.request.user))
        return dialogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.kwargs.get('username'):
            # TODO: show alert that user is not found instead of 404
            user = get_object_or_404(get_user_model(), id =self.kwargs.get('username'))
            dialog = utils.get_dialogs_with_user(self.request.user, user)
            if len(dialog) == 0:
                if self.request.user.userpermission.is_student == True:
                    dialog = models.Dialog.objects.create(owner=self.request.user, opponent=user)#I guess we have to work here such that user isn't student dialog shouldn't be created
                else:
                    raise Http404("Faculty or counsellor not authorized to start a dialog")
            else:
                dialog = dialog[0]
            context['active_dialog'] = dialog
        else:
            context['active_dialog'] = self.object_list[0]
        if self.request.user == context['active_dialog'].owner:
            context['opponent_username'] = context['active_dialog'].opponent.username
        else:
            context['opponent_username'] = context['active_dialog'].owner.username
        context['ws_server_path'] = '{}://{}:{}/'.format(
            settings.CHAT_WS_SERVER_PROTOCOL,
            settings.CHAT_WS_SERVER_HOST,
            settings.CHAT_WS_SERVER_PORT,
        )
        return context

#django private chat override end
# Create your views here.
def index(request):
    return render(request,'social/index.html')
def register(request):
    if 'register' in request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username = username).exists():
                return render(request,'social/register.html',{'error_message':"Username already taken"})
            elif User.objects.filter(email = email).exists():
                return render(request,'social/register.html',{'error_message':"Email already taken"})
            else:
                user= User.objects.create_user(username = username, password = password1, email = email, first_name= first_name, last_name = last_name)
                user.save()
                a= userpermission(user = user,is_student = True, is_counsellor = False, is_faculty = False )
                a.save()
                b = permittedlist(user= user)
                b.save()   
                c = resolvedlist(user= user)
                c.save()                
                return redirect('/social/login/')
        else:
            return render(request,'social/register.html',{'error_message':"Password does not match"})
    return render(request,'social/register.html')
def login(request):
    if 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user != None:
            auth.login(request,user)
            return redirect('/')
        else:
            return render(request, 'social/login.html', {'error_message': "Invalid Credentials"})
    return render(request, 'social/login.html')
@login_required(login_url= '/social/login/')
def home(request):
    #all_user= User.objects.all()
    #dict = {'all_user':all_user}
    all_user = []
    a = request.user
    if a.userpermission.is_student == True:
        all_user= User.objects.all()
    else:
        for dia in a.dialog_set.all():
            all_user.append(dia.owner)   
    return render(request,'social/home.html',{'all_user':all_user})

@login_required
def trustable(request, id_user):# all user objects fine as this view only for student. Means all faculty
    all_user= User.objects.all()
    try:
        user = User.objects.get(id =id_user )
    except User.DoesNotExist :
        raise Http404("User does not exist")
    request.user.permittedlist.allowed.add(user.permittedlist)
    return HttpResponse("ok")
@login_required
def resolved(request, id_user):
    all_user= User.objects.all()
    try:
        user = User.objects.get(id =id_user )
    except User.DoesNotExist :
        raise Http404("User does not exist")
    request.user.resolvedlist.resolved.add(user.resolvedlist)
    return HttpResponse("ok")
@login_required
def untrustable(request, id_user):# all user objects fine as this view only for student. Means all faculty
    all_user= User.objects.all()
    try:
        user = User.objects.get(id =id_user )
    except User.DoesNotExist :
        raise Http404("User does not exist")
    request.user.permittedlist.allowed.remove(user.permittedlist)
    return HttpResponse("ok")
@login_required
def create(request):
    if request.user.is_superuser:
        if 'register' in request.POST:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            userType = int(request.POST['userType'])
            is_faculty = False 
            is_counsellor = False
            if userType == 0:
                is_faculty = True
            elif userType == 1:
                is_counsellor = True
            if password1 == password2:
                if User.objects.filter(username = username).exists():
                    return render(request,'social/create.html',{'error_message':"Username already taken"})
                elif User.objects.filter(email = email).exists():
                    return render(request,'social/create.html',{'error_message':"Email already taken"})
                else:
                    user= User.objects.create_user(username = username, password = password1, email = email, first_name= first_name, last_name = last_name)
                    user.save()
                    a= userpermission(user = user,is_student = False, is_counsellor = is_counsellor, is_faculty = is_faculty )
                    a.save()
                    b = resolvedlist(user= user)
                    b.save()       
                    c = permittedlist(user= user)
                    c.save()           
                    return redirect('/')
            else:
                return render(request,'social/create.html',{'error_message':"Password does not match"})
        return render(request,'social/create.html')
    else:
        raise Http404("You are not authorized.")
@login_required
def unresolved(request,id_user):
    all_user= User.objects.all()
    try:
        user = User.objects.get(id = id_user)
    except User.DoesNotExist:
        raise Http404("User not found")
    user.resolvedlist.resolved.remove(request.user.resolvedlist)
    request.user.permittedlist.allowed.remove(user.permittedlist)
    return HttpResponse("ok")
@login_required
def post(request):
    all_post = Post.objects.all().order_by('-date')
    return render(request,'social/posts.html',{'all_post':all_post})
@login_required
def addPost(request):
    if request.user.userpermission.is_student == False:
        if 'add' in request.POST:
            image = None
            username = request.user.username
            desription = request.POST['description']
            date = datetime.now()
            if 'image' in request.FILES:
                image = request.FILES['image']
            a = Post(username = username,desription = desription,date = date, image = image)
            a.save()
            if 'image' in request.FILES:
                image = request.FILES['image']
                a.image = image
        all_post = Post.objects.all().order_by('-date')
        return render(request,'social/posts.html',{'all_post':all_post})
    else:
        raise Http404("Unathorized acess")                    