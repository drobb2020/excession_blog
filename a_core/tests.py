from django.test import SimpleTestCase
from django.urls import resolve, reverse

from .views import AboutPageView, ContactPageView, IndexPageView


class HomePageTest(SimpleTestCase):
    def setUp(self):
        url = reverse("index")
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)

    def test_indexpage_template(self):
        self.assertTemplateUsed(self.response, "a_core/index.html")

    def test_indexpage_contains_correct_html(self):
        self.assertContains(self.response, "Excession Development Blog")

    def test_indexpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_indexpage_url_resolves_indexpageview(self):
        view = resolve("/")
        self.assertEqual(view.func.__name__, IndexPageView.as_view().__name__)


class AboutPageTest(SimpleTestCase):
    def setUp(self):
        url = reverse("about")
        self.response = self.client.get(url)

    def test_aboutpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_aboutpage_template(self):
        self.assertTemplateUsed(self.response, "a_core/about.html")

    def test_aboutpage_contains_correct_html(self):
        self.assertContains(self.response, "About Excession Blog")

    def test_aboutpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_aboutpage_url_resolves_aboutpageview(self):
        view = resolve("/about/")
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)


class ContactPageTest(SimpleTestCase):
    def setUp(self):
        url = reverse("contact")
        self.response = self.client.get(url)

    def test_contactpage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_contactpage_template(self):
        self.assertTemplateUsed(self.response, "a_core/contact.html")

    def test_contactpage_contains_correct_html(self):
        self.assertContains(self.response, "Contact Us")

    def test_contactpage_does_not_contain_incorrect_html(self):
        self.assertNotContains(self.response, "Hi there! I should not be on the page.")

    def test_contactpage_url_resolves_contactpageview(self):
        view = resolve("/contact/")
        self.assertEqual(view.func.__name__, ContactPageView.as_view().__name__)
