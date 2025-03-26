from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from dashboard.models import Events,Entries,Payment
from django.contrib import messages
from django.urls import reverse
import razorpay
from django.conf import settings


# Create your views here.

def index(request):
    events = Events.objects.all()[:2]
    return render(request,'Home/index.html',{"events":events})


def Explore(request):
    return render(request,'Home/Explore.html')

def events(request):
    events_obj = Events.objects.all()
    return render(request,'Home/events.html',{"events":events_obj})

def eventDetails(request,id):
    event = Events.objects.get(id=id)
    return render(request,'Home/event-details.html',{"event":event})


def eventRegister(request, id):
    if request.method == "POST":
        team_name = request.POST.get('team_name')
        members = request.POST.get('members')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')

        try:
            event = Events.objects.get(id=id)
            entry = Entries(event=event, team_name=team_name, members=members, Mobile=mobile, email=email)
            entry.save()

            return redirect(reverse('payment') + f"?entry_id={entry.id}")
        
        except Exception as e:
            print(e)
            messages.error(request, f"Error: {e}")
            return redirect('event-detail', id=id)

    if request.method == "GET":
        event = Events.objects.get(id=id)
        return render(request, 'Home/event-register.html', {"event": event})
    
    
    
def payment(request):
    entry_id = request.GET.get('entry_id')

    try:
        entry = Entries.objects.get(id=entry_id)
        event = entry.event
        event_name = event.title
        event_price = int(event.price * 100)
        
        if entry.payment_status:
            messages.success(request, "Payment already made for this entry.")
            return redirect('index')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        order_data = {
            "amount": event_price,
            "currency": "INR",
            "receipt": f"entry_{entry.id}",
            "payment_capture": 1,
        }
        order = client.order.create(data=order_data)

        return render(request, 'Home/payment.html', {
            "entry": entry,
            "event_name": event_name,
            "event_price": event.price,
            "order_id": order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID,
        })

    except Entries.DoesNotExist:
        messages.error(request, "Invalid entry. Please try again.")
        return redirect('index')


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_payment_email(entry, payment_obj):
    subject = f"Payment Confirmation for {entry.event.title}"
    context = {
        'team_name': entry.team_name,
        'event_name': entry.event.title,
        'payment_id': payment_obj.payment_id,
        'amount': entry.event.price,
        'event_date': entry.event.event_date,
        'event_image_url': entry.event.poster_url,
        'whatsapp_group_url': entry.event.whatsapp_group_url
    }

    html_message = render_to_string('Home/payment_confirmation.html', context)
    plain_message = strip_tags(html_message)
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = entry.email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

def process_payment(request):
    entry_id = request.GET.get('entry_id')
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')

    try:
        entry = Entries.objects.get(id=entry_id)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        # Verify Razorpay payment signature
        if client.utility.verify_payment_signature(params_dict):
            entry.payment_status = True
            entry.save()

            # Save payment details in the Payment model
            payment_obj = Payment(
                entry=entry,
                payment_id=payment_id,
                order_id=order_id,
                signature=signature
            )
            payment_obj.save()

            # Call the email sending function
            send_payment_email(entry, payment_obj)

            messages.success(request, "Payment successful! You will receive a confirmation email shortly.")
            return redirect('event-detail', id=entry.event.id)

        else:
            messages.error(request, "Payment verification failed!")
            return redirect('payment')

    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong. Please try again.")
        return redirect('index')
    
    
def PrivacyPolicy(request):
    return render(request, 'Home/privacy-policy.html')

def TermsConditions(request):
    return render(request, 'Home/term-condition.html')

def CancelPolicy(request):
    return render(request, 'Home/cancel-policy.html')