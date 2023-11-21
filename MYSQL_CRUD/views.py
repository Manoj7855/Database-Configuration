from django.shortcuts import render ,redirect
from .forms import MyRegisterform
from django.contrib import messages
from .models import Registerform
# Create your views here.
def home(request):
    datas=Registerform.objects.all()

    return render(request,"home.html",{'datas':datas})

def insert(request):
    if request.method=='POST':
        form=MyRegisterform(request.POST)
        form.save()
        messages.success(request,"Registration Succcessfully completed")
        return redirect('Home')
    form=MyRegisterform()
    return render(request,"register.html",{'form':form})

def update(request,id):
    datas=Registerform.objects.get(id=id)
    if request.method=='POST':
        name=request.POST['name']
        age=request.POST['age']
        address=request.POST['address']
        contact=request.POST['contact']
        email=request.POST['email']
        
        datas.name=name
        datas.age=age
        datas.address=address
        datas.contact=contact
        datas.email=email
        datas.save()
        messages.success(request,'Update Successfully Completed')
        return redirect('Home')
    return render(request,"update.html",{'datas':datas})

def delete(request,id):
    data=Registerform.objects.get(id=id)
    data.delete()
    messages.error(request,'Delete Successfully Completed')
    return redirect('Home')
    
