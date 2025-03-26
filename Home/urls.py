from django.urls import path
from Home.views import *

urlpatterns = [
        path('',index, name='index'),
        path('Explore',Explore, name='Explore'),
        path('events',events, name='events'),
        path('events/<int:id>',eventDetails, name='event-detail'),
        path('event-register/<int:id>',eventRegister, name='event-register'),
        path('payment/', payment, name='payment'),
        path('process-payment/', process_payment, name='process-payment'),
]
