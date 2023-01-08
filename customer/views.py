from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, TemplateView, ListView
from customer.forms import RegistrationForm, LoginForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from api.models import Products

# Create your views here.

class SignUpView(CreateView):
    template_name = "signup.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request, "Account created successfully")
        return super().form_valid(form)

    def form_invalid(self, form) :
        messages.error(self.request, "Account creation failed")
        return super().form_invalid(form)


class SigninView(FormView):
    template_name = "cust-login.html"
    form_class= LoginForm

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            usr = authenticate(request, username = uname, password=pwd)
            if usr:
                login(request,usr)
                return redirect("user-home")
            else:
                messages.error(request, "invalid credentials")
                return render(request, "cust-login.html", {"form":form})

class HomeView(ListView):
    template_name = "cust-index.html"
    context_object_name = "products"
    model = Products

    