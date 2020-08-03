from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import RegisterForm , CommentForm
from .models import *
# Create your views here.
def index(request):
    course = Course.objects.all()[:5]
    category = Category.objects.all()[:3]
    comments = Comment.objects.all()[:3]
    categories =Category.objects.all()
    search_list =request.GET.get('q')
    if search_list :
        course = Course.objects.filter(
            Q(description__icontains = search_list) | Q(name__icontains = search_list)
        ).distinct()
       
    context={
        # 'posts':posts,
        'comments':comments,
        'courses':course,
        'category':category,
        'categories':categories,
        "home_page": "active"
    }
    return render(request,'index.html',context)

def Courses(request):
    category = Category.objects.all()[:3]

    course = Course.objects.published()
    search_list =request.GET.get('q')
    if search_list :
        course = Course.objects.filter(
            Q(description__icontains = search_list) | Q(name__icontains = search_list)
        ).distinct()
    paginator = Paginator(course, 2) # Show 2 contacts per page
    page = request.GET.get('page')
    course = paginator.get_page(page)     
    context={
        'category':category,
        'courses':course,
        "course_page": "active"

    }
    return render(request,'courses.html',context)
def Coursedetail(request,id):
    category = Category.objects.all()[:3]
    detail_course =Course.objects.get(id=id)
    related_course = Course.objects.filter(category=detail_course.category).exclude(id=id)
    sessions = detail_course.session_set.all()
    counts = detail_course.session_set.all().count()
    comments = detail_course.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = detail_course
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    context={
        'category':category,
        'detail':detail_course,
        'sessions':sessions,
        'counts':counts,
        'related_course':related_course,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }
    return render(request,'more-info.html',context)

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
    return render(request,'signup.html',{'form':form,"signup_page": "active"})                    

def signup_student(request):

    if request.method == 'POST':
        form =  RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            group = Group.objects.get(name='student')
            user.groups.add(group)
            user = authenticate(username=username, password=raw_password)
            user.save() 
            login(request,user)
            return redirect('Home:signup-student')
    else:
        form = RegisterForm()
    return render(request,'signup-student.html',{'form':form,"signup_page": "active"}) 
        
   