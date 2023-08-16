from django.db import models

from industry.validators import nepali_date_validator


class IndustryWithoutGis(models.Model):
    reg_date = models.CharField(max_length=10, validators=[nepali_date_validator], blank=True, null=True)
    industry_reg_no = models.CharField(max_length=100, blank=True, null=True)
    industry_name = models.CharField(max_length=150, blank=True, null=True)
    owner_name = models.CharField(max_length=100, blank=True, null=True)
    industry_address = models.CharField(max_length=100, blank=True, null=True)
    fixed_capital = models.FloatField(default=0, blank=True, null=True)
    current_capital = models.FloatField(default=0, blank=True, null=True)
    total_capital = models.FloatField(default=0, blank=True, null=True)
    yearly_capacity = models.FloatField(default=0, blank=True, null=True)
    male = models.IntegerField(default=0, blank=True, null=True)
    female = models.IntegerField(default=0, blank=True, null=True)
    total_manpower = models.IntegerField(default=0, blank=True, null=True)
    
    def __str__(self):
        return self.industry_name