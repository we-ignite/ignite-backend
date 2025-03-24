from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

# -------------------------- Code for Login the Admin Dashboard (starts) --------------------------

def adminLogin(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, "User Not Found")
            return redirect('admin-login')

        user = authenticate(username=username,password=password)
        if user is None:
            messages.success(request, "Wrong Password")
            return redirect('admin-login')

        login(request,user)
        return redirect('dashboard')
    return render(request,"dashboard/login.html")

# -------------------------- Code for Login the Admin Dashboard (end) --------------------------


# -------------------------- Code for Admin Dashboard (starts) --------------------------


@login_required(login_url="admin-login")
def dashboard(request):
    return render(request,"dashboard/dashboard.html")



# -------------------------- Code for Admin Dashboard (starts) --------------------------
