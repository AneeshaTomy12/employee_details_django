from django.shortcuts import render,redirect
from accounts.form import CreateuserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

 
def home(request):
    if request.method=='POST':
        username=request.POST.get('user')
        password=request.POST.get('pass')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            # if(request.user.is_prof==True):
            #     return redirect('/admin', )
            # else:
            return redirect('profile/')
            # return redirect('/profile')
        else:
            return render(request,'index.html',{
                'error_msg':'Login Failed'})
            

    return render(request,'index.html')

def register(request):
    form=CreateuserForm()
    context={'form':form}
    if request.method=='POST':
        form=CreateuserForm(request.POST) 
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request,'register.html',context)

@login_required(login_url='index')
def profile(request):
    return render(request,'profile.html')

def logoutpage(request):
    logout(request)
    return redirect('index')

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "templates/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("templates/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="templates/password_reset.html", context={"password_reset_form":password_reset_form})


