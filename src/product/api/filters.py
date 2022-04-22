from rest_framework import filters


class SubscriptionGroupMembersFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_dict = {}
        variant = request.query_params.get("variant")
        from_price_range = request.query_params.get("from_price_range")
        to_price_range = request.query_params.get("to_price_range")
        created_date = request.query_params.get("created_date")

        if created_date:
            filter_dict["created_at"] = created_date

        if variant:
            filter_dict["productvariant__variant_title"] = variant

        if from_price_range:
            filter_dict["productvariantprices__price__gte"] = from_price_range

        if to_price_range:
            filter_dict["productvariantprices__price__lte"] = to_price_range

        if filter_dict:
            queryset = queryset.filter(**filter_dict)

        return queryset
