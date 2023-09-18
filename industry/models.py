from django.db import models

from .validators import nepali_date_validator
from .utils import get_choice_display_value

from fdip import commons


class Industry(models.Model):
    """Model for Industry"""
    created_on = models.DateTimeField(auto_now_add=True)    
    #Industry Details
    industry_name = models.CharField(max_length=255)
    industry_reg_no = models.CharField(max_length=255, blank=True, null=True)
    reg_date = models.CharField(max_length=20, blank=True, null=True, validators=[nepali_date_validator])
    owner_name = models.CharField(max_length=255)
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
        """Overriding save method so that others text is only stored for those industries whose 
        industry_acc_product is selected as others"""
        if self.industry_acc_product != 'O':
            self.others_text = None
        super().save(*args, **kwargs)
    
    @property
    def sex_display_value(self):
        return get_choice_display_value(self.sex, commons.SEX_CHOICES)
    
    @property
    def caste_display_value(self):
        return get_choice_display_value(self.caste, commons.CASTE_CHOICES)
    
    @property
    def investment_display_value(self):
        return get_choice_display_value(self.investment, commons.INVESTMENT_CHOICES)
    
    @property
    def industry_acc_product_display_value(self):
        return get_choice_display_value(self.industry_acc_product, commons.TYPE_OF_PRODUCT)
    
    @property
    def ownership_display_value(self):
        return get_choice_display_value(self.ownership, commons.OWNERSHIP_CHOICES)
    
    @property
    def district_display_value(self):
        return get_choice_display_value(self.district, commons.DISTRICT_CHOICES)
    
    @property
    def local_body_display_value(self):
        return get_choice_display_value(self.local_body, commons.ALL_LOCALBODY_CHOICES)


class IndustryPhoto(models.Model):
    """Model for storing industry photos"""
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='industry_photo')
    photo = models.ImageField(upload_to='images', null=True, blank=True)