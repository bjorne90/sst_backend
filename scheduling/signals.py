from django.dispatch import receiver
from booking.signals import booking_canceled
from scheduling.models import WorkShift

@receiver(booking_canceled)
def update_workshift(sender, **kwargs):
    # Update the related WorkShift when a booking is canceled
    booking_instance = kwargs['instance']
    try:
        workshift = WorkShift.objects.get(id=booking_instance.workshift.id)
        workshift.is_booked = False
        workshift.save()
    except WorkShift.DoesNotExist:
        pass
