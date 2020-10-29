from measures.models import Measure
from rest_framework import viewsets, permissions
from .serializers import MeasureSerializer

# Measure Viewset

class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.all()
    permissions_classes = [
        permissions.AllowAny
    ]
    serializer_class = MeasureSerializer