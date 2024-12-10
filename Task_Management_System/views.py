from django.shortcuts import render, redirect 
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth import logout ,authenticate ,login
from django.views import View
from django.shortcuts import get_object_or_404
from .models import User,Task,Comment
import re
from .forms import TaskForm
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password



User = get_user_model()

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            errors = {}

            if not username.isalpha():
                errors["username"] = "Username must contain only characters."

            if User.objects.filter(email=email).exists():
                errors["email"] = "Email is already registered."

            if "@" not in email or "." not in email:
                errors["email"] = "Enter a valid email address."

            if len(password) < 5:
                errors["password"] = "Password must be at least 5 characters."

            if not re.search(r"[!@#$%^&*|<>,(){}]", password):
                errors["password"] = "Password must contain at least one special character."

            if errors:
                return render(request, "signup.html", {"errors": errors})

            user = User(first_name=username, email=email)
            user.set_password(password)  
            user.save()

            return redirect("login")
        except IntegrityError as e:
            return render(request, 'signup.html', {'error': 'Email or Username already exists.', 'details': str(e)})
        except Exception as e:
            return render(request, 'signup.html', {'error': 'An error occurred', 'details': str(e)})

    
class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            return redirect('home_page')
        return render(request, 'login.html', {'error': 'Invalid email or password'})
        
class Create_Task(LoginRequiredMixin,View):
    login_url='login'
    def get(self,request):
        form=TaskForm()
        users=User.objects.all()
        return render(request,'create_task.html',{'form':form,'users':users})
    
    def post(self,request):
        form= TaskForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data['title']
            description=form.cleaned_data['description']
            assigned_to=form.cleaned_data['assigned_to']
            assigned_by=request.user
            start_date=form.cleaned_data['start_date']
            end_date=form.cleaned_data['end_date']
            priority=form.cleaned_data['priority']
            status=form.cleaned_data['status']
            
            task=Task.objects.create(
                title=title,
                description=description,
                assigned_to=assigned_to,
                assigned_by=assigned_by,
                start_date=start_date,
                end_date=end_date,
                priority=priority,
                status=status,
            )
            return redirect('home_page')
        else:
            return render(request,'create_task.html',{"form": form ,"error":'Please correct the errors below.'})

                
class Home_Page(LoginRequiredMixin,View):
    login_url='login'
    def get(self,request):
        task= Task.objects.all()
        return render(request,'home_page.html',{'tasks':task})
    
class Logout(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        return redirect('login')
             


 