from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .form import AskFoodform
from .models import Category, Product, Substitute
import os


class Index(View):
    """
    Index page
    """
    form = AskFoodform
    template_name = "product/index.html"

    def get(self, request):
        """
        Send research form
        if form is valid redirect user on results page
        """
        form = self.form(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/results/')
        else:
            form = self.form
        return render(request, self.template_name, {'index_form': form})


class Results(View):
    """
    Results page
    """
    template_name = "product/results.html"

    def get(self, request):
        """
        Get form value
        If the value is a category display the products of the category.
        If the value is a product displays the products of the product category.
        If not displays all products.
        """
        category = ""
        product = ""
        food = request.GET.get("food")
        try:
            cat = Category.objects.all().filter(name__icontains=food).order_by("name")
            category = cat[0]
            list_product = Product.objects.all().filter(category=category).order_by("nutriscore")
        except (Category.DoesNotExist, IndexError):
            try:
                products = Product.objects.all().filter(name__icontains=food).order_by("name")
                product = products[0]
                cat = product.category
                list_product = Product.objects.all().filter(category=cat,
                                                            nutriscore__lte=product.nutriscore).order_by("nutriscore")
            except (Product.DoesNotExist, IndexError):
                list_product = Product.objects.all().order_by("nutriscore")

        paginator = Paginator(list_product, 18)  # Show 6 products per page
        page = request.GET.get('page')
        products = paginator.get_page(page)

        return render(request, self.template_name,
                      {'products': products, 'category': category, 'product': product, 'food': food})

    @method_decorator(login_required)
    def post(self, request):
        """
        If the user is logged in, he can save a substitute.
        """
        food_id = request.POST['food_id']
        current_user = request.user  # get current user
        p = Product(id=food_id)
        try:
            Product.objects.get(substitute__user=current_user, substitute__product=p)
        except Product.DoesNotExist:
            sub = Substitute(product=p,
                             user=current_user)
            sub.save()
        return HttpResponseRedirect('/my_products')


class DetailProduct(View):
    """
    Page Detail food
    """
    template_name = "product/food_detail.html"

    def get(self, request, id):
        """
        displays the details of the selected product
        """
        try:
            prod = Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

        return render(request, self.template_name, {"prod": prod})


class MyProducts(View):
    """
    Page My product
    """
    template_name = "product/my_products.html"

    @method_decorator(login_required, name='dispatch')
    def get(self, request):
        """
        The logged in user can see their products
        """
        current_user = request.user
        list_product = Product.objects.all().filter(substitute__user=current_user).order_by("nutriscore")
        paginator = Paginator(list_product, 18)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        return render(request, self.template_name, {'products': products})


class LegalNotice(View):
    """
    Legal notices page
    """
    template_name = "product/legal_notice.html"

    def get(self, request):
        return render(request, self.template_name)
