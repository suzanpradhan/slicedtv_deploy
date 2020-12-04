from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from .models import Subscription
from subscription.serializers import DefaultSubscription

class ListDefaultSubscription(generics.ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = DefaultSubscription

    def list(self, request):
        queryset = self.get_queryset()
        serializer = DefaultSubscription(queryset, many=True)
        return Response(serializer.data)
