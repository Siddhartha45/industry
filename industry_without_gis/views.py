import pandas as pd
import xlwt
import csv

from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers import serialize

from .models import IndustryWithoutGis
from .forms import IndustryWithoutGisModelForm

from fdip import commons
from industry.views import session_local_delete
from report.excel_data_mapping import (
    dtype_mapping, sex_mapping, caste_mapping, investment_mapping, industry_acc_product_mapping, current_status_mapping, 
    ownership_mapping, raw_materials_source_mapping, current_running_capacity_mapping, district_mapping, local_body_mapping
    )


def without_gis_data_import(request, file):
    """function for exporting excel data of industries without gis to IndutryWithoutGis model"""
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
                        'settlement', 'product_description', 'product_service_name', 'machinery_tool']
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
            industry = IndustryWithoutGis(**industry_data)
            if hasattr(industry, 'total_manpower'):
                industry.total_manpower = total_manpower
            industry.save() 
    return messages.success(request, "The excel data is saved to database.")


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


def view_industry_profile_without_gis(request, industry_id):
    industry = get_object_or_404(IndustryWithoutGis, id=industry_id)
    context = {'industry': industry}
    return render(request, 'industry_without_gis/industry_detail_without_gis.html', context)


def delete_industry_without_gis(request, industry_id):
    industry = get_object_or_404(IndustryWithoutGis, id=industry_id)
    industry.delete()
    messages.info(request, "Industry deleted!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   #redirects user to same page after deleting


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


def industry_without_gis_profile_pdf(request, industry_id):
    industry = get_object_or_404(IndustryWithoutGis, id=industry_id)
    context = {'industry': industry}
    return render(request, 'industry_without_gis/industry_without_gis_profile_pdf.html', context)


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