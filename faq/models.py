from django.db import models


class Faq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField(max_length=600)