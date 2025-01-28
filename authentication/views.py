from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# Create your views here.

@login_required
def account(request):
    template = 'account.html'
    user = request.user
    print(user)
    context = {'user': user} 
    return render(request, template, context)

@login_required
def update_profil(request):
    template = 'account.html'
    user = request.user
    print(user)
    context = {'user': user} 
    messages.warning(request, f"We have not provide this feature yet, {user.login}")

    return render(request, template, context)

def home(request):
    template = 'base.html' 
    context = {'obj': 2}
    return render(request, template, context)


from .forms import AccountForm, LoginForm

class Signup(TemplateView):

    template = 'fake_signup.html'
    template = 'signup.html'
    context = {}

    def get(self, request):
        print('user ', request.user)
        form = AccountForm()
        self.context = {'form': form}
        return render(request, self.template, self.context) 
    
    def post(self, request, *args, **kwargs):
        form = AccountForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            print(user)
            messages.success(request, f"Account created successfully! Welcome, {user.login}")
            #login(request, user) 
            return redirect('login')
        
        self.context = {'form': form}
        
        return render(request, self.template, self.context)


class Login(TemplateView):

    template = 'login.html'
    account_template = 'account.html'
    context = {}
    

    def get(self, request):
        form = LoginForm()
        self.context = {'form': form}
        print('user ', request.user)
        return render(request, self.template, self.context) 
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(email, password)
            user = authenticate(request, username=email, password=password)
            print("user", user)
            if user is not None:
                login(request, user)
                messages.success(request, "You loged in successfuly") 
                return redirect("account")
            else:
                messages.error(request, "Invalid login credentials.")
                form.add_error(None, "Invalid login credentials.")
        self.context = {'form': form}
        return render(request, self.template, self.context)


def logout_view(request):
    name = request.user.login
    logout(request)
    template = 'base.html'
    context = {'message': 'You log out '}
    messages.error(request, f"See u later, {name}")
    return redirect("home")