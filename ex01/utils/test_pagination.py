from unittest import TestCase
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_return_pagination_range(self):
        pagination = make_pagination_range(
            list_range=list(range(1, 21)),
            pages=4,
            current_page=1
        )

        self.assertEqual(pagination, [1, 2, 3, 4])

    def test_pagination_range(self):
        ...
