from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import ContactForm 

def home(request):
    return render(request, "home.html", {})

class ContactUsView(FormView):
    template_name = "contact_form.html"
    form_class = ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)
