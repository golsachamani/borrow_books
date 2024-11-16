from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import base,FormView
from django.contrib.auth import logout,authenticate,login
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from django.http import HttpRequest
from . import models
from . import forms
from books import models as book_models
# Create your views here.


class Signin(base.View):
    template_name = 'registration/signin.html'

    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect('home')
        form = forms.Login()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = forms.Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(
                request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                profile,created_profile = models.Profile.objects.get_or_create(
                    nikename=user.username, 
                    bio = "",
                    user = user,
                )
                
                return redirect('home')

        return render(request, 'registration/signin.html', context={'form': form})


class Signout(base.View):

    def get(self, request):
        logout(request)
        return redirect('home')

    def post(self, request):
        logout(request)
        return redirect('home')

class Signup(FormView):
    form_class = forms.Signup
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        result = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
@require_http_methods(['GET','POST'])
def profile(request,pk):
    if request.method == 'GET':
        profile = models.Profile.objects.get(pk=pk)
        borrowed_books = book_models.BookInstace.objects.filter(borrower=request.user)

        return render(request, 'profile.html', context={'profile':profile,'borrowed_books': borrowed_books})
    
    if request.method== 'POST':
        form = forms.Profile(request.data)
        if form.is_valid():
            form.save(commit=True)
            return redirect(request.user.profile.get_absolute_url())