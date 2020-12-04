from django.urls import path
from subscription.views import ListDefaultSubscription as subs

urlpatterns = [
    path('getdefsubs/', subs.as_view(), name='default_subs'),]