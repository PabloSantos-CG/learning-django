from unittest import TestCase
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_return_pagination_range(self):
        list_range = list(range(1, 21))

        pagination1 = make_pagination_range(list_range, 4, 1)['pagination']
        self.assertEqual(pagination1, [1, 2, 3, 4])

        pagination2 = make_pagination_range(list_range, 4, 6)['pagination']
        self.assertEqual(pagination2, [5, 6, 7, 8])

        pagination3 = make_pagination_range(list_range, 4, 15)['pagination']
        self.assertEqual(pagination3, [14, 15, 16, 17])

        pagination4 = make_pagination_range(list_range, 4, 20)['pagination']
        self.assertEqual(pagination4, [17, 18, 19, 20])
