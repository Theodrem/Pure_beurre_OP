from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .form import AskFoodform
from .models import Category, Product, Substitute


class Index(View):
    form = AskFoodform
    template_name = "pure_beurre/index.html"

    def get(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/results/')
        else:
            form = self.form
        return render(request, self.template_name, {'index_form': form})


class Results(View):
    template_name = "pure_beurre/results.html"

    def get(self, request):
        categories = ""
        product = ""
        food = request.GET.get("food")
        try:
            cat = Category.objects.all().filter(name__icontains=food).order_by("name")
            categories = cat[0]
            list_product = Product.objects.all().filter(category=categories).order_by("nutriscore")
        except (Category.DoesNotExist, IndexError):
            try:
                products = Product.objects.all().filter(name__icontains=food).order_by("name")
                product = products[0]
                categories = product.category
                list_product = Product.objects.all().filter(category=categories,
                                                            nutriscore__lte=product.nutriscore).order_by("nutriscore")
            except (Product.DoesNotExist, IndexError):
                list_product = Product.objects.all().order_by("nutriscore")

        paginator = Paginator(list_product, 18)  # Show 6 products per page
        page = request.GET.get('page')
        products = paginator.get_page(page)

        return render(request, self.template_name, {'products': products, 'c': categories, 'p': product, 'food': food})

    @method_decorator(login_required)
    def post(self, request):
        food_id = request.POST['food_id']
        current_user = request.user
        p = Product(id=food_id)
        try:
            Product.objects.get(substitute__user=current_user, substitute__product=p)
        except Product.DoesNotExist:
            sub = Substitute(product=p,
                             user=current_user)
            sub.save()
        return HttpResponseRedirect('/my_products')


class DetailProduct(View):
    template_name = "pure_beurre/food_detail.html"

    def get(self, request, id):
        try:
            prod = Product.objects.get(id=id)
        except Product.DoesNotExist:
            raise Http404

        return render(request, self.template_name, {"prod": prod})


class MyProducts(View):
    template_name = "pure_beurre\my_products.html"

    @method_decorator(login_required, name='dispatch')
    def get(self, request):
        current_user = request.user
        list_product = Product.objects.all().filter(substitute__user=current_user)
        paginator = Paginator(list_product, 18)
        page = request.GET.get('page')
        products = paginator.get_page(page)
        return render(request, self.template_name, {'products': products})


class LegalNotice(View):
    template_name = "pure_beurre/legal_notice.html"

    def get(self, request):
        return render(request, self.template_name)
