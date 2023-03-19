from rest_framework import pagination
from rest_framework.response import Response
from myapps.event.models import EventModel, CategoryModel, EventRegistrationModel
from myapps.authentication.models import UserLoginInfo
from rest_framework import generics
from myapps.event.serializers.event import EventSearchSerializer, EventSearchValidationSerializer
from django.db.models import Q
from django.http import JsonResponse
from utils.constants import *
from utils.jwt.jwt_security import authenticate_login
from django.utils import timezone
from rest_framework.views import View

def GetDataApi(request):
    return JsonResponse({'cities': list(dict(CITIES).keys()), "categories": list(CategoryModel.objects.all().values())})

def event_detail_api(request):
    try:
        event = EventModel.objects.filter(id=request.GET.get('id'))
    except Exception:
        return JsonResponse({'message': "Invalid event Id."}, status=400)
    else:
        data = EventSearchSerializer(event, many=True).data
        return JsonResponse(data[0] if data else {})


class EventRegisterApi(generics.CreateAPIView):
    def post(self, request):
        input_data = request.data
        try:
            event = EventModel.objects.get(id=input_data['event_id'])
            user = UserLoginInfo.objects.get(id=input_data['user_id'])
        except Exception:
            return JsonResponse({'message': "Invalid event or user Id."}, status=400)
        else:
            if EventRegistrationModel.objects.filter(user=user, event=event).exists():
                event.booking_count = event.booking_count + 1
                event.save()
            else:
                event_registration = EventRegistrationModel.objects.create(user=user, event=event, is_paid=True)
            return JsonResponse({"message": "Event registered successfully."})


class EventSearchApi(generics.ListAPIView):
    model=EventModel
    queryset = EventModel.objects.all().order_by('event_date')
    serializer_class = EventSearchSerializer

    def filter(self, queryset, data):
        if 'query' in data and data['query']:
            queryset = queryset.filter(
                Q(title__icontains=data['query']) |
                Q(location__icontains=data['query']) | 
                Q(city__icontains=data['query']) | 
                Q(category__title__icontains=data['query']) | 
                Q(artists__user__name__icontains=data['query'])
            )
        if 'category' in data and data['category']:
            queryset = queryset.filter(category__title__in=[title.title() for title in data['category']])
        if 'city' in data and data['city']:
            queryset = queryset.filter(city__icontains=data['city'])
        if 'filter_type' in data:
            if data['filter_type'] == 'upcoming': 
                queryset = queryset.filter(event_date__gt=timezone.now())
            if data['filter_type'] == 'recomend':
                queryset = queryset.order_by('-booking_count')[:5]
        if 'order_by' in data and data['order_by'] in [f.name for f in EventModel._meta.get_fields()]:
            queryset = queryset.order_by(f"-{data['order_by']}" if 'sort' in data and data['sort'] == 'dec' else data['order_by'])
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        serializer = EventSearchValidationSerializer(data=self.request.GET)
        if serializer.is_valid():
            validated_data = serializer.data
            queryset = self.filter(queryset, validated_data)
            if 'limit' in validated_data:
                pagination.PageNumberPagination.page_size = validated_data['limit'] 
        return queryset