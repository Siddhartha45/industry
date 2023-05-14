from django.shortcuts import render, redirect, get_object_or_404
from .models import Faq
from .forms import FaqForm
from django.contrib import messages
from fdip.decorators import superadmin_required


@superadmin_required
def faq_create(request):
    if request.method == 'POST':
        form = FaqForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ Created')
            return redirect('faq-list')
    else:
        form = FaqForm()
        
    if form.errors:
        for field in form:
            if field.errors:
                messages.error(request, 'Please fill out all the fields.')
                break
    context = {'form': form}
    return render(request, 'faq/create.html', context)


def faq_display(request):
    faq = Faq.objects.all()
    context = {'faq': faq}
    return render(request, 'faq/display.html', context)


@superadmin_required
def faq_list(request):
    faq = Faq.objects.all()
    context = {'faq': faq}
    return render(request, 'faq/list.html', context)


@superadmin_required
def faq_edit(request, faq_id):
    faq = get_object_or_404(Faq, id=faq_id)
    
    if request.method == 'POST':
        form = FaqForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated!')
            return redirect('faq-list')
    else:
        form = FaqForm(instance=faq)
    context = {'form': form, 'faq': faq}
    return render(request, 'faq/edit.html', context)


@superadmin_required
def faq_delete(request, faq_id):
    faq = get_object_or_404(Faq, id=faq_id)
    faq.delete()
    return redirect('faq-list')
    