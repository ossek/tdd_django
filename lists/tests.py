from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string

class HomePageTest(TestCase):

 def test_root_url_resolves_to_home_page_view(self):
    found = resolve('/')
    print(found)
    print(found.func)
    # simply assert that the function we resolved to == home_page from views.py/lists.views
    self.assertEqual(found.func, home_page)

 def test_home_page_returns_correct_html(self):
    request = HttpRequest()
    response = home_page(request)
    expected_html = render_to_string('home.html')
    self.assertEqual(response.content.decode(),expected_html)
