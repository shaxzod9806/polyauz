from django.db import models

# Create your models here
SMS_CHOICES = (
    (1, 'create_user'),
    (2, 'reset_password'),
    (3, 'notification'),
    (4, 'news'),
)

SENT_OPTIONS = (
    (0, 'not_sent'),
    (1, "sent")
)


class SMS(models.Model):
    phone_number = models.CharField(null=True, max_length=255)
    text = models.CharField(null=True, max_length=255)
    sms_type = models.PositiveSmallIntegerField(choices=SMS_CHOICES, default=1)
    is_sent = models.PositiveSmallIntegerField(choices=SENT_OPTIONS, default=0)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)


class Country(models.Model):
    country_name = models.CharField(null=True, max_length=255)

# class CountryLangs(models.Model):

