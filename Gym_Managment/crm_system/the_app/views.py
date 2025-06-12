from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
import time

@login_required(login_url='login')
def start(request):
    return render(request, 'main_parts/home.html', {"username": request.user.username})

def register(request):
    if request.user.is_authenticated:
        return redirect("start")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')

            if not username or not password or not email:
                messages.error(request, 'There are empty fields')
                return redirect(register)
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already exist')
                return redirect(register)
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already exist')
                return redirect(register)

            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, "Account created successfully")
            return redirect("login")
    return render(request,'main_parts/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect("start")
    username, password = None, None
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        request.session["login_sound"] = True
        if not username or not password:
            messages.error(request, 'There are empty fields')

            return redirect("login")

        if user is not None:

            login(request, user)
            return redirect('start')
        else:

            messages.error(request, 'Username or password is incorrect')
            return redirect("login")

    return render(request, 'main_parts/login.html')

def logout_view(request):
    
    
    logout(request)
    
    return redirect("login")

def category_view(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:

            messages.error(request, "Category name is required.")
            return redirect('category')
        elif Category.objects.filter(name=name).exists():

            messages.error(request, "Category with this name already exists.")
            return render(request, 'main_parts/category.html', {"categories": categories})
        else:
            request.session["success_sound"] = True
            new_category = Category.objects.create(name=name)
            new_category.save()
            messages.success(request, "Category added successfully.")
        return render(request, 'main_parts/category.html', {"categories": categories})
    else:
        return render(request, 'main_parts/category.html', {"categories": categories})
    
def edit_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        if request.method == 'POST':
            category.name = request.POST.get('name')
            category.save()
            messages.success(request, "Category updated successfully.")
            return redirect('category')
        else:
            return render(request, 'main_parts/category.html', {"category": category})
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect('category')

def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(request, "Category deleted successfully.")
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
    return redirect('category')
    
def customer_view(request):
    
    
    customers = Customer.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        date_joined = request.POST.get('date_joined')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        
        if not name or not phone or not category_id:
            messages.error(request, "All fields are required.")
            return redirect('customers')

        new_customer = Customer.objects.create(name=name, phone=phone, category=category, date_joined=date_joined)
        new_customer.save()
        messages.success(request, "Customer added successfully.")
        return redirect('customers')
    
    return render(request, 'main_parts/customers.html', {"customers": customers, "categories": categories})
def edit_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        categories = Category.objects.all()
        if request.method == 'POST':
            customer.name = request.POST.get('name')
            customer.phone = request.POST.get('phone')
            category_id = request.POST.get('category')
            customer.category = Category.objects.get(id=category_id)
            customer.date_joined = request.POST.get('date_joined')
            customer.save()
            messages.success(request, "Customer updated successfully.")
            return redirect('customers')
        else:
            return render(request, 'main_parts/edit_customer.html', {"customer": customer, "categories": categories})
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found.")
        return redirect('customers')
    
def delete_customer(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
        customer.delete()
        messages.success(request, "Customer deleted successfully.")
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found.")
    return redirect('customers')

def progress_view(request, customer_id):
    try:
        customer = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        messages.error(request, "Customer not found.")
        print('gg')
        return redirect('customers')

    if request.method == 'POST':
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        
        try:
            new_progress = Progress.objects.create(
                customer=customer,
                progress_description=request.POST.get('progress_description'),
                picture=request.FILES.get('picture'),
                weight=weight,
                height=height,
                total_body_water=request.POST.get('total_body_water'),
                body_fat_mass=request.POST.get('body_fat_mass'),
                skeletal_muscle_mass=request.POST.get('skeletal_muscle_mass'),
                intracellular_fluid=request.POST.get('intracellular_fluid'),
                extracellular_fluid=request.POST.get('extracellular_fluid'),
                body_mass_index=request.POST.get('body_mass_index'),
                body_fat_percentage=request.POST.get('body_fat_percentage'),
                basal_metabolic_rate=request.POST.get('basal_metabolic_rate'),
            )
            messages.success(request, "Progress added successfully.")
            return redirect('customer_progress', customer_id=customer_id)
        except Exception as e:
            messages.error(request, f"Error creating progress: {str(e)}")
            return redirect('customer_progress', customer_id=customer_id)

    progress_list = Progress.objects.filter(customer=customer).order_by('-date')
    return render(request, 'main_parts/progress.html', {
        "customer": customer,
        "progress_list": progress_list,
    })
def delete_progress(request, progress_id):
    try:
        progress = Progress.objects.get(id=progress_id)
        customer_id = progress.customer.id
        progress.delete()
        messages.success(request, "Progress deleted successfully.")
    except Progress.DoesNotExist:
        messages.error(request, "Progress not found.")
        # fallback: redirect to customers if progress not found
        return redirect('customers')
    return redirect('customer_progress', customer_id=customer_id)