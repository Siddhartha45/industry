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
            messages.success(request, 'Report Sent!')
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
            
            file_path = os.path.join(settings.MEDIA_ROOT, 'files', file.name)
            with open(file_path, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
                f.seek(0)
            
            df = pd.read_excel(file_path)
            
            for _, row in df.iterrows():
                
                industry_data = {}
                
                if 'industry_name' in df.columns:
                    industry_data['industry_name'] = row['industry_name']
                if 'industry_reg_no' in df.columns:
                    industry_data['industry_reg_no'] = row['industry_reg_no']
                # if 'reg_date' in df.columns:
                #     industry_data['reg_date'] = row['reg_date']
                if 'owner_name' in df.columns:
                    industry_data['owner_name'] = row['owner_name']
                if 'address' in df.columns:
                    industry_data['address'] = row['address']
                if 'telephone_number' in df.columns:
                    industry_data['telephone_number'] = row['telephone_number']
                if 'contact_person' in df.columns:
                    industry_data['contact_person'] = row['contact_person']
                if 'mobile_number' in df.columns:
                    industry_data['mobile_number'] = row['mobile_number']
                if 'district' in df.columns:
                    industry_data['district'] = row['district']
                if 'local_body' in df.columns:
                    industry_data['local_body'] = row['local_body']
                if 'latitude' in df.columns:
                    industry_data['latitude'] = row['latitude']
                if 'longitude' in df.columns:
                    industry_data['longitude'] = row['longitude']
                if 'product_description' in df.columns:
                    industry_data['product_description'] = row['product_description']
                
                #for assigning investment
                if 'investment' in df.columns:
                    investment_choice = row['investment']
                    if investment_choice == "साना" or investment_choice == "साना प्रा.फ.":
                        investment = "SMALL"
                    elif investment_choice == "लघु" or investment_choice == "लघु प्रा.फ":
                        investment = "MINIATURE"
                    elif investment_choice == "घरेलु" or investment_choice == "घरेलु  प्रा.फ.":
                        investment = "DOMESTIC"
                    elif investment_choice == "मझौला":
                        investment = "MEDIUM"
                    elif investment_choice == "ठुलो":
                        investment = "LARGE"
                    else:
                        investment = None
                else:
                    investment = None
                if investment is not None:
                    industry_data['investment'] = investment
                
                #for assigning product
                if 'industry_acc_product' in df.columns:
                    industry_acc_product_choice = row['industry_acc_product']
                    if industry_acc_product_choice == "कृषि मूलक":
                        industry_acc_product = "AF"
                    elif industry_acc_product_choice == "उत्पादन मूलक":
                        industry_acc_product = "MF"
                    elif industry_acc_product_choice == "सेवा मूलक":
                        industry_acc_product = "S"
                    else:
                        industry_acc_product = None
                else:
                    industry_acc_product = None
                if industry_acc_product is not None:
                    industry_data['industry_acc_product'] = industry_acc_product
                
                #for assigning status   
                if 'current_status' in df.columns:
                    current_status_choice = row['current_status']
                    if current_status_choice == "सकृय" or current_status_choice == "चालु":
                        current_status = "A"
                    elif current_status_choice == "निष्कृय":
                        current_status = "I"
                    else:
                        current_status = None
                else:
                    current_status = None
                if current_status is not None:
                    industry_data['current_status'] = current_status
            
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
                    industry_data['yearly_capacity'] = row['yearly_capacity']
                
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
            os.remove(file_path)
            messages.success(request, "The excel data is saved to database.")
    else:
        form = UploadFileForm()
            
    return render(request, 'report/fileupload.html', {'form': form})