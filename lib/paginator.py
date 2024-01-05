from rest_framework import pagination
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from lib.error_codes import INVALID_PAGE
from lib.exceptions import CustomAPIException


class DefaultOffsetPagination(pagination.PageNumberPagination):
    page_size_query_param = "per_page"

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "per_page": self.page.paginator.per_page,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except NotFound:
            raise CustomAPIException(
                INVALID_PAGE,
                "Page Not Found",
                404,
            )
