from rest_framework import serializers
from measures.models import Measure

# Measure Serializer

class MeasureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measure
        fields = '__all__'