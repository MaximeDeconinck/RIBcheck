from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import NewUserForm, RIBForm
from .models import CustomUser, LogEntry
from .signature import RIBsignature

def index(request):
  return render(request, 'mainapp/index.html')

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				LogEntry.objects.create(user=request.user, message="Successful login of user ID {}".format(user.id))
				return redirect('mainapp:profile')
			else:
				messages.error(request,"Invalid username or password")
				LogEntry.objects.create(user=request.user, message="Failed login of user ID {}".format(user.id))
		else:
			messages.error(request,"Invalid username or password")
	form = AuthenticationForm()
	return render(request=request, template_name="mainapp/login.html", context={"login_form":form})

def logout_request(request):
	LogEntry.objects.create(user=request.user, message="Log out of user ID {}".format(request.user.id))
	logout(request)
	messages.info(request, "You have successfully logged out") 
	return redirect('mainapp:index')

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful" )
			LogEntry.objects.create(user=request.user, message="Registration successful of user ID {}".format(user.id))
			return redirect('mainapp:index')
		messages.error(request, "Unsuccessful registration : invalid information")
	form = NewUserForm()
	return render(request=request, template_name="mainapp/register.html", context={"register_form":form})

def profile(request):
	if request.user.is_superuser:
		User = get_user_model()
		users = User.objects.all()
		return render(request=request, template_name="mainapp/profile.html", context={"users_info":users})
	else:
		user = request.user
		return render(request=request, template_name="mainapp/profile.html", context={"user_info":user})

def newuser(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, "User creation successful" )
			LogEntry.objects.create(user=request.user, message="User creation successful of user ID {}".format(user.id))
			return redirect('mainapp:profile')
		messages.error(request, "Unsuccessful user creation : invalid information")
	form = NewUserForm()
	return render(request=request, template_name="mainapp/newuser.html", context={"register_form":form})

def checklist(request):
    users = CustomUser.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'mainapp/checklist.html', context)

def check(request, customuser_id):
    user = get_object_or_404(CustomUser, id=customuser_id)
    if request.method == "POST":
        form = RIBForm(request.POST)
        if form.is_valid():
            salt = user.salt
            test_signature = RIBsignature(str(form.cleaned_data['username']), str(form.cleaned_data['adress']), str(form.cleaned_data['country']), str(form.cleaned_data['iban']), salt)
            if user.signature == test_signature:
                messages.success(request, "Successful verification: the RIB you entered is authentic")
                LogEntry.objects.create(user=request.user, message="Successful verification for user ID {} : ".format(customuser_id) + "test signature = " + test_signature + " vs true signature = " + user.signature)
            else:
                messages.error(request, "Unsuccessful verification: make sure that the information you entered is correct")
                LogEntry.objects.create(user=request.user, message="Unsuccessful verification for user ID {} : ".format(customuser_id) + "test signature = " + test_signature + " vs true signature = " + user.signature)
    else:
        form = RIBForm()
    return render(request=request, template_name="mainapp/check.html", context={"rib_form": form})

def view_logs(request):
    logs = LogEntry.objects.order_by('-timestamp')
    return render(request, 'mainapp/logs.html', {'logs': logs})