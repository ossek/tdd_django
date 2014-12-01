from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from lists.views import home_page
from django.template.loader import render_to_string
from lists.models import Item, List

class ListViewTest(TestCase):

    def test_displays_only_items_for_that_list(self):
        new_item_text1 = 'first item'
        new_item_text2 = 'second item'

        correct_list = List.objects.create()
        Item.objects.create(text = new_item_text1,owningList = correct_list)
        Item.objects.create(text = new_item_text2,owningList = correct_list)
        other_list = List.objects.create()
        Item.objects.create(text = 'bollocks', owningList = other_list)
        Item.objects.create(text = 'shenanigans', owningList = other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))
        ## alternatively: 
        # request = HttpRequest()
        # response = home_page(request)

        self.assertContains(response,new_item_text1)
        self.assertContains(response,new_item_text2)
        self.assertNotContains(response,'bollocks')
        self.assertNotContains(response,'shenanigans')

    def test_uses_list_template(self):
        new_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (new_list.id,))
        self.assertTemplateUsed(response,'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'],correct_list)

class NewItemTest(TestCase):

    def test_can_save_POST_request_to_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        self.client.post('/lists/%d/add_item' % (correct_list.id,), \
                data = {'item_text' : 'new for existing list'})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text,'new for existing list')
        self.assertEqual(new_item.owningList, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.post('/lists/%d/add_item' % (correct_list.id,), \
                data = {'item_text' : 'new for existing list'})
        self.assertRedirects(response,'/lists/%d/' % (correct_list.id,))


class NewListTest(TestCase):

    def test_redirects_after_post(self):
        new_item_text = 'A new list item'
        response = self.client.post('/lists/new', \
                data = {'item_text':new_item_text})
        new_list = List.objects.first()
        self.assertRedirects(response,'/lists/%d/' % (new_list.id,))
        ## alternatively: 
        # self.assertEqual(response.status_code,302)
        # self.assertEqual(response['location'],'/lists/the-only-list-in-the-world/')

    def test_saving_a_post_request(self):
        new_item_text = 'A new list item'
        response = self.client.post('/lists/new', \
                data = {'item_text':new_item_text})
        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, new_item_text)
   

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

    
class ListAndItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        first_item_text = 'The first (ever) list item'
        first_item = Item()
        first_item.owningList = list_
        first_item.text = first_item_text
        first_item.save()

        second_item_text = 'Item the second'
        second_item = Item()
        second_item.owningList = list_
        second_item.text = second_item_text
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list,list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(),2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text,first_item_text)
        self.assertEqual(first_saved_item.owningList,list_)
        self.assertEqual(second_saved_item.text,second_item_text)
        self.assertEqual(second_saved_item.owningList,list_)
