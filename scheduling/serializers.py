from rest_framework import serializers
from .models import WorkShift

class WorkShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkShift
        fields = ['id', 'event', 'location', 'shift_details', 'start_time', 'end_time', 'is_booked', 'role',]
