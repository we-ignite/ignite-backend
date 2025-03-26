from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dashboard.models import Events,Entries

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


def adminLogout(request):
    logout(request)
    return redirect('admin-login')

# -------------------------- Code for Login the Admin Dashboard (end) --------------------------


# -------------------------- Code for Admin Dashboard (starts) --------------------------


@login_required(login_url="admin-login")
def dashboard(request):
    events_obj = Events.objects.all()
    return render(request,"dashboard/dashboard.html",{"events_obj":events_obj})


@login_required(login_url="admin-login")
def eventDetails(request,id):
    event = Events.objects.get(id=id)
    entries_obj = Entries.objects.filter(event=event)
    return render(request,"dashboard/event_details.html",{"event":event,"entries_obj":entries_obj})


@login_required(login_url="admin-login")
def editEvent(request,id):
    event = Events.objects.get(id=id)
    entries_obj = Entries.objects.filter(event=event)
    return render(request,"dashboard/event-edit-details.html",{"event":event,"entries_obj":entries_obj})


@login_required(login_url="admin-login")
def editEventSave(request):
    if request.method=="POST":
        id = request.POST.get('id')
        title = request.POST.get('title')
        content = request.POST.get('content')
        rules = request.POST.get('rules')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        tags = request.POST.get('tags')
        price = request.POST.get('price')
        mode = request.POST.get('mode')
        event_date = request.POST.get('event_date')
        poster_url = request.POST.get('poster_url')
        whatsapp_group_url = request.POST.get('whatsapp_group_url')


        event = Events.objects.get(id=id)
        event.title = title
        event.content = content
        event.rules = rules
        event.from_date = from_date
        event.to_date = to_date
        event.tags = tags
        event.price = price
        event.mode = mode
        event.event_date = event_date
        event.poster_url = poster_url
        event.whatsapp_group_url = whatsapp_group_url
        event.save()
        return redirect('event-details/'+str(id))
    return JsonResponse("method not allowed",safe=False)


@login_required(login_url="admin-login")
def addEvent(request):
    if request.method=="POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        rules = request.POST.get('rules')
        event_date = request.POST.get('event_date')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        tags = request.POST.get('tags')
        price = request.POST.get('price')
        mode = request.POST.get('mode')
        poster_url = request.POST.get('poster_url')
        whatsapp_group_url = request.POST.get('whatsapp_group_url')

        event = Events(title=title,content=content,rules=rules,from_date=from_date,to_date=to_date,tags=tags,price=price,mode=mode,event_date = event_date,poster_url = poster_url,whatsapp_group_url = whatsapp_group_url)
        event.save()
        return redirect('dashboard')
    
    return JsonResponse("method not allowed",safe=False)



@login_required(login_url="admin-login")
def deleteEvent(request,id):
    event = Events.objects.get(id=id)
    event.delete()
    return redirect('dashboard')



# -------------------------- Code for Admin Dashboard (starts) --------------------------
