import pandas as pd
import xlwt
import csv

from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.serializers import serialize
from django.db.models import Sum

from .models import IndustryWithoutGis
from .forms import IndustryWithoutGisModelForm

from fdip import commons
from fdip.decorators import superadmin_required
from .excel_name import *
from industry.views import session_local_delete
from report.excel_data_mapping import (
    dtype_mapping, sex_mapping, caste_mapping, investment_mapping, industry_acc_product_mapping, current_status_mapping, 
    ownership_mapping, raw_materials_source_mapping, current_running_capacity_mapping, district_mapping, local_body_mapping
    )


def industry_without_gis_home(request):
    session_local_delete(request)
    
    selected_district = request.GET.get('district')
    
    if selected_district:
        data_filter = IndustryWithoutGis.objects.filter(district=selected_district)
    else:
        data_filter = IndustryWithoutGis.objects.all()

    unique_districts = IndustryWithoutGis.objects.values_list('district', flat=True).distinct()

    district_count = unique_districts.count()
    
    total_industry = data_filter.count()
    #for showing chart acc to investment
    miniature = data_filter.filter(investment='MINIATURE').count()
    domestic = data_filter.filter(investment='DOMESTIC').count()
    small = data_filter.filter(investment='SMALL').count()
    medium = data_filter.filter(investment='MEDIUM').count()
    large = data_filter.filter(investment='LARGE').count()
    #for showing chart acc to ownership
    private = data_filter.filter(ownership='PRIVATE').count()
    partnership = data_filter.filter(ownership='PARTNERSHIP').count()
    #for showing chart acc to current status
    active = data_filter.filter(current_status='A').count()
    inactive = data_filter.filter(current_status='I').count()
    #for showing chart acc to type of product
    energy = data_filter.filter(industry_acc_product='E').count()
    manufacturing = data_filter.filter(industry_acc_product='MF').count()
    ag = data_filter.filter(industry_acc_product='AF').count()
    mineral = data_filter.filter(industry_acc_product='MI').count()
    infra = data_filter.filter(industry_acc_product='I').count()
    tourism = data_filter.filter(industry_acc_product='T').count()
    it = data_filter.filter(industry_acc_product='IC').count()
    service = data_filter.filter(industry_acc_product='S').count()
    others = data_filter.filter(industry_acc_product='O').count()
    #for showing chart acc to employment
    total_manpower = data_filter.aggregate(total=Sum('total_manpower'))['total']
    skilled = data_filter.aggregate(total=Sum('skillfull'))['total']
    unskilled = data_filter.aggregate(total=Sum('unskilled'))['total']
    indigenous = data_filter.aggregate(total=Sum('indigenous'))['total']
    foreign = data_filter.aggregate(total=Sum('foreign'))['total']
    male = data_filter.aggregate(total=Sum('male'))['total']
    female = data_filter.aggregate(total=Sum('female'))['total']

    context = {
                'unique_districts':unique_districts,
                'district_count':district_count,
                
                'total_industry': total_industry,
                'miniature': miniature,
                'domestic': domestic,
                'small': small,
                'medium': medium,
                'large': large,
                'private': private,
                'partnership': partnership,
                'active': active,
                'inactive': inactive,
                'energy': energy,
                'manufacturing': manufacturing,
                'ag': ag,
                'mineral': mineral,
                'infra': infra,
                'tourism': tourism,
                'it': it,
                'service': service,
                'others': others,
                'total_manpower': total_manpower,
                'skilled': skilled,
                'unskilled': unskilled,
                'indigenous': indigenous,
                'foreign': foreign,
                'male': male,
                'female': female,
                }
    if request.user.is_authenticated:
        return render(request, 'industry_without_gis/industry_without_gis_graph.html', context)
    else:
        return render(request, 'public/industry_without_gis_public.html', context)

@superadmin_required
def without_gis_data_import(request, file):
    """function for exporting excel data of industries without gis to IndutryWithoutGis model"""
    df = pd.read_excel(file, dtype=dtype_mapping)
    df.columns = df.columns.str.strip()     # Removes blank spaces from column names

    for _, row in df.iterrows():
        industry_data = {}
        
        if industry_name in df.columns:
            industry_name_value = row[industry_name]
            if pd.notna(industry_name_value):
                industry_data['industry_name'] = industry_name_value
            else:                                                   # Excel row not having industry_name value are not entered
                continue

        if reg_date in df.columns:
            reg_date_value = row[reg_date]
            if pd.notna(reg_date_value):
                try:
                    datetime_obj = pd.to_datetime(reg_date_value)
                    formatted_reg_date = datetime_obj.strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
                    industry_data['reg_date'] = formatted_reg_date
                except ValueError:
                    industry_data['reg_date'] = None

        column_names = {
            'industry_reg_no': industry_reg_no, 'owner_name': owner_name, 'address': address, 
            'telephone_number': telephone_number, 'contact_person': contact_person, 
            'mobile_number': mobile_number, 'ward_no': ward_no, 'settlement': settlement, 
            'product_description': product_description, 'product_service_name': product_service_name, 
            'machinery_tool': machinery_tool
        }
        for k, v in column_names.items():
            if v in df.columns:
                value = row[v]
                if pd.notna(value):
                    industry_data[k] = value

        
        column_mappings = {
            'sex': (sex, sex_mapping),
            'caste': (caste, caste_mapping),
            'investment': (investment, investment_mapping),
            'industry_acc_product': (industry_acc_product, industry_acc_product_mapping),
            'current_status': (current_status, current_status_mapping),
            'ownership': (ownership, ownership_mapping),
            'raw_material_source': (raw_material_source, raw_materials_source_mapping),
            'current_running_capacity': (current_running_capacity, current_running_capacity_mapping),
            'district': (district, district_mapping),
            'local_body': (local_body, local_body_mapping),
        }
        for column, mapping in column_mappings.items():
            if mapping[0] in df.columns:
                choice = row[mapping[0]]
                if pd.notna(choice):
                    industry_data[column] = mapping[1].get(choice.strip(), None)

        manpower_columns = {
            'male': male, 'female': female, 'skillfull': skillfull, 
            'unskilled': unskilled, 'indigenous': indigenous, 
            'foreign': foreign
        }
        for k, v in manpower_columns.items():
            if v in df.columns:
                manpower_value = row[v] if pd.notna(row[v]) else 0
                try:
                    int_manpower_value = int(manpower_value)
                except ValueError:
                    int_manpower_value = 0
                industry_data[k] = int_manpower_value
        # Stores value of total manpower (if one of the column is missing returns 0)
        total_manpower = industry_data.get('male', 0) + industry_data.get('female', 0)
        
        capital_columns = {
            'yearly_capacity': yearly_capacity, 'fixed_capital': fixed_capital, 
            'current_capital': current_capital, 'total_capital': total_capital
        }
        for k, v in capital_columns.items():
            if v in df.columns:
                capital_value = row[v] if pd.notna(row[v]) else 0
                clean_capital_value = str(capital_value).replace(',', '')  # Remove commas from the number
                try:
                    float_capital_value = float(clean_capital_value)
                except ValueError:
                    float_capital_value = 0
                industry_data[k] = float_capital_value
        
        if industry_data:
            industry = IndustryWithoutGis(**industry_data)
            if hasattr(industry, 'total_manpower'):
                industry.total_manpower = total_manpower
            industry.save() 
    return messages.success(request, "The excel data is saved to database.")


@login_required
def without_gis_industry_list(request):
    all_localbody = commons.ALL_LOCALBODY_CHOICES
    if 'type' in request.session:
        investment_input = request.session.get('investment_input')
        product_input = request.session.get('product_input')
        district_input = request.session.get('district_input')
        local_input = request.session.get('local_input')

        if investment_input != 'None' and product_input != 'None' and district_input != 'None' and local_input != 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input, district__contains=district_input, local_body__contains=local_input)
        
        elif investment_input == 'None' and product_input == 'None' and district_input == 'None' and local_input == 'None':
            industries_queryset = IndustryWithoutGis.objects.all().order_by('-id')[:100]
        
        elif investment_input != 'None' and product_input == 'None' and district_input == 'None' and local_input == 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input) 
        
        elif investment_input == 'None' and product_input != 'None' and district_input == 'None' and local_input == 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(industry_acc_product__contains=product_input)
            
        elif investment_input == 'None' and product_input == 'None' and district_input != 'None' and local_input == 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(district__contains=district_input)
        
        elif investment_input == 'None' and product_input == 'None' and district_input == 'None' and local_input != 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(local_body__contains=local_input)
        
        elif investment_input != 'None' and product_input != 'None' and district_input == 'None' and local_input == 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, industry_acc_product__contains=product_input)
            
        elif investment_input != 'None' and product_input == 'None' and district_input != 'None' and local_input == 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, district__contains=district_input)
            
        elif investment_input != 'None' and product_input == 'None' and district_input == 'None' and local_input != 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, local_body__contains=local_input)
            
        elif investment_input != 'None' and product_input != 'None' and district_input != 'None' and local_input == 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, industry_acc_product__contains=product_input, district__contains=district_input)
            
        elif investment_input != 'None' and product_input == 'None' and district_input != 'None' and local_input != 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, district__contains=district_input, local_body__contains=local_input)
            
        elif investment_input != 'None' and product_input != 'None' and district_input == 'None' and local_input != 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input, local_body__contains=local_input)
        
        elif investment_input == 'None' and product_input != 'None' and district_input != 'None' and local_input == 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(industry_acc_product__contains=product_input, district__contains=district_input)
            
        elif investment_input == 'None' and product_input != 'None' and district_input == 'None' and local_input != 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(industry_acc_product__contains=product_input, local_body__contains=local_input)
            
        elif investment_input == 'None' and product_input == 'None' and district_input != 'None' and local_input != 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(district__contains=district_input, local_body__contains=local_input)
            
        elif investment_input == 'None' and product_input != 'None' and district_input != 'None' and local_input != 'None':
            industries_queryset = IndustryWithoutGis.objects.filter(industry_acc_product__contains=product_input, district__contains=district_input, local_body__contains=local_input)
    else:
        industries_queryset = IndustryWithoutGis.objects.all().order_by('-id')

    # Configure the number of records to display per page
    items_per_page = 100

    # Create a Paginator object using the industries queryset
    paginator = Paginator(industries_queryset, items_per_page)

    # Get the current page number from the request GET parameters
    page_number = request.GET.get('page', 1)

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    # Prepare data to be passed to the template
    data = {
        'industry': page,
        'request':request,
        'messages': messages.get_messages(request),
        'all_localbody': all_localbody,
    }
    
    return render(request, 'industry_without_gis/industry_list_without_gis.html', data)


@login_required
def view_industry_profile_without_gis(request, industry_id):
    industry = get_object_or_404(IndustryWithoutGis, id=industry_id)
    context = {'industry': industry}
    return render(request, 'industry_without_gis/industry_detail_without_gis.html', context)


@superadmin_required
def delete_industry_without_gis(request, industry_id):
    industry = get_object_or_404(IndustryWithoutGis, id=industry_id)
    industry.delete()
    messages.info(request, "Industry deleted!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   #redirects user to same page after deleting


@login_required
def edit_industry_without_gis(request, industry_id):
    data = {
        'sex' : commons.SEX_CHOICES,
        'cas' : commons.CASTE_CHOICES,
        'inv' : commons.INVESTMENT_CHOICES,
        'own' : commons.OWNERSHIP_CHOICES,
        'raw' : commons.MATERIAL_SOURCE,
        'top' : commons.TYPE_OF_PRODUCT,
        'cs' : commons.CURRENT_STATUS,
        'ca' : commons.CAPACITY,
        'district': commons.DISTRICT_CHOICES,
    }
    industry = get_object_or_404(IndustryWithoutGis, id=industry_id)
    if request.method == 'POST':
        form = IndustryWithoutGisModelForm(request.POST, instance=industry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Industry Detail is Updated Successfully!')
            return redirect('industry_without_gis_list')
    else:
        form = IndustryWithoutGisModelForm(instance=industry)
        
    if form.errors:
        for field in form:
            if field.errors:
                messages.error(request, 'Please fill the fields with correct data')
                break
        
    context = {
                'form': form, 
                'industry': industry, 
                'data': data
                }
    return render(request, 'industry_without_gis/edit_industry_without_gis.html', context)


def AjaxSearchWithousGis(request):
    investment_input = request.GET.get('investment_input')
    product_input = request.GET.get('product_input')
    district_input = request.GET.get('district_input')
    local_input = request.GET.get('local_input')
    
    page = int(request.GET.get('page', 1)) #lazy loading

    if request.GET.get('type') == "search":
        session_local_delete(request)
        search_query = str(request.GET.get('search'))
        queryset = IndustryWithoutGis.objects.filter(industry_name__contains=search_query)
    else:
        request.session['investment_input'] = investment_input
        request.session['product_input'] = product_input
        request.session['district_input'] = district_input
        request.session['local_input'] = local_input
        request.session['type'] = 'option'
        
        if investment_input != 'None' and product_input != 'None' and district_input != 'None' and local_input != 'None':
            queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input, district__contains=district_input, local_body__contains=local_input)
        
        elif investment_input == 'None' and product_input == 'None' and district_input == 'None' and local_input == 'None':
            queryset = IndustryWithoutGis.objects.all().order_by('-id')[:100]
        
        elif investment_input != 'None' and product_input == 'None' and district_input == 'None' and local_input == 'None':
            queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input) 
        
        elif investment_input == 'None' and product_input != 'None' and district_input == 'None' and local_input == 'None':
            queryset = IndustryWithoutGis.objects.filter(industry_acc_product__contains=product_input)
            
        elif investment_input == 'None' and product_input == 'None' and district_input != 'None' and local_input == 'None':
            queryset = IndustryWithoutGis.objects.filter(district__contains=district_input)
        
        elif investment_input == 'None' and product_input == 'None' and district_input == 'None' and local_input != 'None':
            queryset = IndustryWithoutGis.objects.filter(local_body__contains=local_input)
        
        elif investment_input != 'None' and product_input != 'None' and district_input == 'None' and local_input == 'None':
            queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, industry_acc_product__contains=product_input)
            
        elif investment_input != 'None' and product_input == 'None' and district_input != 'None' and local_input == 'None':
            queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, district__contains=district_input)
            
        elif investment_input != 'None' and product_input == 'None' and district_input == 'None' and local_input != 'None':
            queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, local_body__contains=local_input)
            
        elif investment_input != 'None' and product_input != 'None' and district_input != 'None' and local_input == 'None':
            queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, industry_acc_product__contains=product_input, district__contains=district_input)
            
        elif investment_input != 'None' and product_input == 'None' and district_input != 'None' and local_input != 'None':
            queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, district__contains=district_input, local_body__contains=local_input)
            
        elif investment_input != 'None' and product_input != 'None' and district_input == 'None' and local_input != 'None':
            queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input, local_body__contains=local_input)
        
        elif investment_input == 'None' and product_input != 'None' and district_input != 'None' and local_input == 'None':
            queryset = IndustryWithoutGis.objects.filter(industry_acc_product__contains=product_input, district__contains=district_input)
            
        elif investment_input == 'None' and product_input != 'None' and district_input == 'None' and local_input != 'None':
            queryset = IndustryWithoutGis.objects.filter(industry_acc_product__contains=product_input, local_body__contains=local_input)
            
        elif investment_input == 'None' and product_input == 'None' and district_input != 'None' and local_input != 'None':
            queryset = IndustryWithoutGis.objects.filter(district__contains=district_input, local_body__contains=local_input)
            
        elif investment_input == 'None' and product_input != 'None' and district_input != 'None' and local_input != 'None':
            queryset = IndustryWithoutGis.objects.filter(industry_acc_product__contains=product_input, district__contains=district_input, local_body__contains=local_input)
    
    items_per_page = 100
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    
    json_data = serialize('json', page)
    return JsonResponse(json_data, safe=False)


def session_delete(request):
    if 'type' in request.session:
        del request.session['type']
        del request.session['product_input']
        del request.session['investment_input']
        del request.session['district_input']
        del request.session['local_input']
    return redirect('industry_without_gis_list')


@login_required
def without_gis_industry_excel(request):
    """downloads industry data in excel format"""
    filter_investment = request.GET.get("investment")
    filter_industry_acc_product = request.GET.get("industry_acc_product")
    filter_district = request.GET.get("district")
    filter_localbody = request.GET.get("localbody")
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Industry'+ 'industry_data' + '.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Industry')
    
    headers = ['Name of Industry', 'Industry Reg No', 'District', 'Local Body', 'Ward no', 'Propriter Name', 
                'Sex', 'Cast', 'employment (Men)', 'employment (Women)', 'Type of Industry (Investment)', 
                'Type of Industry (Production)', 'Type of Industry (Private form or Partnership)', 'Total Capital', 
                'Production Capacity (Annual) Nrs']
    
    for col_num, header in enumerate(headers):
        ws.write(0, col_num, header)
    
    industries = IndustryWithoutGis.objects.all()
    
    if filter_investment != 'None':
        industries = industries.filter(investment=filter_investment)
    
    if filter_industry_acc_product != 'None':
        industries = industries.filter(industry_acc_product=filter_industry_acc_product)
        
    if filter_district != 'None':
        industries = industries.filter(district=filter_district)
        
    if filter_localbody != 'None':
        industries = industries.filter(investment=filter_localbody)
    
    for row_num, industry in enumerate(industries, start=1):
        ws.write(row_num, 0, industry.industry_name)
        ws.write(row_num, 1, industry.industry_reg_no)
        ws.write(row_num, 2, industry.district_display_value)
        ws.write(row_num, 3, industry.local_body_display_value)
        ws.write(row_num, 4, industry.ward_no)
        ws.write(row_num, 5, industry.owner_name)
        ws.write(row_num, 6, industry.sex_display_value)
        ws.write(row_num, 7, industry.caste_display_value)
        ws.write(row_num, 8, industry.male)
        ws.write(row_num, 9, industry.female)
        ws.write(row_num, 10, industry.investment_display_value)
        ws.write(row_num, 11, industry.industry_acc_product_display_value)
        ws.write(row_num, 12, industry.ownership_display_value)
        ws.write(row_num, 13, industry.total_capital)
        ws.write(row_num, 14, industry.yearly_capacity)

    wb.save(response)
    return response


@login_required
def without_gis_industry_csv(request):
    """downloads industry data in csv format"""
    filter_investment = request.GET.get("investment")
    filter_industry_acc_product = request.GET.get("industry_acc_product")
    filter_district = request.GET.get("district")
    filter_localbody = request.GET.get("localbody")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Industry'+ 'industry_data' + '.csv'
    response.write(u'\ufeff'.encode('utf8'))
    
    writer = csv.writer(response)
    writer.writerow(['Name of Industry', 'Industry Reg No', 'District', 'Local Body', 'Ward no', 'Propriter Name', 
                    'Sex', 'Caste', 'employment (Men)', 'employment (Women)', 'Type of Industry (Investment)', 
                    'Type of Industry (Production)', 'Type of Industry (Private form or Partnership)', 'Total Capital', 
                    'Production Capacity (Annual) Nrs'])
    
    industries = IndustryWithoutGis.objects.all()
    
    if filter_investment != 'None':
        industries = industries.filter(investment=filter_investment)
    
    if filter_industry_acc_product != 'None':
        industries = industries.filter(industry_acc_product=filter_industry_acc_product)
        
    if filter_district != 'None':
        industries = industries.filter(ownership=filter_district)
        
    if filter_localbody != 'None':
        industries = industries.filter(ownership=filter_localbody)
    
    for industry in industries:
        writer.writerow(
            [industry.industry_name, industry.industry_reg_no, industry.district_display_value, industry.local_body_display_value, 
            industry.ward_no, industry.owner_name, industry.sex_display_value, industry.caste_display_value, industry.male, industry.female, 
            industry.investment_display_value, industry.industry_acc_product_display_value, industry.ownership_display_value,
            industry.total_capital, industry.yearly_capacity]
            )
        
    return response


@login_required
def industry_without_gis_profile_pdf(request, industry_id):
    industry = get_object_or_404(IndustryWithoutGis, id=industry_id)
    context = {'industry': industry}
    return render(request, 'industry_without_gis/industry_without_gis_profile_pdf.html', context)


@login_required
def without_gis_download_pdf(request):
    """downloads industry data in pdf format"""
    investment_input = request.GET.get('investment_input')
    product_input = request.GET.get('product_input')
    district_input = request.GET.get("district_input")
    local_input = request.GET.get("local_input")
    

    if investment_input != 'None' and product_input != 'None' and district_input != 'None' and local_input != 'None':
        queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input, district__contains=district_input, local_body__contains=local_input)
    
    elif investment_input != 'None' and product_input == 'None' and district_input == 'None' and local_input == 'None':
        queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input) 
    
    elif investment_input == 'None' and product_input != 'None' and district_input == 'None' and local_input == 'None':
        queryset = IndustryWithoutGis.objects.filter(industry_acc_product__contains=product_input)
        
    elif investment_input == 'None' and product_input == 'None' and district_input != 'None' and local_input == 'None':
        queryset = IndustryWithoutGis.objects.filter(district__contains=district_input)
    
    elif investment_input == 'None' and product_input == 'None' and district_input == 'None' and local_input != 'None':
        queryset = IndustryWithoutGis.objects.filter(local_body__contains=local_input)
    
    elif investment_input != 'None' and product_input != 'None' and district_input == 'None' and local_input == 'None':
        queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, industry_acc_product__contains=product_input)
        
    elif investment_input != 'None' and product_input == 'None' and district_input != 'None' and local_input == 'None':
        queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, district__contains=district_input)
        
    elif investment_input != 'None' and product_input == 'None' and district_input == 'None' and local_input != 'None':
        queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, local_body__contains=local_input)
        
    elif investment_input != 'None' and product_input != 'None' and district_input != 'None' and local_input == 'None':
        queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, industry_acc_product__contains=product_input, district__contains=district_input)
        
    elif investment_input != 'None' and product_input == 'None' and district_input != 'None' and local_input != 'None':
        queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input, district__contains=district_input, local_body__contains=local_input)
        
    elif investment_input != 'None' and product_input != 'None' and district_input == 'None' and local_input != 'None':
        queryset = IndustryWithoutGis.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input, local_body__contains=local_input)
    
    elif investment_input == 'None' and product_input != 'None' and district_input != 'None' and local_input == 'None':
        queryset = IndustryWithoutGis.objects.filter(industry_acc_product__contains=product_input, district__contains=district_input)
        
    elif investment_input == 'None' and product_input != 'None' and district_input == 'None' and local_input != 'None':
        queryset = IndustryWithoutGis.objects.filter(industry_acc_product__contains=product_input, local_body__contains=local_input)
        
    elif investment_input == 'None' and product_input == 'None' and district_input != 'None' and local_input != 'None':
        queryset = IndustryWithoutGis.objects.filter(district__contains=district_input, local_body__contains=local_input)
        
    elif investment_input == 'None' and product_input != 'None' and district_input != 'None' and local_input != 'None':
        queryset = IndustryWithoutGis.objects.filter(industry_acc_product__contains=product_input, district__contains=district_input, local_body__contains=local_input)
    
    else:
        queryset = []

    context = {
        'industry': queryset,
        }
    return render(request,"industry/report.html",context)






# import re
# from industry_without_gis import excel_name

# def translation_settings(request):
#     # Define the updated translations
#     updated_translations = {}

#     if request.method == 'POST':
#         for key in FIELD_TRANSLATIONS:
#             new_translation = request.POST.get(key)
#             if new_translation:
#                 updated_translations[key] = new_translation

#         # Read the contents of the Python file
#         with open('industry_without_gis/excel_name.py', 'r', encoding='utf-8') as excel_file:
#             file_contents = excel_file.read()

#         # Update the FIELD_TRANSLATIONS dictionary in the file_contents
#         for key, value in updated_translations.items():
#             pattern = re.compile(f"'{key}':\s*['\"].*?['\"']", re.DOTALL)
#             replacement = f"'{key}': '{value}'"
#             file_contents = pattern.sub(replacement, file_contents)

#         # Write the updated contents back to the file
#         with open('industry_without_gis/excel_name.py', 'w', encoding='utf-8') as excel_file:
#             excel_file.write(file_contents)

#         # Add a success message
#         messages.success(request, 'Translations updated successfully')

#         # Reload the updated translations
#         existing_translations = updated_translations

#     else:
#         # Use the initial translations
#         existing_translations = FIELD_TRANSLATIONS

#     # Convert updated_translations dictionary to a list of (key, value) pairs for template
#     updated_translations_list = [(key, value) for key, value in updated_translations.items()]

#     return render(request, 'translation_settings.html', {
#         'translations': existing_translations,
#         'updated_translations': updated_translations_list,
#     })