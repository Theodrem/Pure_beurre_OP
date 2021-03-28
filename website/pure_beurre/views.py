from django.shortcuts import render
from django.http import HttpResponseRedirect
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
        return render(request, self.template_name, {'form': form})


class Results(View):
    template_name = "pure_beurre/results.html"

    def get(self, request):
        cat = None
        p = None
        food = request.GET.get("food")
        try:
            cat = Category.objects.get(name__icontains=food)  # contains pour filtrer
        except Category.DoesNotExist:
            try:
                products = Product.objects.all().filter(name__icontains=food).order_by("name")
                try:
                    p = products[0]
                    cat = p.category
                except IndexError:
                    pass
            except Product.DoesNotExist:
                pass

        if p is not None:
            list_product = Product.objects.all().filter(category=cat, nutriscore__lte=p.nutriscore).order_by("nutriscore")
        elif cat is not None:
            list_product = Product.objects.all().filter(category=cat).order_by("nutriscore")
        else:
            list_product = Product.objects.all().order_by("nutriscore")
        paginator = Paginator(list_product, 18)  # Show 6 products per page
        page = request.GET.get('page')
        products = paginator.get_page(page)

        return render(request, self.template_name, {'products': products, 'cat': cat, 'p': p})

    @method_decorator(login_required, name='dispatch')
    def post(self, request):
        food_id = request.POST['food_id']
        current_user = request.user
        p = Product(id=food_id)
        sub = Substitute(product=p,
                         user=current_user)
        sub.save()
        print(food_id)
        return HttpResponseRedirect('/my_products/')


class DetailProduct(View):
    template_name = "pure_beurre/food_detail.html"

    def get(self, request, id):
        prod = Product.objects.get(id=id)
        return render(request, self.template_name, {"prod": prod})


@method_decorator(login_required, name='dispatch')
class MyProducts(View):
    template_name = "pure_beurre\my_products.html"

    def get(self, request):
        current_user = request.user
        list_product = Product.objects.all().filter(substitute__user=current_user)
        paginator = Paginator(list_product, 18)  # Show 6 products per page
        page = request.GET.get('page')
        products = paginator.get_page(page)
        return render(request, self.template_name, {'products': products})
