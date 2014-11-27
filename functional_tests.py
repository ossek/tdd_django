from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # self.browser = webdriver.PhantomJS()
        # have selenium wait a few extra seconds for page load just in case
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()


    # helpers
    def check_for_row_in_list_table(self,row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text,[row.text for row in rows],
                "new item did not appear in table -- its text was:\n%s" % \
                (table.text)
        )


    def test_can_start_a_list_and_retrieve_it_later(self):
        #E goes to a todo app's homepage
        self.browser.get('http://localhost:8000');

        #She notices the page title and header mention todo lists
        self.assertIn('To-Do',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

        #She is invited to enter a todo item right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
                )

        #E types 'Buy peacock feathers' into a textbox
        inputbox.send_keys('Buy peacock feathers')

        #when she hits enter the page updates and now the page lists 'buy peacock feathers' in
        #a todo list
        inputbox.send_keys(Keys.ENTER)

        self.browser.implicitly_wait(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        todo_item_2 = 'use feathers to build hat'
        # NAB -- apparently have to reget the input box
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('use feathers to build hat')
        inputbox.send_keys(Keys.ENTER)
        # self.check_for_row_in_list_table('2: %s' % todo_item_2)
        self.browser.implicitly_wait(1)
        self.check_for_row_in_list_table('2: use feathers to build hat')

        #still a text box inviting another todo add (she adds ' make a fly' )
        self.fail('finish the test')

        #page updates again and shows both items

        #E sees that the site has made a unique url for her list and some explanatory text
        #to that effect

        #she vists the url and the list is still there
        
if __name__ == '__main__':
    unittest.main(warnings='ignore')
