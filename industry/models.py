from django.db import models
from fdip import commons
from .validators import nepali_date_validator


class Industry(models.Model):
    """Model for Industry"""
    
    #Industry Details
    industry_name = models.CharField(max_length=150)
    industry_reg_no = models.CharField(max_length=100, blank=True, null=True)
    reg_date = models.CharField(max_length=10, blank=True, null=True, validators=[nepali_date_validator])
    owner_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=6, choices=commons.SEX_CHOICES, blank=True, null=True)
    caste = models.CharField(max_length=8, choices=commons.CASTE_CHOICES, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    telephone_number = models.CharField(max_length=15, blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    #Industry Address
    district = models.CharField(max_length=20, choices=commons.DISTRICT_CHOICES, blank=True, null=True)
    local_body = models.CharField(max_length=100, choices=commons.ALL_LOCALBODY_CHOICES, blank=True, null=True)
    ward_no = models.CharField(max_length=100, blank=True, null=True)
    settlement = models.CharField(max_length=100, blank=True, null=True)
    #map
    latitude = models.CharField(max_length=100, blank=True)
    longitude = models.CharField(max_length=100, blank=True)
    product_description = models.TextField(max_length=600, blank=True, null=True)
    investment = models.CharField(max_length=9, choices=commons.INVESTMENT_CHOICES, blank=True, null=True)
    ownership = models.CharField(max_length=11, choices=commons.OWNERSHIP_CHOICES, blank=True, null=True)
    raw_material_source = models.CharField(max_length=8, choices=commons.MATERIAL_SOURCE, blank=True, null=True)
    industry_acc_product = models.CharField(max_length=50, choices=commons.TYPE_OF_PRODUCT, blank=True, null=True)
    others_text = models.CharField(max_length=255, blank=True, null=True)
    current_status = models.CharField(max_length=8, choices=commons.CURRENT_STATUS, blank=True, null=True)
    current_running_capacity = models.CharField(max_length=1, choices=commons.CAPACITY, blank=True, null=True)
    machinery_tool = models.TextField(max_length=600, blank=True, null=True)
    product_service_name = models.CharField(max_length=100, blank=True, null=True)
    yearly_capacity = models.FloatField(default=0, blank=True, null=True)
    #Employment
    total_manpower = models.IntegerField(default=0, blank=True, null=True)
    skillfull = models.IntegerField(default=0, blank=True, null=True)
    unskilled = models.IntegerField(default=0, blank=True, null=True)
    indigenous = models.IntegerField(default=0, blank=True, null=True)
    foreign = models.IntegerField(default=0, blank=True, null=True)
    male = models.IntegerField(default=0, blank=True, null=True)
    female = models.IntegerField(default=0, blank=True, null=True)
    fixed_capital = models.FloatField(default=0, blank=True, null=True)
    current_capital = models.FloatField(default=0, blank=True, null=True)
    total_capital = models.FloatField(default=0, blank=True, null=True)

    def __str__(self):
        return self.industry_name
    
    def save(self, *args, **kwargs):
        if self.industry_acc_product != 'O':
            self.others_text = None
        super().save(*args, **kwargs)
        
    
class IndustryPhoto(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='industry_photo')
    photo = models.ImageField(upload_to='images', null=True, blank=True)