import pandas as pd

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from .models import Report
from .forms import ReportForm
from .forms import UploadFileForm
from .excel_data_mapping import *

from fdip.decorators import superadmin_required, admin_required
from industry.models import Industry
from industry_without_gis.views import without_gis_data_import


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


@transaction.atomic     # If error occurs while exporting data doesn't let any data be saved in the database 
@superadmin_required
def import_file(request):
    """for importing excel data to database"""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if 'gis_file_upload' in request.POST:
            if form.is_valid():
                file = request.FILES['file']
                if not file.name.endswith('.xlsx'):
                    messages.error(request, 'Invalid file format. Please upload correct Excel File with proper data!')
                else:
                    gis_data_import(request, file)
        elif 'without_gis_file_upload' in request.POST:
            if form.is_valid():
                file = request.FILES['file']
                if not file.name.endswith('.xlsx'):
                    messages.error(request, 'Invalid file format. Please upload correct Excel File with proper data!')
                else:
                    without_gis_data_import(request, file)
    else:
        form = UploadFileForm()
    return render(request, 'report/fileupload.html', {'form': form})


def gis_data_import(request, file):
    """function for exporting excel data of industries with gis info to Industry model"""
    df = pd.read_excel(file, dtype=dtype_mapping)
    for _, row in df.iterrows():
        industry_data = {}
        
        if 'industry_name' in df.columns:
            industry_name = row['industry_name']
            if pd.notna(industry_name):
                industry_data['industry_name'] = industry_name
            else:                                                   # Excel row not having industry_name value are not entered
                continue

        if 'reg_date' in df.columns:
            reg_date = row['reg_date']
            if pd.notna(reg_date):
                try:
                    datetime_obj = pd.to_datetime(reg_date)
                    formatted_reg_date = datetime_obj.strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
                    industry_data['reg_date'] = formatted_reg_date
                except ValueError:
                    industry_data['reg_date'] = None
                    
        column_names = ['industry_reg_no', 'owner_name', 'address', 'telephone_number', 'contact_person', 'mobile_number', 'ward_no', 
                        'settlement', 'latitude', 'longitude', 'product_description','product_service_name', 'machinery_tool']
        for column_name in column_names:
            if column_name in df.columns:
                value = row[column_name]
                if pd.notna(value):
                    industry_data[column_name] = value
                    
        column_mappings = {
            'sex': sex_mapping,
            'caste': caste_mapping,
            'investment': investment_mapping,
            'industry_acc_product': industry_acc_product_mapping,
            'current_status': current_status_mapping,
            'ownership': ownership_mapping,
            'raw_material_source': raw_materials_source_mapping,
            'current_running_capacity': current_running_capacity_mapping,
            'district': district_mapping,
            'local_body': local_body_mapping,
        }
        for column, mapping in column_mappings.items():
            if column in df.columns:
                choice = row[column]
                if pd.notna(choice):
                    industry_data[column] = mapping.get(choice.strip(), None)

        manpower_columns = ['male', 'female', 'skillfull', 'unskilled', 'indigenous', 'foreign']
        for manpower_column in manpower_columns:
            if manpower_column in df.columns:
                manpower_value = row[manpower_column] if pd.notna(row[manpower_column]) else 0
                try:
                    int_manpower_value = int(manpower_value)
                except ValueError:
                    int_manpower_value = 0
                industry_data[manpower_column] = int_manpower_value
        # Stores value of total manpower
        total_manpower = industry_data['male'] + industry_data['female']
        
        capital_columns = ['yearly_capacity', 'fixed_capital', 'current_capital', 'total_capital']
        for capital_column in capital_columns:
            if capital_column in df.columns:
                capital_value = row[capital_column] if pd.notna(row[capital_column]) else 0
                clean_capital_value = str(capital_value).replace(',', '')  # Remove commas from the number
                try:
                    float_capital_value = float(clean_capital_value)
                except ValueError:
                    float_capital_value = 0
                industry_data[capital_column] = float_capital_value
        
        if industry_data:
            industry = Industry(**industry_data)
            if hasattr(industry, 'total_manpower'):
                industry.total_manpower = total_manpower
            industry.save() 
    return messages.success(request, "The excel data is saved to database.")