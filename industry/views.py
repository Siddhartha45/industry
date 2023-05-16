from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Industry, IndustryPhoto
from .forms import IndustryForm
from fdip import commons
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
#export part
import csv
import datetime
import xlwt


@login_required
def home(request):
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
                messages.error(request, 'रोजगारीको अवस्थामा नम्बर हाल्नुहोस!')
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
def industry_list(request):
    if request.GET:
        search_data = Industry.objects.filter(industry_name__contains = request.GET["search"])
    else:
        search_data = Industry.objects.all()
    data = {
        'industry' : Industry.objects.all(),
        'industry' : search_data
    }
    return render(request, 'industry/industrylist.html', data)


@login_required
def delete_industry(request, industry_id):
    industry = get_object_or_404(Industry, id=industry_id)
    industry.delete()
    return redirect('industry-list')


def search_industry(request):
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
    
    if filter_ownership:
        industries = industries.filter(ownership=filter_ownership)
    
    if filter_investment:
        industries = industries.filter(investment=filter_investment)
    
    if filter_industry_acc_product:
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
    
    if filter_ownership:
        industries = industries.filter(ownership=filter_ownership)
    
    if filter_investment:
        industries = industries.filter(investment=filter_investment)
    
    if filter_industry_acc_product:
        industries = industries.filter(industry_acc_product=filter_industry_acc_product)
    
    for industry in industries:
        writer.writerow([industry.industry_name, industry.owner_name, industry.address, industry.telephone_number])
        
    return response


#this is in use for downloading pdf
@login_required
def download_pdf(request):
    industry = Industry.objects.all()

    context = {
        'industry': industry,
        }
    return render(request,"industry/report.html",context)
