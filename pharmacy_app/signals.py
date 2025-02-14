from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from pharmacy_app.models import Staff


@receiver(post_save, sender=User)
def create_staff_profile(sender, instance, created, **kwargs):
    if created:
        Staff.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_staff_profile(sender, instance, **kwargs):
    instance.staff.save()
