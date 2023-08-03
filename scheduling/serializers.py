from rest_framework import serializers
from .models import WorkShift

class WorkShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkShift
        fields = ['id', 'event', 'location', 'is_booked', 'start_time', 'end_time',]
