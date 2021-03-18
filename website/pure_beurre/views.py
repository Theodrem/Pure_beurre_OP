from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.views import View
from .form import AskFoodform
from .models import Category, Product


class Index(View):
    form = AskFoodform
    template_name = "pure_beurre/index.html"

    def get(self, request):
        form = self.form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = self.form(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('/results/%s' % form.data['food'])
                
        else:
            form = self.form

        return render(request, self.template_name, {'form': form})


class Results(View):
    template_name = "pure_beurre/page_category.html"

    def get(self, request, food):
        try:
            cat = Category.objects.get(name=food)
        except Category.DoesNotExist:
            try:
                p = Product.objects.get(name=food)
                return HttpResponseRedirect('/food/%s' % p.id)
            except Product.DoesNotExist:
                return HttpResponseRedirect('/')

        list_product = Product.objects.all().filter(category_id=cat.id)
        paginator = Paginator(list_product, 6)  # Show 25 contacts per page
        page = request.GET.get('page')
        products = paginator.get_page(page)
        return render(request, self.template_name, {'products': products, 'cat': cat})


class DetailProduct(View):
    template_name = "pure_beurre/food_detail.html"

    def get(self, request, id):
        prod = Product.objects.get(id=id)
        list_substitute = Product.objects.all().filter(category_id=prod.category_id, nutriscore__lte=prod.nutriscore).order_by("nutriscore")
        return render(request, self.template_name, {"prod": prod,
                                                    "subs": list_substitute})
