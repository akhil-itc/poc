from datetime import datetime

from django.contrib.auth.models import User
from django.db.models import Avg, Max
from django.dispatch import receiver
from django.template.backends import django
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from ..models import Author, Book, Subscriber, Subscription
from ..signals import subscriptionSubs_created


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'



class BookSerializers(serializers.ModelSerializer):
    # author = AuthorSerializers(many=True)

    class Meta:
        model = Book
        fields = ('title', 'description', 'count', 'subscription_cost', 'topic', 'author')


class SubscriberSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = '__all__'


class AggregateSerializer(serializers.ModelSerializer):
    subs_cost_avg = serializers.SerializerMethodField()
    max_cost = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('subs_cost_avg', 'max_cost')

    def get_subs_cost_avg(self, obj):
        subs_cost_avg = Book.objects.aggregate(subs_cost_avg=Avg('subscription_cost'))
        print(subs_cost_avg)
        return subs_cost_avg['subs_cost_avg']

    def get_max_cost(self, obj):
        max_cost = Book.objects.aggregate(max_cost=Max('subscription_cost'))
        print(max_cost)
        return max_cost['max_cost']


class SubscriptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        # fields = "__all__"
        fields = ('book', 'borrowed_date', 'amount_paid', 'days', 'returned', 'due_amount')


class SubscriptionSubsSerializers(serializers.ModelSerializer):
    subscriber = SubscriberSerializers()

    class Meta:
        model = Subscription
        fields = ('due_amount', 'subscriber', 'book', 'borrowed_date', 'amount_paid', 'days', 'returned', 'due_amount')

    def create(self, validated_data):
        books_sub = Subscription.objects.filter(book=validated_data['book'], returned=False).count()
        book_count = Book.objects.only('count').get(pk=validated_data['book'].pk)
        if book_count.count - books_sub > 0:

            subscriber_data = validated_data.pop('subscriber')
            subscriber = Subscriber.objects.create(**subscriber_data)
            subscription = Subscription.objects.create(subscriber=subscriber, **validated_data)
            return subscription
        else:

            raise ValidationError('Book is taken away')
