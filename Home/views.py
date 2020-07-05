from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import *
# Create your views here.
def index(request):
    course = Course.objects.all()[:3]
    categories =Category.objects.all()
    context={
        'courses':course,
        'categories':categories,
    }
    return render(request,'index.html',context)

def category(request,category):
    # course = Course.objects.all()
    course =Course.objects.filter(category__title=category)
    # udercategory = Category.objects.all()
    # course = Course.objects.all()[:3]

    context={
        # 'categories':category,
        'courses':course,

    }
    return render(request,'category.html',context)

def signup(request):
    if request.method == 'POST':
        form =  RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            group = Group.objects.get(name='teacher')
            user.groups.add(group)
            user = authenticate(username=username, password=raw_password)
            user.is_staff=True
            user.save() 
            login(request,user)
            return redirect('Home:signup')
    else:
        form = RegisterForm()
    return render(request,'signup.html',{'form':form})                    

    
        
   