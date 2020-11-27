from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .signals import subscriptionSubs_created


class Author(models.Model):
    name = models.CharField(max_length=25)
    address = models.TextField()

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    count = models.PositiveIntegerField()
    subscription_cost = models.PositiveIntegerField()
    topic = models.CharField(max_length=20)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.title)


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    address = models.TextField()
    phone = models.PositiveIntegerField()


class Subscription(models.Model):
    subscriber = models.OneToOneField(Subscriber, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    borrowed_date = models.DateField()
    amount_paid = models.PositiveIntegerField()
    days = models.DurationField()
    returned = models.BooleanField()

    # due_amount=(Book. subscription_cost* Subscription.days)  - Subscription.amount_paid
    @property
    def due_amount(self):
        return (self.book.subscription_cost * self.days.days) - self.amount_paid


# @receiver(subscriptionSubs_created, sender=Subscription)
# def handle_new_subscription(sender, **kwargs):
#     print(sender)
#     sub = kwargs['books_sub']
#     book = kwargs['book_count']
#     message = """Subs: {} Book: {}. """.format(sub.count, book.count)
#     print(message)


@receiver(pre_save, sender=Subscription)
def my_callback(sender, instance, *args, **kwargs):
    instance.days = timedelta(days=instance.days.seconds)
