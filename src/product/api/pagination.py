from rest_framework.pagination import PageNumberPagination


class GlobalPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 50


def pagination_for_non_model_viewset(request, queryset, page_size, serializer_class):
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    page = paginator.paginate_queryset(queryset, request)
    serializer = serializer_class(page, many=True, context={"request": request})
    paginated_response = paginator.get_paginated_response(serializer.data)
    return paginated_response
