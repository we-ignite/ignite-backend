from django.urls import path
from dashboard.views import *

urlpatterns = [
    path('',dashboard, name='dashboard'),
    path('login',adminLogin, name='admin-login'),
    path('logout',adminLogout, name='admin-logout'),
    
    
    path('add-event',addEvent, name='add-event'),
    path('event-details/<int:id>',eventDetails, name='event-detail'),
    path('edit-event/<int:id>',editEvent, name='edit-event'),
    path('edit-event-save',editEventSave, name='edit-event-save'),
    path('delete-event/<int:id>',deleteEvent, name='delete-event'),
    
]
