from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import ContactPage

# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hey Account has been created for {username}')
            return redirect('home')
            
    form = UserCreationForm()
    return render(request, 'users/register.html',{'form':form})

def contact(request):
    if request.method == "POST":
        
        name = request.POST.get("name","")
        email = request.POST.get("email","")
        message = request.POST.get("message","")
        contact = ContactPage(name=name,email=email,message=message)
        contact.save()
        return redirect('home')
  
         
    return render(request, 'users/contact.html')    