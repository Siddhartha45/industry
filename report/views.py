from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from fdip.decorators import superadmin_required, admin_required


@admin_required
def report_problem(request):
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, 'Report Sent')
            return redirect('report')
    else:
        form = ReportForm()
    if form.errors:
        for field in form:
            if field.errors:
                messages.error(request, 'Please fill the message field and select the issue image accordingly!.')
                break
    context = {'form': form}
    return render(request, 'report/reportproblem.html', context)


@superadmin_required
def report_list(request):
    data = {
        'report': Report.objects.all()
    }
    return render(request, 'report/reportview.html', data)


@superadmin_required
def report_delete(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.delete()
    messages.info(request, "Report deleted")
    return redirect('report-list')


@superadmin_required
def report_show(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    context = {'report': report}
    return render(request, 'report/show.html', context)




from .forms import UploadFileForm   
from industry.models import Industry
import csv 
import pandas as pd
from django.contrib import messages
import re
import os
from django.conf import settings

@superadmin_required
def import_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            df = pd.read_excel(file)
            
            for _, row in df.iterrows():
                
                industry_data = {}
                
                if 'industry_name' in df.columns:
                    industry_data['industry_name'] = row['industry_name']
                if 'industry_reg_no' in df.columns:
                    industry_data['industry_reg_no'] = row['industry_reg_no']
                if 'reg_date' in df.columns:
                    industry_data['reg_date'] = row['reg_date']
                if 'owner_name' in df.columns:
                    industry_data['owner_name'] = row['owner_name']
                
                #sex
                if 'sex' in df.columns:
                    sex_choice = row['sex']
                    if sex_choice == "Others":
                        industry_data['sex'] = "OTHERS"
                    elif sex_choice == "Dalit":
                        industry_data['sex'] = "DALIT"
                    elif sex_choice == "Janajati":
                        industry_data['sex'] = "JANAJATI"
                    else:
                        industry_data['sex'] = None
                
                #caste
                if 'caste' in df.columns:
                    caste_choice = row['caste']
                    if caste_choice == "Male":
                        industry_data['caste'] = "MALE"
                    elif caste_choice == "Female":
                        industry_data['caste'] = "FEMALE"
                    elif caste_choice == "Others":
                        industry_data['caste'] = "OTHERS"
                    else:
                        industry_data['caste'] = None
                
                if 'owner_address' in df.columns:
                    industry_data['address'] = row['owner_address']
                if 'telephone_number' in df.columns:
                    industry_data['telephone_number'] = row['telephone_number']
                if 'contact_person' in df.columns:
                    industry_data['contact_person'] = row['contact_person']
                if 'mobile_number' in df.columns:
                    industry_data['mobile_number'] = row['mobile_number']
                if 'ward_no' in df.columns:
                    industry_data['ward_no'] = row['ward_no']
                if 'settlement' in df.columns:
                    industry_data['settlement'] = row['settlement']
                if 'latitude' in df.columns:
                    industry_data['latitude'] = row['latitude']
                if 'longitude' in df.columns:
                    industry_data['longitude'] = row['longitude']
                if 'product_description' in df.columns:
                    industry_data['product_description'] = row['product_description']
                
                #for assigning district
                if 'district' in df.columns:
                    district_choice = row['district']
                    if district_choice == "Kailali":
                        industry_data['district'] = "KAILALI"
                    elif district_choice == "Kanchanpur":
                        industry_data['district'] = "KANCHANPUR"
                    elif district_choice == "Dadeldhura":
                        industry_data['district'] = "DADELDHURA"
                    elif district_choice == "Doti":
                        industry_data['district'] = "DOTI"
                    elif district_choice == "Achham":
                        industry_data['district'] = "ACHHAM"
                    elif district_choice == "Bajura":
                        industry_data['district'] = "BAJURA"
                    elif district_choice == "Bajhang":
                        industry_data['district'] = "BAJHANG"
                    elif district_choice == "Baitadi":
                        industry_data['district'] = "BAITADI"
                    elif district_choice == "Darchula":
                        industry_data['district'] = "DARCHULA"
                    else:
                        industry_data['district'] = None
                
                #for assigning local body
                if 'local_body' in df.columns:
                    local__body_choice = row['local_body']
                    if local__body_choice == "Apihimal":
                        industry_data['local_body'] = "APIHIMAL"
                    elif local__body_choice == "Kedarseu":
                        industry_data['local_body'] = "KEDARSU"
                    else:
                        industry_data['local_body'] = None
                
                #for assigning investment
                if 'investment' in df.columns:
                    investment_choice = row['investment']
                    if investment_choice == "small":
                        industry_data['investment'] = "SMALL"
                    elif investment_choice == "micro":
                        industry_data['investment'] = "MINIATURE"
                    elif investment_choice == "domestic":
                        industry_data['investment'] = "DOMESTIC"
                    elif investment_choice == "medium":
                        industry_data['investment'] = "MEDIUM"
                    elif investment_choice == "large":
                        industry_data['investment'] = "LARGE"
                    else:
                        industry_data['investment'] = None
                else:
                    industry_data['investment'] = None
                
                #for assigning product
                if 'industry_acc_product' in df.columns:
                    industry_acc_product_choice = row['industry_acc_product']
                    if industry_acc_product_choice == "energy":
                        industry_data['industry_acc_product'] = "E"
                    elif industry_acc_product_choice == "manufacturing":
                        industry_data['industry_acc_product'] = "MF"
                    elif industry_acc_product_choice == "agriculture":
                        industry_data['industry_acc_product'] = "AF"
                    elif industry_acc_product_choice == "mineral":
                        industry_data['industry_acc_product'] = "MI"
                    elif industry_acc_product_choice == "infrastructure":
                        industry_data['industry_acc_product'] = "I"
                    elif industry_acc_product_choice == "tourism":
                        industry_data['industry_acc_product'] = "T"
                    elif industry_acc_product_choice == "IC":
                        industry_data['industry_acc_product'] = "Ic"
                    elif industry_acc_product_choice == "service":
                        industry_data['industry_acc_product'] = "S"
                    elif industry_acc_product_choice == "others":
                        industry_data['industry_acc_product'] = "O"
                    else:
                        industry_data['industry_acc_product'] = None
                else:
                    industry_data['industry_acc_product'] = None
                
                #for assigning status   
                if 'current_status' in df.columns:
                    current_status_choice = row['current_status']
                    if current_status_choice == "active":
                        industry_data['current_status'] = "A"
                    elif current_status_choice == "inactive":
                        industry_data['current_status'] = "I"
                    else:
                        industry_data['current_status'] = None
                else:
                    industry_data['current_status'] = None
                    
                #for assigning ownership   
                if 'ownership' in df.columns:
                    ownership_choice = row['ownership']
                    if ownership_choice == "Private":
                        industry_data['ownership'] = "PRIVATE"
                    elif ownership_choice == "Partnership":
                        industry_data['ownership'] = "PARTNERSHIP"
                    else:
                        industry_data['ownership'] = None
                else:
                    industry_data['ownership'] = None
                    
                #for assigning source of raw materials   
                if 'raw_materials_source' in df.columns:
                    source_of_raw_materials_choice = row['raw_materials_source']
                    if source_of_raw_materials_choice == "Local":
                        industry_data['raw_material_source'] = "LOCAL"
                    elif source_of_raw_materials_choice == "Imported":
                        industry_data['raw_material_source'] = "IMPORTED"
                    else:
                        industry_data['raw_material_source'] = None
                else:
                    industry_data['raw_material_source'] = None
                    
                #for assigning current running capacity
                if 'current_running_capacity' in df.columns:
                    current_running_capacity_choice = row['current_running_capacity']
                    if current_running_capacity_choice == "50-70":
                        industry_data['current_running_capacity'] = "B"
                    elif current_running_capacity_choice == "70-100":
                        industry_data['current_running_capacity'] = "A"
                    elif current_running_capacity_choice == "50":
                        industry_data['current_running_capacity'] = "C"
                    elif current_running_capacity_choice == "25":
                        industry_data['current_running_capacity'] = "D"
                    else:
                        industry_data['current_running_capacity'] = None
            
            
                if 'product_service_name' in df.columns:
                    industry_data['product_service_name'] = row['product_service_name']
                
                if 'male' in df.columns:
                    male_value = row['male'] if pd.notnull(row['male']) else 0
                    try:
                        male_value = int(male_value)
                    except ValueError:
                        male_value = 0
                    industry_data['male'] = male_value
                total_manpower = 0
                
                if 'female' in df.columns:
                    female_value = row['female'] if pd.notnull(row['female']) else 0
                    try:
                        female_value = int(female_value)
                    except ValueError:
                        female_value = 0
                    industry_data['female'] = female_value
                
                    total_manpower = female_value + male_value
                    
                if 'yearly_capacity' in df.columns:
                    yearly_capacity_value = row['yearly_capacity'] if pd.notnull(row['yearly_capacity']) else 0
                    yearly_capacity_value = str(yearly_capacity_value).replace(',', '')  # Remove commas from the number
                    try:
                        industry_data['yearly_capacity'] = float(yearly_capacity_value)
                    except ValueError:
                        industry_data['yearly_capacity'] = 0
                
                if 'fixed_capital' in df.columns:
                    fixed_capital_value = row['fixed_capital'] if pd.notnull(row['fixed_capital']) else 0
                    fixed_capital_value = str(fixed_capital_value).replace(',', '')  # Remove commas from the number
                    try:
                        industry_data['fixed_capital'] = float(fixed_capital_value)
                    except ValueError:
                        industry_data['fixed_capital'] = 0
                
                if 'current_capital' in df.columns:
                    current_capital_value = row['current_capital'] if pd.notnull(row['current_capital']) else 0
                    current_capital_value = str(current_capital_value).replace(',', '')  # Remove commas from the number
                    try:
                        industry_data['current_capital'] = float(current_capital_value)   
                    except ValueError:
                        industry_data['current_capital'] = 0
                    
                if 'total_capital' in df.columns:
                    total_capital_value = row['total_capital'] if pd.notnull(row['total_capital']) else 0
                    total_capital_value = str(total_capital_value).replace(',', '')  # Remove commas from the number
                    try:
                        industry_data['total_capital'] = float(total_capital_value)
                    except ValueError:
                        industry_data['total_capital'] = 0
                
                industry = Industry(**industry_data)
                if hasattr(industry, 'total_manpower'):
                    industry.total_manpower = total_manpower
                
                industry.save() 
            messages.success(request, "The excel data is saved to database.")
    else:
        form = UploadFileForm()
            
    return render(request, 'report/fileupload.html', {'form': form})