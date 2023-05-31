from django.db import models
from accounts.models import CustomUser


class Report(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='report')
    message = models.TextField(max_length=600)
    issue_image = models.ImageField(upload_to='images', blank=True)