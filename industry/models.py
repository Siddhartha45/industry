from django.db import models
from fdip import commons


class Industry(models.Model):
    #Industry Details
    industry_name = models.CharField(max_length=150)
    industry_reg_no = models.CharField(max_length=100, unique=True, null=True, blank=True)
    reg_date = models.DateField(null=True, blank=True)
    owner_name = models.CharField(max_length=100, null=True, blank=True)
    sex = models.CharField(max_length=6, choices=commons.SEX_CHOICES)
    caste = models.CharField(max_length=8, choices=commons.CASTE_CHOICES)
    address = models.CharField(max_length=100, null=True, blank=True)
    telephone_number = models.CharField(max_length=15, null=True, blank=True)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    #Industry Address
    district = models.CharField(max_length=100, null=True, blank=True)
    local_body = models.CharField(max_length=100, null=True, blank=True)
    ward_no = models.CharField(max_length=100, null=True, blank=True)
    settlement = models.CharField(max_length=100, null=True, blank=True)
    #map
    latitude = models.CharField(max_length=100, null=True, blank=True)
    longitude = models.CharField(max_length=100, null=True, blank=True)
    product_description = models.TextField(max_length=600, null=True, blank=True)
    investment = models.CharField(max_length=9, choices=commons.INVESTMENT_CHOICES)
    ownership = models.CharField(max_length=11, choices=commons.OWNERSHIP_CHOICES)
    raw_material_source = models.CharField(max_length=8, choices=commons.MATERIAL_SOURCE)
    industry_acc_product = models.CharField(max_length=50, choices=commons.TYPE_OF_PRODUCT)
    current_status = models.CharField(max_length=8, choices=commons.CURRENT_STATUS)
    current_running_capacity = models.CharField(max_length=1, choices=commons.CAPACITY)
    machinery_tool = models.TextField(max_length=600, null=True, blank=True)
    product_service_name = models.CharField(max_length=100, null=True, blank=True)
    yearly_capacity = models.CharField(max_length=100, null=True, blank=True)
    #Employment
    total_manpower = models.IntegerField(null=True, blank=True)
    skillfull = models.IntegerField(null=True, blank=True)
    unskilled = models.IntegerField(null=True, blank=True)
    indigenous = models.IntegerField(null=True, blank=True)
    foreign = models.IntegerField(null=True, blank=True)
    male = models.IntegerField(null=True, blank=True)
    female = models.IntegerField(null=True, blank=True)
    fixed_capital = models.CharField(max_length=255, null=True, blank=True)
    current_capital = models.CharField(max_length=255, null=True, blank=True)
    total_capital = models.CharField(max_length=255, null=True, blank=True)
    #industry_photo = models.ImageField(upload_to='images', blank=True, null=True)
            
    def __str__(self):
        return self.industry_name
    
    
class IndustryPhoto(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='industry_photo')
    photo = models.ImageField(upload_to='images', null=True, blank=True)