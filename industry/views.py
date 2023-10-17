import csv
import xlwt

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import JsonResponse


from .models import Industry, IndustryPhoto
from .forms import IndustryForm

from fdip import commons


def home(request):
    session_local_delete(request)
    
    selected_district = request.GET.get('district')
    
    if selected_district:
        data_filter = Industry.objects.filter(district=selected_district)
    else:
        data_filter = Industry.objects.all()

    unique_districts = Industry.objects.values_list('district', flat=True).distinct()
    
    try:
        district_dict = {district['district']: district['count'] for district in Industry.objects.values('district').annotate(count=Count('district'))}
    except:
        district_dict = {}

    district_count = unique_districts.count()
    
    total_industry = data_filter.count()
    #for showing chart acc to investment
    miniature = data_filter.filter(investment='MINIATURE').count()
    domestic = data_filter.filter(investment='DOMESTIC').count()
    small = data_filter.filter(investment='SMALL').count()
    medium = data_filter.filter(investment='MEDIUM').count()
    large = data_filter.filter(investment='LARGE').count()
    total_industry_acc_inv = miniature + domestic + small + medium + large
    #for showing chart acc to ownership
    private = data_filter.filter(ownership='PRIVATE').count()
    partnership = data_filter.filter(ownership='PARTNERSHIP').count()
    total_ownership = private + partnership
    #for showing chart acc to current status
    active = data_filter.filter(current_status='A').count()
    inactive = data_filter.filter(current_status='I').count()
    total_current_status = active + inactive
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
    total_industry_acc_pro = (energy + manufacturing + ag + mineral + infra + 
                             tourism + it + service + others)
    #for showing chart acc to employment
    total_manpower = data_filter.aggregate(total=Sum('total_manpower'))['total']
    skilled = data_filter.aggregate(total=Sum('skillfull'))['total']
    unskilled = data_filter.aggregate(total=Sum('unskilled'))['total']
    indigenous = data_filter.aggregate(total=Sum('indigenous'))['total']
    foreign = data_filter.aggregate(total=Sum('foreign'))['total']
    male = data_filter.aggregate(total=Sum('male'))['total']
    female = data_filter.aggregate(total=Sum('female'))['total']

    context = {
                'data_filter': data_filter,
                'unique_districts': unique_districts,
                'district_count': district_count,
                'district_dict': district_dict,
                
                'total_industry': total_industry,
                
                'total_industry_acc_inv': total_industry_acc_inv,
                'miniature': miniature,
                'domestic': domestic,
                'small': small,
                'medium': medium,
                'large': large,
                
                'total_ownership': total_ownership,
                'private': private,
                'partnership': partnership,
                
                'total_current_status': total_current_status,
                'active': active,
                'inactive': inactive,
                
                'total_industry_acc_pro': total_industry_acc_pro,
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
        return render(request, 'account/adminpanel.html', context)
    else:
        return render(request, 'public/public_view.html', context)


def get_local_bodies(request, district):
    """Returns Json Response of localbody_choices acc to district selected"""
    if district == 'KAILALI':
        localbody_choices = commons.KAILALI_LOCALBODY_CHOICES
    elif district == 'KANCHANPUR':
        localbody_choices = commons.KANCHANPUR_LOCALBODY_CHOICES
    elif district == 'DADELDHURA':
        localbody_choices = commons.DADELDHURA_LOCALBODY_CHOICES
    elif district == 'DOTI':
        localbody_choices = commons.DOTI_LOCALBODY_CHOICES
    elif district == 'ACHHAM':
        localbody_choices = commons.ACHHAM_LOCALBODY_CHOICES
    elif district == 'BAJURA':
        localbody_choices = commons.BAJURA_LOCALBODY_CHOICES
    elif district == 'BAJHANG':
        localbody_choices = commons.BAJHANG_LOCALBODY_CHOICES
    elif district == 'BAITADI':
        localbody_choices = commons.BAITADI_LOCALBODY_CHOICES
    elif district == 'DARCHULA':
        localbody_choices = commons.DARCHULA_LOCALBODY_CHOICES
    else:
        localbody_choices = []
    return JsonResponse({'localbody_choices': localbody_choices})


@login_required
def add_industry(request):
    """For adding the industry details"""
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
    if request.method == "POST":
        form = IndustryForm(request.POST, request.FILES)
        
        if form.is_valid(): 
            industry_data = form.cleaned_data
            others_text = industry_data.get('others_text')
            
            if others_text:
                industry_data['industry_acc_product'] = 'O' #sets the industry_acc_products choice to others if user fills the other_texts fields
            
            photos = request.FILES.getlist('photo')

            industry = Industry.objects.create(**industry_data)
            for photo in photos:
                IndustryPhoto.objects.create(industry=industry, photo=photo)
                
            messages.success(request, 'Industry Detail is Added Successfully!')
            return redirect('industry-list')
    else:
        form = IndustryForm()
        
    if form.errors:
        for field in form:
            if field.errors:
                messages.error(request, 'Invalid data! Please fill all the fields with correct data.')
                break
    
    context = {
        'data': data,
        'form': form,
    }
    
    return render(request, 'industry/addindustry.html', context)


@login_required
def edit_industry(request, industry_id):
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
    industry = get_object_or_404(Industry, id=industry_id)
    industry_photos = IndustryPhoto.objects.filter(industry=industry)
    
    if request.method == 'POST':
        form = IndustryForm(request.POST, request.FILES, instance=industry)
        if form.is_valid():
            form.save()
            for photo in request.FILES.getlist('photo'):
                IndustryPhoto.objects.create(industry=industry, photo=photo)
            messages.success(request, 'Industry Detail is Updated Successfully!')
            return redirect('industry-list')
    else:
        form = IndustryForm(instance=industry)
        
    if form.errors:
        for field in form:
            if field.errors:
                messages.error(request, 'Please fill the fields with correct data')
                break
        
    context = {
                'form': form, 
                'industry': industry, 
                'industry_photos': industry_photos, 
                'data': data
                }
    return render(request, 'industry/edit.html', context)


@login_required
def view_industry_profile(request, industry_id):
    industry = get_object_or_404(Industry, id=industry_id)
    photos = industry.industry_photo.all()
    context = {'industry': industry, 'photos': photos}
    return render(request, 'industry/industrydetail.html', context)


@login_required
def industry_profile_pdf(request, industry_id):
    industry = get_object_or_404(Industry, id=industry_id)
    context = {'industry': industry}
    return render(request, 'industry/industrydetail_pdf.html', context)


def industry_list(request):
    
    districts = commons.DISTRICT_CHOICES
    all_localbody = commons.ALL_LOCALBODY_CHOICES

    if 'type' in request.session:
        investment_input = request.session.get('investment_input')
        product_input = request.session.get('product_input')
        district_input = request.session.get('district_input')
        local_input = request.session.get('local_input')

        if investment_input != 'None' and product_input != 'None' and district_input != 'None' and local_input != 'None':
            industries_queryset = Industry.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input, district__contains=district_input, local_body__contains=local_input)
        
        elif investment_input == 'None' and product_input == 'None' and district_input == 'None' and local_input == 'None':
            industries_queryset = Industry.objects.all().order_by('-id')[:100]
        
        elif investment_input != 'None' and product_input == 'None' and district_input == 'None' and local_input == 'None':
            industries_queryset = Industry.objects.filter(investment__contains=investment_input) 
        
        elif investment_input == 'None' and product_input != 'None' and district_input == 'None' and local_input == 'None':
            industries_queryset = Industry.objects.filter(industry_acc_product__contains=product_input)
            
        elif investment_input == 'None' and product_input == 'None' and district_input != 'None' and local_input == 'None':
            industries_queryset = Industry.objects.filter(district__contains=district_input)
        
        elif investment_input == 'None' and product_input == 'None' and district_input == 'None' and local_input != 'None':
            industries_queryset = Industry.objects.filter(local_body__contains=local_input)
        
        elif investment_input != 'None' and product_input != 'None' and district_input == 'None' and local_input == 'None':
            industries_queryset = Industry.objects.filter(investment__contains=investment_input, industry_acc_product__contains=product_input)
            
        elif investment_input != 'None' and product_input == 'None' and district_input != 'None' and local_input == 'None':
            industries_queryset = Industry.objects.filter(investment__contains=investment_input, district__contains=district_input)
            
        elif investment_input != 'None' and product_input == 'None' and district_input == 'None' and local_input != 'None':
            industries_queryset = Industry.objects.filter(investment__contains=investment_input, local_body__contains=local_input)
            
        elif investment_input != 'None' and product_input != 'None' and district_input != 'None' and local_input == 'None':
            industries_queryset = Industry.objects.filter(investment__contains=investment_input, industry_acc_product__contains=product_input, district__contains=district_input)
            
        elif investment_input != 'None' and product_input == 'None' and district_input != 'None' and local_input != 'None':
            industries_queryset = Industry.objects.filter(investment__contains=investment_input, district__contains=district_input, local_body__contains=local_input)
            
        elif investment_input != 'None' and product_input != 'None' and district_input == 'None' and local_input != 'None':
            industries_queryset = Industry.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input, local_body__contains=local_input)
        
        elif investment_input == 'None' and product_input != 'None' and district_input != 'None' and local_input == 'None':
            industries_queryset = Industry.objects.filter(industry_acc_product__contains=product_input, district__contains=district_input)
            
        elif investment_input == 'None' and product_input != 'None' and district_input == 'None' and local_input != 'None':
            industries_queryset = Industry.objects.filter(industry_acc_product__contains=product_input, local_body__contains=local_input)
            
        elif investment_input == 'None' and product_input == 'None' and district_input != 'None' and local_input != 'None':
            industries_queryset = Industry.objects.filter(district__contains=district_input, local_body__contains=local_input)
            
        elif investment_input == 'None' and product_input != 'None' and district_input != 'None' and local_input != 'None':
            industries_queryset = Industry.objects.filter(industry_acc_product__contains=product_input, district__contains=district_input, local_body__contains=local_input)
    else:
        industries_queryset = Industry.objects.all().order_by('-id')

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
        'districts': districts,
    }
    
    if request.user.is_authenticated:
        return render(request, 'industry/industrylist.html', data)
    else:
        return render(request, 'public/public_industry_list.html', data)


@login_required
def delete_industry(request, industry_id):
    industry = get_object_or_404(Industry, id=industry_id)
    industry.delete()
    messages.info(request, "Industry deleted!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   #redirects user to same page after deleting


@login_required
def search_industry(request):
    session_local_delete(request)
    if request.GET:
        search_data = Industry.objects.filter(industry_name__contains = request.GET["search"])
    else:
        search_data = Industry.objects.all()
    data = {
            'industry' : search_data
        }
    return render(request, 'industry/searchindustry.html', data)


@login_required
def industry_excel(request):
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
    
    industries = Industry.objects.all()
    
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
def industry_csv(request):
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
    
    industries = Industry.objects.all()
    
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
def download_pdf(request):
    """downloads industry data in pdf format"""
    investment_input = request.GET.get('investment_input')
    product_input = request.GET.get('product_input')
    district_input = request.GET.get("district_input")
    local_input = request.GET.get("local_input")
    

    if investment_input != 'None' and product_input != 'None' and district_input != 'None' and local_input != 'None':
        queryset = Industry.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input, district__contains=district_input, local_body__contains=local_input)
    
    elif investment_input != 'None' and product_input == 'None' and district_input == 'None' and local_input == 'None':
        queryset = Industry.objects.filter(investment__contains=investment_input) 
    
    elif investment_input == 'None' and product_input != 'None' and district_input == 'None' and local_input == 'None':
        queryset = Industry.objects.filter(industry_acc_product__contains=product_input)
        
    elif investment_input == 'None' and product_input == 'None' and district_input != 'None' and local_input == 'None':
        queryset = Industry.objects.filter(district__contains=district_input)
    
    elif investment_input == 'None' and product_input == 'None' and district_input == 'None' and local_input != 'None':
        queryset = Industry.objects.filter(local_body__contains=local_input)
    
    elif investment_input != 'None' and product_input != 'None' and district_input == 'None' and local_input == 'None':
        queryset = Industry.objects.filter(investment__contains=investment_input, industry_acc_product__contains=product_input)
        
    elif investment_input != 'None' and product_input == 'None' and district_input != 'None' and local_input == 'None':
        queryset = Industry.objects.filter(investment__contains=investment_input, district__contains=district_input)
        
    elif investment_input != 'None' and product_input == 'None' and district_input == 'None' and local_input != 'None':
        queryset = Industry.objects.filter(investment__contains=investment_input, local_body__contains=local_input)
        
    elif investment_input != 'None' and product_input != 'None' and district_input != 'None' and local_input == 'None':
        queryset = Industry.objects.filter(investment__contains=investment_input, industry_acc_product__contains=product_input, district__contains=district_input)
        
    elif investment_input != 'None' and product_input == 'None' and district_input != 'None' and local_input != 'None':
        queryset = Industry.objects.filter(investment__contains=investment_input, district__contains=district_input, local_body__contains=local_input)
        
    elif investment_input != 'None' and product_input != 'None' and district_input == 'None' and local_input != 'None':
        queryset = Industry.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input, local_body__contains=local_input)
    
    elif investment_input == 'None' and product_input != 'None' and district_input != 'None' and local_input == 'None':
        queryset = Industry.objects.filter(industry_acc_product__contains=product_input, district__contains=district_input)
        
    elif investment_input == 'None' and product_input != 'None' and district_input == 'None' and local_input != 'None':
        queryset = Industry.objects.filter(industry_acc_product__contains=product_input, local_body__contains=local_input)
        
    elif investment_input == 'None' and product_input == 'None' and district_input != 'None' and local_input != 'None':
        queryset = Industry.objects.filter(district__contains=district_input, local_body__contains=local_input)
        
    elif investment_input == 'None' and product_input != 'None' and district_input != 'None' and local_input != 'None':
        queryset = Industry.objects.filter(industry_acc_product__contains=product_input, district__contains=district_input, local_body__contains=local_input)
    
    else:
        queryset = []

    context = {
        'industry': queryset,
        }
    return render(request,"industry/report.html",context)


def AjaxSearch(request):
    investment_input = request.GET.get('investment_input')
    product_input = request.GET.get('product_input')
    district_input = request.GET.get('district_input')
    local_input = request.GET.get('local_input')
    
    page = int(request.GET.get('page', 1)) #lazy loading

    if request.GET.get('type') == "search":
        session_local_delete(request)
        search_query = str(request.GET.get('search'))
        queryset = Industry.objects.filter(industry_name__contains=search_query)
    else:
        request.session['investment_input'] = investment_input
        request.session['product_input'] = product_input
        request.session['district_input'] = district_input
        request.session['local_input'] = local_input
        request.session['type'] = 'option'
        
        if investment_input != 'None' and product_input != 'None' and district_input != 'None' and local_input != 'None':
            queryset = Industry.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input, district__contains=district_input, local_body__contains=local_input)
        
        elif investment_input == 'None' and product_input == 'None' and district_input == 'None' and local_input == 'None':
            queryset = Industry.objects.all().order_by('-id')[:100]
        
        elif investment_input != 'None' and product_input == 'None' and district_input == 'None' and local_input == 'None':
            queryset = Industry.objects.filter(investment__contains=investment_input) 
        
        elif investment_input == 'None' and product_input != 'None' and district_input == 'None' and local_input == 'None':
            queryset = Industry.objects.filter(industry_acc_product__contains=product_input)
            
        elif investment_input == 'None' and product_input == 'None' and district_input != 'None' and local_input == 'None':
            queryset = Industry.objects.filter(district__contains=district_input)
        
        elif investment_input == 'None' and product_input == 'None' and district_input == 'None' and local_input != 'None':
            queryset = Industry.objects.filter(local_body__contains=local_input)
        
        elif investment_input != 'None' and product_input != 'None' and district_input == 'None' and local_input == 'None':
            queryset = Industry.objects.filter(investment__contains=investment_input, industry_acc_product__contains=product_input)
            
        elif investment_input != 'None' and product_input == 'None' and district_input != 'None' and local_input == 'None':
            queryset = Industry.objects.filter(investment__contains=investment_input, district__contains=district_input)
            
        elif investment_input != 'None' and product_input == 'None' and district_input == 'None' and local_input != 'None':
            queryset = Industry.objects.filter(investment__contains=investment_input, local_body__contains=local_input)
            
        elif investment_input != 'None' and product_input != 'None' and district_input != 'None' and local_input == 'None':
            queryset = Industry.objects.filter(investment__contains=investment_input, industry_acc_product__contains=product_input, district__contains=district_input)
            
        elif investment_input != 'None' and product_input == 'None' and district_input != 'None' and local_input != 'None':
            queryset = Industry.objects.filter(investment__contains=investment_input, district__contains=district_input, local_body__contains=local_input)
            
        elif investment_input != 'None' and product_input != 'None' and district_input == 'None' and local_input != 'None':
            queryset = Industry.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input, local_body__contains=local_input)
        
        elif investment_input == 'None' and product_input != 'None' and district_input != 'None' and local_input == 'None':
            queryset = Industry.objects.filter(industry_acc_product__contains=product_input, district__contains=district_input)
            
        elif investment_input == 'None' and product_input != 'None' and district_input == 'None' and local_input != 'None':
            queryset = Industry.objects.filter(industry_acc_product__contains=product_input, local_body__contains=local_input)
            
        elif investment_input == 'None' and product_input == 'None' and district_input != 'None' and local_input != 'None':
            queryset = Industry.objects.filter(district__contains=district_input, local_body__contains=local_input)
            
        elif investment_input == 'None' and product_input != 'None' and district_input != 'None' and local_input != 'None':
            queryset = Industry.objects.filter(industry_acc_product__contains=product_input, district__contains=district_input, local_body__contains=local_input)
    
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
    return redirect('industry-list')


def session_local_delete(request):
    if 'type' in request.session:
        del request.session['type']
        del request.session['product_input']
        del request.session['investment_input']
        del request.session['district_input']
        del request.session['local_input']
