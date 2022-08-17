from rest_framework.pagination import PageNumberPagination


# TODO check pagination differences
# TODO think how to make endless scroll/pagination


class BasePageNumberPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "page"
    max_page_size = 50
    page_size_query_param = "page_size"
