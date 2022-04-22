from django.contrib import admin
from product import models as models_product

admin.site.register(models_product.Variant)
admin.site.register(models_product.Product)
admin.site.register(models_product.ProductImage)
admin.site.register(models_product.ProductVariant)
admin.site.register(models_product.ProductVariantPrice)
