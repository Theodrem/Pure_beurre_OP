from django.urls import path

from .views import Index, Results, DetailProduct, MyProducts


urlpatterns = [
    path('', Index.as_view(), name='index_view'),
    path('results/', Results.as_view(), name='results_view'),
    path('food/<int:id>', DetailProduct.as_view(), name='food_detail'),
    path('my_products/', MyProducts.as_view(), name='my_products')

]
