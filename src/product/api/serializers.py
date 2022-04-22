from rest_framework import serializers

from product import models as models_product


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop("fields", None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class VariantSerializer(DynamicFieldsModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = models_product.Variant
        fields = ["id", "title", "description", "active", "created_at"]

    def get_created_at(self, obj):
        created_at = obj.created_at
        timestamp_format = "%d-%B-%YY"
        formated_datetime = created_at.strftime(timestamp_format)
        return formated_datetime


class ProductImageSerializer(DynamicFieldsModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = models_product.ProductImage
        fields = ["id", "product", "file_path"]

    def get_created_at(self, obj):
        created_at = obj.created_at
        timestamp_format = "%d-%B-%YY"
        formated_datetime = created_at.strftime(timestamp_format)
        return formated_datetime


class ProductVariantSerializer(DynamicFieldsModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = models_product.ProductVariant
        fields = ["id", "variant_title", "variant", "product", "created_at"]

    def get_created_at(self, obj):
        created_at = obj.created_at
        timestamp_format = "%d-%B-%YY"
        formated_datetime = created_at.strftime(timestamp_format)
        return formated_datetime


class ProductVariantPriceSerializer(DynamicFieldsModelSerializer):
    created_at = serializers.SerializerMethodField()

    product_variant_one_display = ProductVariantSerializer(
        read_only=True, source="product_variant_one"
    )
    product_variant_two_display = ProductVariantSerializer(
        read_only=True, source="product_variant_two"
    )
    product_variant_three_display = ProductVariantSerializer(
        read_only=True, source="product_variant_three"
    )

    class Meta:
        model = models_product.ProductVariantPrice
        fields = [
            "id",
            "product_variant_one",
            "product_variant_two",
            "product_variant_three",
            "product_variant_one_display",
            "product_variant_two_display",
            "product_variant_three_display",
            "price",
            "stock",
            "product",
            "created_at",
        ]

    def get_created_at(self, obj):
        created_at = obj.created_at
        timestamp_format = "%d-%B-%YY"
        formated_datetime = created_at.strftime(timestamp_format)
        return formated_datetime


class ProductSerializer(DynamicFieldsModelSerializer):
    created_at = serializers.SerializerMethodField()

    productvariantprices_display = ProductVariantPriceSerializer(
        read_only=True, many=True, source="productvariantprices"
    )

    class Meta:
        model = models_product.Product
        fields = [
            "id",
            "title",
            "sku",
            "description",
            "created_at",
            "productvariantprices_display",
        ]

    def get_created_at(self, obj):
        created_at = obj.created_at
        timestamp_format = "%d-%B-%YY"
        formated_datetime = created_at.strftime(timestamp_format)
        return formated_datetime
