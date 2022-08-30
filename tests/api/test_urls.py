from django.urls import reverse, resolve


class TestUrls:
    def test_book_page_url(self):
        path = reverse("book_page", kwargs={"pk": 1})
        assert resolve(path).view_name == "book_page"
