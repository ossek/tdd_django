from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item

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
   
    def test_home_page_can_save_a_post_request(self):
         new_item_text = 'A new list item'
   
         request = HttpRequest()
         request.method = 'POST'
         request.POST['item_text'] = new_item_text
   
         response = home_page(request)
   
         self.assertEqual(Item.objects.count(),1)
         new_item = Item.objects.first()
         self.assertEqual(new_item.text, new_item_text)
   

    def test_home_page_redirects_after_post(self):
        new_item_text = 'A new list item'

        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = new_item_text

        response = home_page(request)

        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'],'/')

        
    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertEqual(Item.objects.count(),0)

    def test_home_page_displays_all_list_items(self):
        new_item_text1 = 'first item'
        new_item_text2 = 'second item'

        Item.objects.create(text = new_item_text1)
        Item.objects.create(text = new_item_text2)

        request = HttpRequest()
        response = home_page(request)

        self.assertIn(new_item_text1,response.content.decode())
        self.assertIn(new_item_text2,response.content.decode())


class ItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        first_item_text = 'The first (ever) list item'
        first_item = Item()
        first_item.text = first_item_text
        first_item.save()

        second_item_text = 'Item the second'
        second_item = Item()
        second_item.text = second_item_text
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,first_item_text)
        self.assertEqual(second_saved_item.text,second_item_text)
