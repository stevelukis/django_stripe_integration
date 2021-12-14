from django.views import generic

from product.models import Product


class ProductListView(generic.ListView):
    model = Product
    template_name = 'product_list.html'
