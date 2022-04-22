from django.views import generic

from product.models import Variant


class CreateProductView(generic.TemplateView):
    template_name = "products/create.html"

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values("id", "title")
        context["product"] = True
        context["variants"] = list(variants.all())
        return context


class ProductListView(generic.TemplateView):
    template_name = "products/product_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context["product"] = True
        return context
