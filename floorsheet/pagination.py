from rest_framework.pagination import PageNumberPagination

class DynamicPageSizePagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Parameter to set page size dynamically
    max_page_size = 100  # Maximum allowable page size to prevent abuse
