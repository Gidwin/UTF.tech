from .models import FoodListSerializer, FoodCategory
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Count, Q


class FoodViewSet(viewsets.ModelViewSet):
    queryset = FoodCategory.objects.all()
    serializer_class = FoodListSerializer

    @action(detail=False, url_path='api/v1/foods/')
    def get_correct_json(self, request):
        new_queryset = FoodCategory.objects.annotate(
            published_food_count=Count('food', filter=Q(food__is_publish=True))
        ).filter(published_food_count__gt=0)
        serializer = self.get_serializer(new_queryset, many=True)
        return Response(serializer.data) 