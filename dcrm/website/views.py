from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    records= Record.objects.all()

    #Check to see if user is logged in 
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate user
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"You have been logged in")
            return redirect('home')
        else:
            messages.error(request,"Invalid username or password")
            return redirect('home')
    else:
        return render(request, 'home.html',{'records':records})


def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out")
    return render(request, 'home.html',{})

def register_user(request):
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username= form.cleaned_data.get('username')
            password= form.cleaned_data.get('password1')
            user= authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"You have been registered")
            return render(request, 'home.html',{})
    else:
        form=SignUpForm()
        return render(request, 'register.html',{'form':form})  
    return render(request, 'register.html',{'form':form})  

def customer_record(request,pk):
    if request.user.is_authenticated:
        # look up the record
        customer_record =  Record.objects.get(pk=pk)
        return render(request, 'record.html',{'customer_record':customer_record}) 
    else:
        messages.success(request,"You must be logged in to view a record")
        return render(request, 'home.html',{})

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it=Record.objects.get(pk=pk)
        delete_it.delete()
        messages.success(request,"Record has been deleted")
        return redirect('home')
    else:
        messages.success(request,"Login to delete a record")
        return render(request, 'home.html',{})
    
def add_record(request):
    form=AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            
            if form.is_valid():
                add_record=form.save()
                messages.success(request,"Record has been added")
                return redirect('home')
        else:
            return render(request, 'add_record.html',{'form':form})
    else:
        messages.success(request,"Login to add a record")
        return render(request, 'home.html',{})


def update_record(request,pk):
    if request.user.is_authenticated:
        # look up the record
        customer_record =  Record.objects.get(pk=pk)
        form=AddRecordForm(request.POST or None, instance=customer_record)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request,"Record has been updated")
                return redirect('home')
        else:
            return render(request, 'update_record.html',{'form':form})
    else:
        messages.success(request,"Login to update a record")
        return render(request, 'home.html',{})