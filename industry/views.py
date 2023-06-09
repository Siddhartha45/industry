from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, HttpResponseRedirect
from .models import Industry, IndustryPhoto
from .forms import IndustryForm
from fdip import commons
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.paginator import Paginator
#export part
import csv
import datetime
import xlwt


@login_required
def home(request):
    session_local_delete(request)
    
    total_industry = Industry.objects.count()
    #for showing chart acc to investment
    miniature = Industry.objects.filter(investment='MINIATURE').count()
    domestic = Industry.objects.filter(investment='DOMESTIC').count()
    small = Industry.objects.filter(investment='SMALL').count()
    medium = Industry.objects.filter(investment='MEDIUM').count()
    large = Industry.objects.filter(investment='LARGE').count()
    #for showing chart acc to ownership
    private = Industry.objects.filter(ownership='PRIVATE').count()
    partnership = Industry.objects.filter(ownership='PARTNERSHIP').count()
    #for showing chart acc to current status
    active = Industry.objects.filter(current_status='A').count()
    inactive = Industry.objects.filter(current_status='I').count()
    #for showing chart acc to type of product
    energy = Industry.objects.filter(industry_acc_product='E').count()
    manufacturing = Industry.objects.filter(industry_acc_product='MF').count()
    ag = Industry.objects.filter(industry_acc_product='AF').count()
    mineral = Industry.objects.filter(industry_acc_product='MI').count()
    infra = Industry.objects.filter(industry_acc_product='I').count()
    tourism = Industry.objects.filter(industry_acc_product='T').count()
    it = Industry.objects.filter(industry_acc_product='IC').count()
    service = Industry.objects.filter(industry_acc_product='S').count()
    others = Industry.objects.filter(industry_acc_product='O').count()
    #for showing chart acc to employment
    total_manpower = Industry.objects.aggregate(total=Sum('total_manpower'))['total']
    skilled = Industry.objects.aggregate(total=Sum('skillfull'))['total']
    unskilled = Industry.objects.aggregate(total=Sum('unskilled'))['total']
    indigenous = Industry.objects.aggregate(total=Sum('indigenous'))['total']
    foreign = Industry.objects.aggregate(total=Sum('foreign'))['total']
    male = Industry.objects.aggregate(total=Sum('male'))['total']
    female = Industry.objects.aggregate(total=Sum('female'))['total']

    context = {
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
    return render(request, 'account/adminpanel.html', context)


@login_required
def add_industry(request):
    data = {
        'sex' : commons.SEX_CHOICES,
        'cas' : commons.CASTE_CHOICES,
        'inv' : commons.INVESTMENT_CHOICES,
        'own' : commons.OWNERSHIP_CHOICES,
        'raw' : commons.MATERIAL_SOURCE,
        'top' : commons.TYPE_OF_PRODUCT,
        'cs' : commons.CURRENT_STATUS,
        'ca' : commons.CAPACITY,
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


@login_required
def industry_list(request):
    # Apply search filter if provided in request GET parameters
    # print(request.session.get("type"))
    # investment_input = request.session.get('investment_input')
    # if request.session.has_key('type'):
    #   username = request.session['type']
    #   return HttpResponse(username+"sad")
    # else:
        # HttpResponse("session not seted")

            
    if 'type' in request.session:
        investment_input = request.session.get('investment_input')
        ownership_input = request.session.get('ownership_input')
        product_input = request.session.get('product_input')

        if investment_input != 'None' and ownership_input != 'None' and product_input != 'None':
            industries_queryset = Industry.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input,ownership__contains=ownership_input)
            
        elif investment_input == 'None' and ownership_input == 'None' and product_input == 'None':
            industries_queryset = Industry.objects.all().order_by('-id')[:100]
            
        elif investment_input == 'None' and ownership_input != 'None' and product_input != 'None':
            industries_queryset = Industry.objects.filter(industry_acc_product__contains=product_input,ownership__contains=ownership_input)
            
        elif investment_input != 'None' and ownership_input != 'None' and product_input == 'None':
            industries_queryset = Industry.objects.filter(investment__contains=investment_input,ownership__contains=ownership_input)

        elif investment_input != 'None' and ownership_input == 'None' and product_input != 'None':
            industries_queryset = Industry.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input)
            
        elif investment_input != 'None' and ownership_input == 'None' and product_input == 'None':
            industries_queryset = Industry.objects.filter(investment__contains=investment_input)
            
        elif investment_input == 'None' and ownership_input != 'None' and product_input == 'None':
            industries_queryset = Industry.objects.filter(ownership__contains=ownership_input)
            
        elif investment_input == 'None' and ownership_input == 'None' and product_input != 'None':
            industries_queryset = Industry.objects.filter(industry_acc_product__contains=product_input)
    else:
        industries_queryset = Industry.objects.all().order_by('-id')
        
        
    # Fetch industries queryset based on the search filter


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
    }
    
    return render(request, 'industry/industrylist.html', data)


@login_required
def delete_industry(request, industry_id):
    industry = get_object_or_404(Industry, id=industry_id)
    industry.delete()
    messages.info(request, "Industry deleted!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   #redirects user to same page after deleting

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


# def industry_search(request):
#     if 'search' in request.GET:
#         district = request.GET['search']
#         industries = Industry.objects.filter(district__icontains=district)
#     else:
#         industries = Industry.objects.all()
#     context = {
#         'industries': industries
#     }
#     return render(request, 'industry/industrylist.html', context)


@login_required
def industry_excel(request):
    # return HttpResponse(request.get().items())
    filter_investment = request.GET.get("investment")
    filter_ownership = request.GET.get("ownership")
    filter_industry_acc_product = request.GET.get("industry_acc_product")
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Industry'+ str(datetime.datetime.now()) + '.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Industry')
    
    headers = ['Industry Name', 'Industry Owner', 'Address', 'Phone No.']
    
    for col_num, header in enumerate(headers):
        ws.write(0, col_num, header)
    
    industries = Industry.objects.all()
    
    if filter_ownership != 'None':
        industries = industries.filter(ownership=filter_ownership)
    
    if filter_investment != 'None':
        industries = industries.filter(investment=filter_investment)
    
    if filter_industry_acc_product != 'None':
        industries = industries.filter(industry_acc_product=filter_industry_acc_product)
    
    for row_num, industry in enumerate(industries, start=1):
        ws.write(row_num, 0, industry.industry_name)
        ws.write(row_num, 1, industry.owner_name)
        ws.write(row_num, 2, industry.address)
        ws.write(row_num, 3, industry.telephone_number)

    wb.save(response)
    
    return response


@login_required
def industry_csv(request):
    filter_investment = request.GET.get("investment")
    filter_ownership = request.GET.get("ownership")
    filter_industry_acc_product = request.GET.get("industry_acc_product")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Industry'+ str(datetime.datetime.now()) + '.csv'
    response.write(u'\ufeff'.encode('utf8'))
    
    writer = csv.writer(response)
    writer.writerow(['Industry Name', 'Industry Owner', 'Address', 'Phone No.'])
    
    industries = Industry.objects.all()
    
    if filter_ownership != 'None':
        industries = industries.filter(ownership=filter_ownership)
    
    if filter_investment != 'None':
        industries = industries.filter(investment=filter_investment)
    
    if filter_industry_acc_product != 'None':
        industries = industries.filter(industry_acc_product=filter_industry_acc_product)
    
    for industry in industries:
        writer.writerow([industry.industry_name, industry.owner_name, industry.address, industry.telephone_number])
        
    return response


#this is in use for downloading pdf
@login_required
def download_pdf(request):
    investment_input = request.GET.get('investment_input')
    ownership_input = request.GET.get('ownership_input')
    product_input = request.GET.get('product_input')
    

    if investment_input != 'None' and ownership_input != 'None' and product_input != 'None':
        queryset = Industry.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input,ownership__contains=ownership_input)

    elif investment_input == 'None' and ownership_input != 'None' and product_input != 'None':
        queryset = Industry.objects.filter(industry_acc_product__contains=product_input,ownership__contains=ownership_input)
        
    elif investment_input != 'None' and ownership_input != 'None' and product_input == 'None':
        queryset = Industry.objects.filter(investment__contains=investment_input,ownership__contains=ownership_input)

    elif investment_input != 'None' and ownership_input == 'None' and product_input != 'None':
        queryset = Industry.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input)
        
    elif investment_input != 'None' and ownership_input == 'None' and product_input == 'None':
        queryset = Industry.objects.filter(investment__contains=investment_input)
        
    elif investment_input == 'None' and ownership_input != 'None' and product_input == 'None':
        queryset = Industry.objects.filter(ownership__contains=ownership_input)
        
    elif investment_input == 'None' and ownership_input == 'None' and product_input != 'None':
        queryset = Industry.objects.filter(industry_acc_product__contains=product_input)
    else:
        queryset = Industry.objects.all()


    context = {
        'industry': queryset,
        }
    
    return render(request,"industry/report.html",context)

def AjaxSearch(request):
    # return HttpResponse(request.GET.items())
    from django.core.serializers import serialize
    from django.http import JsonResponse
    from django.db.models import Q


    
    investment_input = request.GET.get('investment_input')
    ownership_input = request.GET.get('ownership_input')
    product_input = request.GET.get('product_input')
    page = int(request.GET.get('page', 1)) #lazy loading
    

    if request.GET.get('type') == "search":
    
        session_local_delete(request)
        
        search_query = str(request.GET.get('search'))
        queryset = Industry.objects.filter(district__contains=search_query) or Industry.objects.filter(address__contains=search_query)
    else:
        request.session['investment_input'] = investment_input
        request.session['ownership_input'] = ownership_input
        request.session['product_input'] = product_input
        request.session['type'] = 'option'
        if investment_input != 'None' and ownership_input != 'None' and product_input != 'None':
            queryset = Industry.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input,ownership__contains=ownership_input)
            
        elif investment_input == 'None' and ownership_input == 'None' and product_input == 'None':
            queryset = Industry.objects.all().order_by('-id')[:100]

        elif investment_input == 'None' and ownership_input != 'None' and product_input != 'None':
            queryset = Industry.objects.filter(industry_acc_product__contains=product_input,ownership__contains=ownership_input)
            
        elif investment_input != 'None' and ownership_input != 'None' and product_input == 'None':
            queryset = Industry.objects.filter(investment__contains=investment_input,ownership__contains=ownership_input)

        elif investment_input != 'None' and ownership_input == 'None' and product_input != 'None':
            queryset = Industry.objects.filter(investment__contains=investment_input,industry_acc_product__contains=product_input)
            
        elif investment_input != 'None' and ownership_input == 'None' and product_input == 'None':
            queryset = Industry.objects.filter(investment__contains=investment_input)
            
        elif investment_input == 'None' and ownership_input != 'None' and product_input == 'None':
            queryset = Industry.objects.filter(ownership__contains=ownership_input)
            
        elif investment_input == 'None' and ownership_input == 'None' and product_input != 'None':
            queryset = Industry.objects.filter(industry_acc_product__contains=product_input)
    
    
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
        del request.session['ownership_input']
        del request.session['investment_input']

        #return HttpResponse("session delete")
    #return HttpResponse("session are not delete")
    return redirect('industry-list')

def session_local_delete(request):
    if 'type' in request.session:
        del request.session['type']
        del request.session['product_input']
        del request.session['ownership_input']
        del request.session['investment_input']
    