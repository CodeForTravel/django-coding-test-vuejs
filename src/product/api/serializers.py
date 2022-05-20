from rest_framework import serializers
from django.db import transaction
from django.db.models import Q
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
        timestamp_format = "%d-%B-%Y"
        formated_datetime = created_at.strftime(timestamp_format)
        return formated_datetime


class ProductImageSerializer(DynamicFieldsModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = models_product.ProductImage
        fields = ["id", "product", "file_path"]

    def get_created_at(self, obj):
        created_at = obj.created_at
        timestamp_format = "%d-%B-%Y"
        formated_datetime = created_at.strftime(timestamp_format)
        return formated_datetime


class ProductVariantSerializer(DynamicFieldsModelSerializer):
    created_at = serializers.SerializerMethodField()
    variant_root_title = serializers.CharField(source="variant.title")

    class Meta:
        model = models_product.ProductVariant
        fields = [
            "id",
            "variant_title",
            "variant",
            "variant_root_title",
            "product",
            "created_at",
        ]

    def get_created_at(self, obj):
        created_at = obj.created_at
        timestamp_format = "%d-%B-%Y"
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
        timestamp_format = "%d-%B-%Y"
        formated_datetime = created_at.strftime(timestamp_format)
        return formated_datetime


class ProductSerializer(DynamicFieldsModelSerializer):
    created_at = serializers.SerializerMethodField()

    productvariantprices_display = ProductVariantPriceSerializer(
        read_only=True, many=True, source="productvariantprices"
    )
    productvariants_display = ProductVariantSerializer(
        read_only=True, many=True, source="productvariants"
    )

    product_variant = serializers.ListField(write_only=True, required=False)
    product_variant_prices = serializers.ListField(write_only=True, required=False)
    product_image = serializers.ListField(write_only=True, required=False)
    productimages = ProductImageSerializer(read_only=True, many=True)

    class Meta:
        model = models_product.Product
        fields = [
            "id",
            "title",
            "sku",
            "description",
            "created_at",
            "productvariantprices_display",
            "productvariants_display",
            "product_variant",
            "product_variant_prices",
            "product_image",
            "productimages",
        ]

    def get_created_at(self, obj):
        created_at = obj.created_at
        timestamp_format = "%d-%B-%Y"
        formated_datetime = created_at.strftime(timestamp_format)
        return formated_datetime

    @transaction.atomic
    def create(self, validated_data):

        product_variants = validated_data.pop("product_variant")
        product_variant_prices = validated_data.pop("product_variant_prices")
        product_image = validated_data.pop("product_image")

        # creating product
        product = models_product.Product.objects.create(**validated_data)

        # creating product varinat
        for product_variant in product_variants:
            tags = product_variant.get("tags")
            option = int(product_variant.get("option"))
            varint = models_product.Variant.objects.get(id=option)
            for tag in tags:
                product_variant = models_product.ProductVariant.objects.create(
                    variant_title=tag, variant=varint, product=product
                )

        # creating product price varinat
        for product_variant_price in product_variant_prices:
            title = product_variant_price.get("title")
            price = float(product_variant_price.get("price"))
            stock = float(product_variant_price.get("stock"))
            product_price_variant = models_product.ProductVariantPrice.objects.create(
                price=price, stock=stock, product=product
            )
            if title:
                title_list = title.split("/")
                for price_title in title_list:
                    if price_title:
                        product_variant = models_product.ProductVariant.objects.get(
                            variant_title=price_title, product=product
                        )
                    if product_variant:
                        if product_variant.variant.id == 1:
                            product_price_variant.product_variant_one = product_variant
                        elif product_variant.variant.id == 2:
                            product_price_variant.product_variant_two = product_variant
                        elif product_variant.variant.id == 3:
                            product_price_variant.product_variant_three = (
                                product_variant
                            )
                        product_price_variant.save()

        # creating image
        if product_image:
            file_path = product_image.get("file_path")
            models_product.ProductImage.objects.create(
                file_path=file_path, product=product
            )

        return product

    @transaction.atomic
    def update(self, instance, validated_data):

        product_variants = validated_data.pop("product_variant")
        product_variant_prices = validated_data.pop("product_variant_prices")
        product_image = validated_data.pop("product_image")

        instance.title = validated_data.get("title")
        instance.description = validated_data.get("description")
        instance.save()

        # creating/updating product varinat
        for product_variant in product_variants:
            tags = product_variant.get("tags")
            option = int(product_variant.get("option"))
            varint = models_product.Variant.objects.get(id=option)
            for tag in tags:
                (
                    product_variant_instance,
                    created,
                ) = models_product.ProductVariant.objects.get_or_create(
                    variant_title=tag, variant=varint, product=instance.id
                )

        models_product.ProductVariantPrice.objects.filter(product=instance).delete()
        # creating product price varinat
        for product_variant_price in product_variant_prices:
            title = product_variant_price.get("title")
            price = float(product_variant_price.get("price"))
            stock = float(product_variant_price.get("stock"))
            product_price_variant = models_product.ProductVariantPrice.objects.create(
                price=price, stock=stock, product=instance
            )
            if title:
                title_list = title.split("/")
                for price_title in title_list:
                    if price_title:
                        product_variant_instance = (
                            models_product.ProductVariant.objects.get(
                                variant_title=price_title, product=instance
                            )
                        )
                    if product_variant_instance:
                        if product_variant_instance.variant.id == 1:
                            product_price_variant.product_variant_one = (
                                product_variant_instance
                            )
                        elif product_variant_instance.variant.id == 2:
                            product_price_variant.product_variant_two = (
                                product_variant_instance
                            )
                        elif product_variant_instance.variant.id == 3:
                            product_price_variant.product_variant_three = (
                                product_variant_instance
                            )
                        product_price_variant.save()

        # creating image
        if product_image:
            file_path = product_image.get("file_path")
            models_product.ProductImage.objects.create(
                file_path=file_path, product=instance.id
            )

        return instance
