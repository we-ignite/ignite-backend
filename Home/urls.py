from django.urls import path
from Home.views import *

urlpatterns = [
        path('',index, name='index'),
        path('Explore',Explore, name='Explore'),
        path('events',events, name='events'),
        path('events/<int:id>',eventDetails, name='event-detail'),
        path('event-register/<int:id>',eventRegister, name='event-register'),
        path('payment/', payment, name='payment'),
        # path('process-payment/', process_payment, name='process-payment'),
        path('PrivacyPolicy',PrivacyPolicy, name='PrivacyPolicy'),
        path('Terms',TermsConditions, name='Terms'),
        path('CancelPolicy',CancelPolicy, name='CancelPolicy'),
        path('verify_payment', verify_payment, name='verify-payment'),
        path('payment-success', paymentSuccess, name='payment_success'),

]
