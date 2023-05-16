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



#for exporting excel datas into our industry model
from django.conf import settings
import os
import pandas as pd
from django.http import JsonResponse, HttpResponse
from industry.models import Industry
from fdip import commons

def ImportExcel(request):
    
    file_path = os.path.join(settings.MEDIA_ROOT, "import.xlsx")
    print(file_path)

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        top_10 = df.head(10)
        # print(top_10)
        for index, row in df.iterrows():
            # pass
            # industry_name_preeti = row['industry_name']
            # industry_name_unicode = getUnicode(industry_name_preeti)
            # return HttpResponse("converted preeti data "+industry_name_preeti+" to unicode data "+industry_name_unicode)
            # print(row)
            investment_choice = row['investment']
            if investment_choice == "साना":
                investment = "SMALL"
            elif investment_choice == "लघु":
                investment = "MINIATURE"
            elif investment_choice == "घरेलु":
                investment = "DOMESTIC"
            else:
                investment == "error"
            # print(investment)
            male = 1
            female = 1
            
            current_status_choice = row['current_status']
            if current_status_choice == "सक्रिय":
                current_status = "A"
            elif current_status_choice == "निष्कृय":
                current_status = "I"
            else:
                current_status == "error"
            
            
            
            #industry_name = getUnicode(row['industry_name'])
            
            industry_name = row['industry_name']
            address = row['address']
            ward_no = row['ward_no']
            investment = investment
            product = row['product']
            owner_name = row['owner_name']
            mobile_number = row['mobile_number']
            fixed_capital = row['fixed_capital']
            current_capital = row['current_capital']
            total_capital = row['total_capital']
            current_status = current_status
            female = female
            male = male
            
            data = {
                "industry_name" : industry_name,
                "address" : address,
                "ward_no" : ward_no,
                "investment" : investment,
                "product_description" : product,
                "owner_name" : owner_name,
                "mobile_number" : mobile_number,
                "fixed_capital" : fixed_capital,
                "current_capital" : current_capital,
                "total_capital" : total_capital,
                "current_status" : current_status,
                "female" : female,
                "male" : male,
            }
            
            industry_obj = Industry.objects.create(**data)

        top_10 = df.head(10)
        # print(top_10)
        data = top_10.to_json(orient='records')
        return JsonResponse(data,safe=False)
    else:
        return HttpResponse("file not found")



def ConvertExcel(request):
    
    file_path = os.path.join(settings.MEDIA_ROOT, "darchula.xlsx")
    print(file_path)

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        top_10 = df.head(10)
        # print(top_10)
        for index, row in df.iterrows():
            # pass
            # industry_name_preeti = row['industry_name']
            # industry_name_unicode = getUnicode(industry_name_preeti)
            # return HttpResponse("converted preeti data "+industry_name_preeti+" to unicode data "+industry_name_unicode)
            # print(row)
            
            # print(investment)
            #industry_name = getUnicode(row['industry_name'])
            
            industry_name = row['industry_name']
            address = row['address']
            ward_no = row['ward_no']
            investment = investment
            product = row['product']
            owner_name = row['owner_name']
            mobile_number = row['mobile_number']
            fixed_capital = row['fixed_capital']
            current_capital = row['current_capital']
            total_capital = row['total_capital']
            current_status = current_status
            female = female
            male = male
            
            data = {
                "industry_name" : industry_name,
                "address" : address,
                "ward_no" : ward_no,
                "investment" : investment,
                "product_description" : product,
                "owner_name" : owner_name,
                "mobile_number" : mobile_number,
                "fixed_capital" : fixed_capital,
                "current_capital" : current_capital,
                "total_capital" : total_capital,
                "current_status" : current_status,
                "female" : female,
                "male" : male,
            }
            
            industry_obj = Industry.objects.create(**data)

        top_10 = df.head(10)
        # print(top_10)
        data = top_10.to_json(orient='records')
        return JsonResponse(data,safe=False)
    else:
        return HttpResponse("file not found")



def getUnicode(preeti_code):
    file_path = os.path.join(settings.MEDIA_ROOT, "map.json")
    print(file_path)
    mapper = npttf2utf.FontMapper(file_path)
    unicode = mapper.map_to_unicode(preeti_code, from_font="Preeti", unescape_html_input=False, escape_html_output=False)
    return unicode


    
    
import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework import views
try:
    import npttf2utf
except:
    print("Please install npttf2utf")
    
from django.conf import settings

file_path = os.path.join(settings.MEDIA_ROOT, "map.json")

class PreetiToUniCode(views.APIView):
    def get(self, request):        
        print(file_path)
        mapper = npttf2utf.FontMapper(file_path)
        unicode = mapper.map_to_unicode(';"gf}nf] sfkL pBf]u', from_font="Preeti", unescape_html_input=False, escape_html_output=False)
        # बकमानजवप            
        return HttpResponse(unicode)

class UnicodeToPreeti(views.APIView):
    def get(self,request):
        mapper = npttf2utf.FontMapper(file_path)
        preeti = mapper.map_to_preeti("सबिन आचार्य", from_font="unicode", unescape_html_input=False, escape_html_output=False)
        # ;lag cfrf/\o
        return HttpResponse(preeti)