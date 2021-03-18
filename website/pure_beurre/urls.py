from django.urls import path

from .views import Index, Results, DetailProduct


urlpatterns = [
    path('', Index.as_view(), name='index_view'),
    path('results/<str:food>/', Results.as_view(), name='category'),
    path('food/<int:id>', DetailProduct.as_view(), name='food_detail')

]
