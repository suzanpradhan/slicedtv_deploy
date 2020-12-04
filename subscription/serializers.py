from subscription.models import Subscription
from rest_framework import serializers


class DefaultSubscription(serializers.ModelSerializer):
    class Meta:
        model = Subscription

        fields=["subscription_type","subscription_amount",]
