from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from dashboard.models import Events,Entries,Payment
from django.contrib import messages
from django.urls import reverse
import razorpay
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
from cashfree_pg.models.create_order_request import CreateOrderRequest
from cashfree_pg.api_client import Cashfree
from cashfree_pg.models.customer_details import CustomerDetails
from cashfree_pg.models.order_meta import OrderMeta
import urllib3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


Cashfree.XClientId = "77107481798f19dd72ae4279d1470177"
Cashfree.XClientSecret = "cfsk_ma_prod_c9c7c59366cd2247c9b04c54fb530be2_1b0e1aa0"
Cashfree.XEnvironment = Cashfree.PRODUCTION
x_api_version = "2023-08-01"


# Cashfree.XClientId = "TEST10319890eb6dfbd817fd5b5759bd09891301"
# Cashfree.XClientSecret = "cfsk_ma_test_95fc3f3ea67227e3f60c4582a3d783ff_4fe81163"
# Cashfree.XEnvironment = Cashfree.SANDBOX
# x_api_version = "2023-08-01"


CREDENTIALS_FILE = "/home/ubuntu/cred.json"

# Google Sheets API setup
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# Open your spreadsheet
spreadsheet = client.open("Event 2025(April Registration Through Websites")
sheet = spreadsheet.sheet1  # Get the first sheet


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
            customer_id = random.randint(100000, 999999)
            entry = Entries(event=event,customer_id=customer_id, team_name=team_name, members=members, Mobile=mobile, email=email)
            entry.save()

            return redirect(reverse('payment') + f"?entry_id={entry.id}")
        
        except Exception as e:
            print(e)
            messages.error(request, f"Error: {e}")
            return redirect('event-detail', id=id)

    if request.method == "GET":
        event = Events.objects.get(id=id)
        return render(request, 'Home/event-register.html', {"event": event})
    
    
    
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from dashboard.models import Entries  # Ensure Entries model is correctly imported
import logging

logger = logging.getLogger(__name__)


def payment(request):
    entry_id = request.GET.get('entry_id')

    try:
        # Fetch entry details from the database
        entry = Entries.objects.get(id=entry_id)
        event = entry.event
        event_name = event.title
        event_price = float(event.price)

        customer_id = str(entry.customer_id).zfill(3)
        customer_phone = str(entry.Mobile)
        order_amount = event_price

        if entry.payment_status:
            messages.success(request, "Payment already made for this entry.")
            return redirect('index')

        # Create Cashfree Order Request
        customer_details = CustomerDetails(
            customer_id=customer_id,
            customer_phone=customer_phone
        )
        order_meta = OrderMeta(
            return_url=f"https://ignitestudentassociation.in/verify_payment?order_id={entry.id}&order_status=PAID",
            notify_url="https://ignitestudentassociation.in/payment_notify/"
        )
        create_order_request = CreateOrderRequest(
            order_amount=order_amount,
            order_currency="INR",
            customer_details=customer_details,
            order_meta=order_meta
        )

        # Call Cashfree API
        response = Cashfree().PGCreateOrder(x_api_version, create_order_request, None, None)

        logger.debug(f"Cashfree Response: {response.__dict__}")

        if hasattr(response, 'data') and hasattr(response.data, 'order_status'):
            order_entity = response.data
        
            
            print(order_entity)
            print()
            print(order_entity.order_id)

            if order_entity.order_status == 'ACTIVE':
                return_url = f'https://ignitestudentassociation.in/verify_payment?entry_id={entry.id}&order_amount={order_amount}&payment_id={order_entity.order_id}&cf_order_id={order_entity.cf_order_id}'
                notify_url = f'https://ignitestudentassociation.in/payment_notify/'
                
                print()
                print(return_url)
                
                logger.debug(f"Generated return URL: {return_url}")
                return render(request, 'Home/payment.html', {
                    "entry": entry,
                    "event_name": event_name,
                    "event_price": event.price,
                    "order_id": order_entity.order_id,
                    'payment_session_id': order_entity.payment_session_id,
                    'return_url': return_url,
                    'notify_url': notify_url
                })

        messages.error(request, "Failed to create order. Please try again.")
        return redirect('payment_page')

    except Entries.DoesNotExist:
        messages.error(request, "Invalid entry. Please try again.")
        return redirect('index')

    except Exception as e:
        logger.error(f"Error processing payment: {e}")
        messages.error(request, "Something went wrong while processing the payment.")
        return redirect("payment_page")


 
import requests
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

def verify_payment(request):
    """
    Verify payment after Cashfree redirects the user post-payment.
    """
    order_id = request.GET.get("entry_id")
    cf_order_id = request.GET.get("payment_id")

    # Validate input
    if not order_id or not cf_order_id:
        logger.error("Invalid payment details: Missing order_id or cf_order_id")
        return JsonResponse("Invalid payment details", safe=False)  # Redirect to homepage

    try:
        # Fetch the entry from the database
        entry = Entries.objects.get(id=int(order_id))

        # Check if the payment is already recorded
        if Payment.objects.filter(entry=entry, order_id=order_id).exists():
            logger.info(f"Payment already recorded for order_id: {order_id}")
            return JsonResponse("Payment already recorded", safe=False)  # Redirect to homepage

        # Determine the base URL based on the environment
        base_url = "https://api.cashfree.com"
        url = f"{base_url}/pg/orders/{cf_order_id}"
        headers = {
            "x-api-version": Cashfree.XApiVersion,
            "x-client-id": Cashfree.XClientId,
            "x-client-secret": Cashfree.XClientSecret,
        }

        try:
            # Make the API request to verify payment
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Check if the response status is 200 OK
            if response.status_code == 200:
                payment_details = response.json()
                order_status = payment_details.get("order_status", "FAILED")

                # Log the API response for audit
                logger.info(f"Payment verification response: {payment_details}")

                # Check if the payment was successful
                if order_status == "PAID":
                    payment = Payment.objects.create(
                        entry=entry,
                        payment_id=payment_details.get("cf_order_id"),
                        order_id=order_id,
                        payment_status="PAID",
                        order_amount=payment_details.get("order_amount")
                    )

                    # Update entry payment status
                    entry.payment_status = True
                    entry.save()

                    # Send confirmation email
                    send_payment_email(entry, payment)
                    created_at_str = entry.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    sheet.append_row([entry.event.title, entry.team_name, entry.email, entry.Mobile, entry.members, created_at_str])

                    messages.success(request, "Payment successful! Confirmation email sent.")
                    return redirect("payment_success")

                # Payment failed or canceled
                logger.warning(f"Payment failed or canceled for order_id: {order_id}")
                messages.error(request, "Payment failed or canceled.")
                return redirect("payment_failure")

            else:
                # Non-200 status code
                error_message = response.json().get("message", "Unknown error")
                logger.error(f"Failed to verify payment: {error_message}")
                messages.error(request, f"Payment verification failed: {error_message}")
                return redirect("payment_failure")

        except requests.RequestException as api_error:
            # Log network or API errors
            logger.error(f"Network error during payment verification: {api_error}")
            messages.error(request, "Error verifying payment. Please try again later.")
            return redirect("index")

    except Entries.DoesNotExist:
        # Handle invalid entry ID
        logger.error(f"Invalid order ID: {order_id}")
        messages.error(request, "Invalid order ID.")
        return redirect("index")

    except Exception as e:
        # Handle generic errors
        logger.error(f"Unexpected error during payment verification: {e}")
        messages.error(request, "Something went wrong. Please contact support.")
        return redirect("index")
    
    

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

# def process_payment(request):
#     entry_id = request.GET.get('entry_id')
#     payment_id = request.GET.get('payment_id')
#     order_id = request.GET.get('order_id')
#     signature = request.GET.get('signature')

#     try:
#         entry = Entries.objects.get(id=entry_id)

#         client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#         params_dict = {
#             'razorpay_order_id': order_id,
#             'razorpay_payment_id': payment_id,
#             'razorpay_signature': signature
#         }

#         if client.utility.verify_payment_signature(params_dict):
#             entry.payment_status = True
#             entry.save()

#             payment_obj = Payment(
#                 entry=entry,
#                 payment_id=payment_id,
#                 order_id=order_id,
#                 signature=signature
#             )
#             payment_obj.save()

#             send_payment_email(entry, payment_obj)

#             messages.success(request, "Payment successful! You will receive a confirmation email shortly.")
#             return redirect('event-detail', id=entry.event.id)

#         else:
#             messages.error(request, "Payment verification failed!")
#             return redirect('payment')

#     except Exception as e:
#         print(e)
#         messages.error(request, "Something went wrong. Please try again.")
#         return redirect('index')
    
    
def paymentSuccess(request):
    return render(request, 'Home/payment_success.html')

def paymentFailure(request):
    return render(request, 'Home/payment_failure.html')
    
def PrivacyPolicy(request):
    return render(request, 'Home/privacy-policy.html')

def TermsConditions(request):
    return render(request, 'Home/term-condition.html')

def CancelPolicy(request):
    return render(request, 'Home/cancel-policy.html')