from django.shortcuts import render
from django.core.paginator import Paginator

from industry.models import Industry
from fdip import commons

# Create your views here.
def all_industries(request):
    district = commons.DISTRICT_CHOICES
    investment = commons.INVESTMENT_CHOICES
    industries = Industry.objects.all()
    
    searched_name = request.GET.get("searched_name")
    searched_district = request.GET.get("searched_district")
    searched_investment = request.GET.get("searched_investment")

    print("name", searched_name)
    print("district",searched_district)
    if searched_name:
        industries = industries.filter(industry_name__icontains=searched_name)
    if searched_district:
        industries = industries.filter(district=searched_district)
    if searched_investment:
        industries = industries.filter(investment=searched_investment)
    
    paginator = Paginator(industries, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    starting_sn = (page_obj.number - 1) * paginator.per_page + 1

    context = {
        "district": district, "page_obj": page_obj, "investment": investment,
        "starting_sn": starting_sn,
        "searched_name": searched_name,
        "searched_district": searched_district,
        "searched_investment": searched_investment
        }
    return render(request, "improv/industries.html", context)

