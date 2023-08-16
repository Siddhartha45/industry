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
import pandas as pd
from django.contrib import messages
from django.db import transaction


@transaction.atomic     # If error occurs while exporting data doesn't let any data be saved in the database 
@superadmin_required
def import_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            # Read the Excel file and specify data types
            dtype_mapping = {
                            'industry_reg_no': str, 
                            'reg_date': str,
                            'mobile_number': str, 
                            'telephone_number': str, 
                            'sex': str,
                            'caste': str,
                            'district': str,
                            'local_body': str,
                            'investment': str,
                            'industry_acc_product': str,
                            'current_status': str,
                            'ownership': str,
                            'raw_materials_source': str,
                            'current_running_capacity': str,
                            }
            df = pd.read_excel(file, dtype=dtype_mapping)
            
            for _, row in df.iterrows():
                
                industry_data = {}
                
                if 'industry_name' in df.columns:
                    industry_name = row['industry_name']
                    if pd.notna(industry_name):
                        industry_data['industry_name'] = industry_name
                    else:                                                   # Excel row not having industry_name value are not entered
                        continue
                
                if 'industry_reg_no' in df.columns:
                    industry_reg_no = row['industry_reg_no']
                    if pd.notna(industry_reg_no):
                        industry_data['industry_reg_no'] = industry_reg_no
                
                if 'reg_date' in df.columns:
                    reg_date = row['reg_date']
                    if pd.notna(reg_date):
                        try:
                            datetime_obj = pd.to_datetime(reg_date)
                            formatted_reg_date = datetime_obj.strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
                            industry_data['reg_date'] = formatted_reg_date
                        except ValueError:
                            industry_data['reg_date'] = None
                    
                if 'owner_name' in df.columns:
                    owner_name = row['owner_name']
                    if pd.notna(owner_name):
                        industry_data['owner_name'] = owner_name
                
                #sex
                if 'sex' in df.columns:
                    sex_choice = row['sex']
                    if pd.notna(sex_choice):  # Check if value is not NaN
                        sex_choice = sex_choice.strip()
                        if sex_choice == "Others":
                            industry_data['sex'] = "OTHERS"
                        elif sex_choice == "Male":
                            industry_data['sex'] = "MALE"
                        elif sex_choice == "Female":
                            industry_data['sex'] = "FEMALE"
                        else:
                            industry_data['sex'] = None
                
                #caste
                if 'caste' in df.columns:
                    caste_choice = row['caste']
                    if pd.notna(caste_choice):  # Check if value is not NaN
                        caste_choice = caste_choice.strip()
                        if caste_choice == "Dalit":
                            industry_data['caste'] = "DALIT"
                        elif caste_choice == "Janajati":
                            industry_data['caste'] = "JANAJATI"
                        elif caste_choice == "Others":
                            industry_data['caste'] = "OTHERS"
                        else:
                            industry_data['caste'] = None
                
                if 'owner_address' in df.columns:
                    address = row['owner_address']
                    if pd.notna(address):
                        industry_data['address'] = address
                
                if 'telephone_number' in df.columns:
                    telephone_number = row['telephone_number']
                    if pd.notna(telephone_number):
                        industry_data['telephone_number'] = telephone_number
                    
                if 'contact_person' in df.columns:
                    contact_person = row['contact_person']
                    if pd.notna(contact_person):
                        industry_data['contact_person'] = contact_person
                
                if 'mobile_number' in df.columns:
                    mobile_number = row['mobile_number']
                    if pd.notna(mobile_number):
                        industry_data['mobile_number'] = str(mobile_number)
                    
                if 'ward_no' in df.columns:
                    ward_no = row['ward_no']
                    if pd.notna(ward_no):
                        industry_data['ward_no'] = ward_no
                    
                if 'settlement' in df.columns:
                    settlement = row['settlement']
                    if pd.notna(settlement):
                        industry_data['settlement'] = settlement
                    
                if 'latitude' in df.columns:
                    latitude = row['latitude']
                    if pd.notna(latitude):
                        industry_data['latitude'] = latitude
                        
                if 'longitude' in df.columns:
                    longitude = row['longitude']
                    if pd.notna(longitude):
                        industry_data['longitude'] = longitude
                        
                if 'product_description' in df.columns:
                    product_description = row['product_description']
                    if pd.notna(product_description):
                        industry_data['product_description'] = product_description
                
                #for assigning district
                if 'district' in df.columns:
                    district_choice = row['district']   
                    if pd.notna(district_choice):  # Check if value is not NaN
                        district_choice = district_choice.strip()   # Removes the space from value in district column
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
                    if pd.notna(local__body_choice):  # Check if value is not NaN
                        local__body_choice = local__body_choice.strip()
                        if local__body_choice == "Apihimal":
                            industry_data['local_body'] = "APIHIMAL"
                        elif local__body_choice == "Kedarseu":
                            industry_data['local_body'] = "KEDARSU"
                        elif local__body_choice == "Bhimdatta":
                            industry_data['local_body'] = "BHIMDATTA"
                        elif local__body_choice == "Bithadchir":
                            industry_data['local_body'] = "BITTADCHIR"
                        elif local__body_choice == "Bungal":
                            industry_data['local_body'] = "BUNGAL"
                        elif local__body_choice == "Chabispathivera":
                            industry_data['local_body'] = "CHABBISPATHIVERA"
                        elif local__body_choice == "Chaurpati":
                            industry_data['local_body'] = "CHAURPATI"
                        elif local__body_choice == "Dhakari":
                            industry_data['local_body'] = "DHAKARI"
                        elif local__body_choice == "Dhangadhi":
                            industry_data['local_body'] = "DHANGADI"
                        elif local__body_choice == "Durgathali":
                            industry_data['local_body'] = "DURGATHALI"
                        elif local__body_choice == "JayaPrithivi":
                            industry_data['local_body'] = "JAYPRITHVI"
                        elif local__body_choice == "Khaptadchhanna":
                            industry_data['local_body'] = "KHAPTADCHATRA"
                        elif local__body_choice == "Laljhadi":
                            industry_data['local_body'] = "LALJHADI"
                        elif local__body_choice == "Lamkichuha":
                            industry_data['local_body'] = "LAMKICHUHA"
                        elif local__body_choice == "Masta":
                            industry_data['local_body'] = "MASTA"
                        elif local__body_choice == "SaiPaal":
                            industry_data['local_body'] = "SAIPAL"
                        elif local__body_choice == "Shuklaphanta":
                            industry_data['local_body'] = "SUKLAPHATA"
                        elif local__body_choice == "Surma":
                            industry_data['local_body'] = "SURMA"
                        elif local__body_choice == "Talkot":
                            industry_data['local_body'] = "TALKOT"
                        elif local__body_choice == "Thalara":
                            industry_data['local_body'] = "THALARA"
                        else:
                            industry_data['local_body'] = None
                
                #for assigning investment
                if 'investment' in df.columns:
                    investment_choice = row['investment']
                    if pd.notna(investment_choice):  # Check if value is not NaN
                        investment_choice = investment_choice.strip()
                        if investment_choice == "Small":
                            industry_data['investment'] = "SMALL"
                        elif investment_choice == "Micro":
                            industry_data['investment'] = "MINIATURE"
                        elif investment_choice == "Cottage":
                            industry_data['investment'] = "DOMESTIC"
                        elif investment_choice == "Medium":
                            industry_data['investment'] = "MEDIUM"
                        elif investment_choice == "Large":
                            industry_data['investment'] = "LARGE"
                        else:
                            industry_data['investment'] = None
                
                #for assigning product
                if 'industry_acc_product' in df.columns:
                    industry_acc_product_choice = row['industry_acc_product']
                    if pd.notna(industry_acc_product_choice):  # Check if value is not NaN
                        industry_acc_product_choice = industry_acc_product_choice.strip()
                        if industry_acc_product_choice == "Energy":
                            industry_data['industry_acc_product'] = "E"
                        elif industry_acc_product_choice == "Manufacturing":
                            industry_data['industry_acc_product'] = "MF"
                        elif industry_acc_product_choice == "Agricultural":
                            industry_data['industry_acc_product'] = "AF"
                        elif industry_acc_product_choice == "Mineral":
                            industry_data['industry_acc_product'] = "MI"
                        elif industry_acc_product_choice == "Infrastructure":
                            industry_data['industry_acc_product'] = "I"
                        elif industry_acc_product_choice == "Tourism":
                            industry_data['industry_acc_product'] = "T"
                        elif industry_acc_product_choice == "IC":
                            industry_data['industry_acc_product'] = "Ic"
                        elif industry_acc_product_choice == "Service":
                            industry_data['industry_acc_product'] = "S"
                        elif industry_acc_product_choice == "Others":
                            industry_data['industry_acc_product'] = "O"
                        else:
                            industry_data['industry_acc_product'] = None
                
                #for assigning status   
                if 'current_status' in df.columns:
                    current_status_choice = row['current_status']
                    if pd.notna(current_status_choice):  # Check if value is not NaN
                        current_status_choice = current_status_choice.strip()
                        if current_status_choice == "Active":
                            industry_data['current_status'] = "A"
                        elif current_status_choice == "Inactive":
                            industry_data['current_status'] = "I"
                        else:
                            industry_data['current_status'] = None
                    
                #for assigning ownership   
                if 'ownership' in df.columns:
                    ownership_choice = row['ownership']
                    if pd.notna(ownership_choice):  # Check if value is not NaN
                        ownership_choice = ownership_choice.strip()
                        if ownership_choice == "Private":
                            industry_data['ownership'] = "PRIVATE"
                        elif ownership_choice == "Partnership":
                            industry_data['ownership'] = "PARTNERSHIP"
                        else:
                            industry_data['ownership'] = None
                    
                #for assigning source of raw materials   
                if 'raw_materials_source' in df.columns:
                    source_of_raw_materials_choice = row['raw_materials_source']
                    if pd.notna(source_of_raw_materials_choice):  # Check if value is not NaN
                        source_of_raw_materials_choice = source_of_raw_materials_choice.strip()
                        if source_of_raw_materials_choice == "Local":
                            industry_data['raw_material_source'] = "LOCAL"
                        elif source_of_raw_materials_choice == "Imported":
                            industry_data['raw_material_source'] = "IMPORTED"
                        else:
                            industry_data['raw_material_source'] = None
                    
                #for assigning current running capacity
                if 'current_running_capacity' in df.columns:
                    current_running_capacity_choice = row['current_running_capacity']
                    if pd.notna(current_running_capacity_choice):  # Check if value is not NaN
                        current_running_capacity_choice = current_running_capacity_choice.strip()
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
                    product_service_name = row['product_service_name']
                    if pd.notna(product_service_name):
                        industry_data['product_service_name'] = product_service_name
                    
                if 'machinery_tool' in df.columns:
                    machinery_tool = row['machinery_tool']
                    if pd.notna(machinery_tool):
                        industry_data['machinery_tool'] = machinery_tool
                
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
                    
                if 'skilled' in df.columns:
                    skilled_value = row['skilled'] if pd.notnull(row['skilled']) else 0
                    try:
                        skilled_value = int(skilled_value)
                    except ValueError:
                        skilled_value = 0
                    industry_data['skillfull'] = skilled_value
                    
                if 'unskilled' in df.columns:
                    unskilled_value = row['unskilled'] if pd.notnull(row['unskilled']) else 0
                    try:
                        unskilled_value = int(unskilled_value)
                    except ValueError:
                        unskilled_value = 0
                    industry_data['unskilled'] = unskilled_value
                    
                if 'foreign' in df.columns:
                    foreign_value = row['foreign'] if pd.notnull(row['foreign']) else 0
                    try:
                        foreign_value = int(foreign_value)
                    except ValueError:
                        foreign_value = 0
                    industry_data['foreign'] = foreign_value
                    
                if 'domestic' in df.columns:
                    domestic_value = row['domestic'] if pd.notnull(row['domestic']) else 0
                    try:
                        domestic_value = int(domestic_value)
                    except ValueError:
                        domestic_value = 0
                    industry_data['indigenous'] = domestic_value
                    
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
                    total_capital_value = str(total_capital_value).replace(',', '') # Remove commas from the number
                    try:
                        industry_data['total_capital'] = float(total_capital_value)
                    except ValueError:
                        industry_data['total_capital'] = 0
                
                if industry_data:
                    industry = Industry(**industry_data)
                    if hasattr(industry, 'total_manpower'):
                        industry.total_manpower = total_manpower
                    industry.save() 
            messages.success(request, "The excel data is saved to database.")
    else:
        form = UploadFileForm()
            
    return render(request, 'report/fileupload.html', {'form': form})