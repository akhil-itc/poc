from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import generic

from .  import forms


class RegisterView(generic .CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = "auth/signup.html"

    def form_valid(self, form):
        usr = form.save()

        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, generic.UpdateView):


    def get_success_url(self):
        return reverse('accounts:profile', kwargs={
            'pk': self.request.user.id,
        })

    def get_object(self):
        return self.request.user.profile
