from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string

class HomePageTest(TestCase):

 # seems there is a convention that a test method must be started with 'test_'
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

 def test_can_save_a_post_request(self):
     request = HttpRequest()
     request.method = 'POST'
     request.POST['item_text'] = 'A new list item'

     response = home_page(request)

     self.assertIn('A new list item', response.content.decode())
     expected_html = render_to_string(
             'home.html',
             {'new_item_text': 'A new list item'}
             )
     self.assertEqual(response.content.decode(),expected_html)

