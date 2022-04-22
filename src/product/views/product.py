from django.views import generic
from product.models import Variant, Product
from product.api import serializers as serializers_product


class CreateProductView(generic.TemplateView):
    template_name = "products/create.html"

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values("id", "title")
        context["product"] = True
        context["variants"] = list(variants.all())
        return context


class UpdateProductView(generic.TemplateView):
    template_name = "products/update.html"

    def get_context_data(self, **kwargs):
        product_id = kwargs.get("product_id")
        context = super(UpdateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values("id", "title")
        context["product"] = True
        context["variants"] = list(variants.all())
        product_obj = Product.objects.get(id=product_id)
        if product_obj:
            serializer = serializers_product.ProductSerializer(product_obj)
            context["product_obj"] = serializer.data

        return context


class ProductListView(generic.TemplateView):
    template_name = "products/product_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context["product"] = True
        return context
