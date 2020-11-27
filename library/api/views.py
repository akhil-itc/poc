from django.db.models import F, ExpressionWrapper, DateField, Avg
from django.utils import timezone

from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AuthorSerializers, BookSerializers, SubscriberSerializers, SubscriptionSerializers, \
    SubscriptionSubsSerializers, AggregateSerializer
from ..models import Author, Book, Subscriber, Subscription


class VanillaView(APIView):
    def get(self, request, format=None):
        # return Response({"sad": "wew"})
        books = Book.objects.all()
        serializer = BookSerializers(books, many=True)
        return Response(serializer.data)


class GenericBookView(GenericAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

    def get_context_data(self, **kwargs):
        # Call class's get_context_data method to retrieve context
        context = super().get_context_data(**kwargs)

        context['page_title'] = 'My page title'
        return context


class BookRetrieveView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers

    # def get_queryset(self):
    #     return Book.objects.all()
    #
    # def get_serializer_class(self):
    #     return BookSerializers


class BookRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers


class AggViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Book.objects.all()
        # print(queryset)
        # for q in queryset:
        #     print(q)
        serializer = AggregateSerializer(queryset)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializers

    queryset = Author.objects.all()


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializers
    queryset = Book.objects.all()
    print(queryset.explain())
    @action(detail=False)
    def recent(self, request):
        snippet = self.get_object()
        return Response(snippet.data)


class SubscriberViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriberSerializers
    queryset = Subscriber.objects.all()


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializers
    queryset = Subscription.objects.all()


class SubscriberNotReturned(generics.ListAPIView):
    serializer_class = SubscriptionSerializers

    queryset = Subscription.objects.annotate(expires=ExpressionWrapper(
        F('borrowed_date') + F('days'), output_field=DateField())).filter(expires__lte=timezone.now(), returned=False)


class AddSubscription(generics.CreateAPIView):
    serializer_class = SubscriptionSubsSerializers
    queryset = Subscription.objects.all()
