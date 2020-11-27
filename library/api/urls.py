from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AuthorViewSet, BookViewSet, SubscriberViewSet, SubscriptionViewSet, SubscriberNotReturned, \
    AddSubscription, AggViewSet, VanillaView, BookListView, GenericBookView, BookRetrieveView

router = DefaultRouter()

router.register(r'author', AuthorViewSet)
router.register(r'book', BookViewSet)
router.register(r'subscriber', SubscriberViewSet)
router.register(r'subscription', SubscriptionViewSet)
router.register(r'agg_cost',AggViewSet, basename='ln-agg')

urlpatterns = router.urls  + [
    path('subscriber-not-returned/', SubscriberNotReturned.as_view(),name='not-ret'),
    path('add-subscription/', AddSubscription.as_view(), name='add-sub'),
    path('test-list-view/', VanillaView.as_view(), name='test-view'),
    path('book-list-view/', BookListView.as_view(), name="book-list-view"),
    path('book-ret-view/<pk>', BookRetrieveView.as_view(), name="book-retrieve-view"),
    path('generic-view/', GenericBookView.as_view(), name='generic-view'),
]