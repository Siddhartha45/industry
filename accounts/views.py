from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from accounts.models import CustomUser
from .forms import CustomUserForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from fdip.decorators import superadmin_required
import xlwt
import csv
from django.contrib.auth.views import PasswordResetView
from django.core.exceptions import ValidationError


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "invalid credentials! Please enter correct email address and password.")
    return render(request, 'account/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def normalize_email(email):
    """for normalizing email of users so that multiple users cant have same email with different case"""
    email = email
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        email_name = email_name.lower()
        domain_part = domain_part.lower()
        email = '@'.join([email_name, domain_part])
    return email


@superadmin_required
def user_create(request,id=None):
    data = {
        'role' : CustomUser.ROLE_CHOICES
    }
        
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('email')
            normalized_email = normalize_email(email)
            data = {
                'username': form.cleaned_data.get('username', 'default_username'),
                'email': normalized_email,
                'fullname': form.cleaned_data.get('fullname', 'default_fullname'),
                'phone_no': form.cleaned_data.get('phone_no', 'default_phone_no'),             
                'role': form.cleaned_data.get('role', 'default_role'),
            }
            password = make_password(request.POST['password'])
            if id != None and len(password) > 2:
                data['password'] = password
            elif len(password)>2:
                data['password'] = password
            if id != None:
                if CustomUser.objects.filter(email=data['email']) and CustomUser.objects.get(id=id).email != data['email']:
                    messages.error(request, f'User with this email ({data["email"]}) is already registered!')
                    return redirect('user-create')
                
            if id == None:
                if CustomUser.objects.filter(email=data['email']):
                    messages.error(request, f'User with this email ({data["email"]}) is already registered!')
                    return redirect('user-create')
            
                if CustomUser.objects.filter(username=data['username']):
                    messages.error(request, 'User with this username ({data["username"]}) is already registered!')
                    return redirect('user-create')
            
            user_obj, created = CustomUser.objects.update_or_create(id=id, defaults=data)
            
            if created:
                messages.success(request, 'User created successfully!')
            else:
                messages.success(request, 'User updated successfully!')
            
            return redirect('view-users')    
    else: 
        form = CustomUserForm()
    
    if form.errors:
        for field in form:
            if field.errors:
                messages.error(request, 'Error! Please fill all the fields with correct data.')
                break
    
    if id !=None:
        user_data = CustomUser.objects.get(id=id)
        role = CustomUser.ROLE_CHOICES
        data['user_data'] = user_data
        data['role'] = role
        data['edit_id'] = id
    return render(request, 'account/createuser.html', data)


@superadmin_required
def view_users(request):
    data = {
        'users' : CustomUser.objects.all(),
    }
    return render(request, 'account/viewadminuser.html', data)


@login_required
def view_user_details(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user != user:
        return redirect('home')
    context = {'user': user}
    return render(request, 'account/userinfo.html', context)


@superadmin_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('view-users')


@login_required
def change_password(request):
    if request.method == 'POST':
        user_id = request.user.id
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        retype_password = request.POST.get('retype_password')
        print(current_password)
        print(new_password)
        print(retype_password)
        if current_password == '' or new_password == '' or retype_password == '':
            messages.error(request, 'Field is left blank. Cannot change Password')
            return redirect('change-password')
            
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Invalid current password!')
            return redirect('change-password')
            
        if new_password != retype_password:
            messages.error(request, 'New passwords did not match! ')
            return redirect('change-password')
        
        user = CustomUser.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()
        #update_session_auth_hash(request, user)    #user is not logged out after changing password
        messages.success(request, 'Password changed successfully.')

        return redirect('change-password')
            
    return render(request, 'account/changepassword.html')


#customizing the django default passwordresetview to check if users email exist in database before sending mail
class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data['email']
        # Check if the email exists in the database
        if not CustomUser.objects.filter(email=email).exists():
            # Display an error message
            messages.error(self.request, 'Email does not exist.')
            return self.form_invalid(form)
        return super().form_valid(form)


#to display the role names in excel file
def get_role_display(role_id):
    for role_choice in CustomUser.ROLE_CHOICES:
        if role_choice[0] == role_id:
            return role_choice[1]
    return ''  # Return an empty string if the role is not found


@superadmin_required
def accounts_excel(request):
    filter_role = request.GET.get("role")
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Accounts.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Account')
    
    headers = ['username', 'fullname', 'role', 'email address', 'phone no.']
    
    for col_num, header in enumerate(headers):
        ws.write(0, col_num, header)
    
    accounts = CustomUser.objects.all()
    print(filter_role)
    
    if filter_role:
        if filter_role != "0":
            accounts = accounts.filter(role=filter_role)
    
    for row_num, account in enumerate(accounts, start=1):
        ws.write(row_num, 0, account.username)
        ws.write(row_num, 1, account.fullname)
        ws.write(row_num, 2, get_role_display(account.role))
        ws.write(row_num, 3, account.email)
        ws.write(row_num, 4, account.phone_no)

    wb.save(response)
    
    return response


@superadmin_required
def accounts_csv(request):
    filter_role = request.GET.get("role")
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Accounts.csv'
    
    writer = csv.writer(response)
    writer.writerow(['username', 'fullname', 'role', 'email address', 'phone no.'])
    
    accounts = CustomUser.objects.all()
    
    if filter_role:
        if filter_role != "0":
            accounts = accounts.filter(role=filter_role)

    for account in accounts:
        writer.writerow([account.username, account.fullname, get_role_display(account.role), account.email, account.phone_no])
        
    return response


@superadmin_required
def accounts_pdf(request):
    account = CustomUser.objects.all()

    context = {
        'account': account,
        }
    return render(request,"account/accountpdf.html",context)