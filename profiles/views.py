from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Profile
from .serializers import ProfileSerializer
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    # Allow users to get their own profile
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    # Allow users to edit their own profile
    @action(detail=False, methods=['patch'])
    def edit_profile(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # Retrieve user's next workshift
    @action(detail=False, methods=['get'])
    def next_workshift(self, request):
        profile = Profile.objects.get(user=request.user)
        booked_workshifts = profile.booked_workshifts.all()
        next_workshift = None
        for booked_workshift in booked_workshifts.order_by('start_time'):
            if booked_workshift.start_time > timezone.now():
                next_workshift = booked_workshift
                break
        # You'll need to create a serializer for WorkShift model and use it here
        # serializer = WorkShiftSerializer(next_workshift)
        # return Response(serializer.data)
        # Return the workshift directly for simplicity
        return Response({"next_workshift": str(next_workshift)})
