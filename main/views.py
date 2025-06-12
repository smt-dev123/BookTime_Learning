from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models
from . import forms  # Added missing import for forms
import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, "home.html", {})

class SignupView(FormView):
    template_name = "signup.html"
    form_class = forms.UserCreationForm
    def get_success_url(self):
        redirect_to = self.request.GET.get("next", "/")
        return redirect_to
    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info("New signup for email=%s through SignupView", email)
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        form.send_mail()
        messages.info(self.request, "You signed up successfully.")
        return response

class ContactUsView(FormView):
    template_name = "contact_form.html"
    form_class = forms.ContactForm
    success_url = "/"

    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)

class ProductListView(ListView):
    template_name = "main/product_list.html"
    paginate_by = 4

    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None

        if tag != "all":
            self.tag = get_object_or_404(models.ProductTag, slug=tag)

        if self.tag:
            products = models.Product.objects.filter(active=True, tags=self.tag)
        else:
            products = models.Product.objects.filter(active=True)

        return products.order_by("name")

class AddressListView(LoginRequiredMixin, ListView):
    model = models.Address
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class AddressCreateView(LoginRequiredMixin, CreateView):
    model = models.Address
    fields = ["name", "address1", "address2", "zip_code", "city", "country"]
    success_url = reverse_lazy("address_list")
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Address
    fields = ["name", "address1", "address2", "zip_code", "city", "country"]
    success_url = reverse_lazy("address_list")
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Address
    success_url = reverse_lazy("address_list")
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

def add_to_basket(request):
    product_id = request.GET.get("product_id")
    if not product_id:
        messages.error(request, "No product ID provided.")
        return redirect("product_list")  # Redirect to product list or another view

    product = get_object_or_404(models.Product, pk=product_id)

    # Ensure basket exists
    if not hasattr(request, 'basket') or not request.basket:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        basket = models.Basket.objects.create(user=user)
        request.session["basket_id"] = basket.id
        request.basket = basket
    else:
        basket = request.basket

    # Add or update basket line
    basketline, created = models.BasketLine.objects.get_or_create(
        basket=basket,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        basketline.quantity += 1
        basketline.save()
        messages.info(request, "Updated quantity in basket.")
    else:
        messages.success(request, "Product added to basket.")

    return HttpResponseRedirect(reverse("product", args=(product.slug,)))

def manage_basket(request):
    if not hasattr(request, 'basket') or not request.basket:
        return render(request, "basket.html", {"formset": None})

    if request.method == "POST":
        formset = forms.BasketLineFormSet(request.POST, instance=request.basket)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Basket updated successfully.")
    else:
        formset = forms.BasketLineFormSet(instance=request.basket)

    if request.basket.is_empty():
        return render(request, "basket.html", {"formset": None})

    return render(request, "basket.html", {"formset": formset})
    
def create_order(self, billing_address, shipping_address):
    if not self.user:
        raise exceptions.BasketException(
        "Cannot create order without user"
        )
    logger.info(
    "Creating order for basket_id=%d"
    ", shipping_address_id=%d, billing_address_id=%d",
    self.id,
    shipping_address.id,
    billing_address.id,)

    order_data = {
    "user":self.user,
    "billing_name": billing_address.name,
    "billing_address1": billing_address.address1,
    "billing_address2": billing_address.address2,
    "billing_zip_code": billing_address.zip_code,
    "billing_city": billing_address.city,
    "billing_country": billing_address.country,
    "shipping_name": shipping_address.name,
    "shipping_address1": shipping_address.address1,
    "shipping_address2": shipping_address.address2,
    "shipping_zip_code": shipping_address.zip_code,
    "shipping_city": shipping_address.city,
    "shipping_country": shipping_address.country,
    }

    order = Order.objects.create(**order_data)
    c = 0
    for line in self.basketline_set.all():
        for item in range(line.quantity):
            order_line_data = {
            "order": order,
            "product": line.product,
            }
            order_line = OrderLine.objects.create(**order_line_data)
            c += 1
    logger.info(
    "Created order with id=%d and lines_count=%d",
    order.id,
    c,)
    self.status = Basket.SUBMITTED
    self.save()
    return order

class AddressSelectionView(LoginRequiredMixin, FormView):
    template_name = "address_select.html"
    form_class = forms.AddressSelectionForm
    success_url = reverse_lazy('checkout_done')
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    def form_valid(self, form):
        del self.request.session['basket_id']
        basket = self.request.basket
        basket.create_order(
        form.cleaned_data['billing_address'],
        form.cleaned_data['shipping_address']
        )
        return super().form_valid(form)