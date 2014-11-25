from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        #have selenium wait a few extra seconds for page load just in case
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

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
        inputbox.send_keys(keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(
                any(row.text == '1: Buy peacock feathers' for row in rows)
                )

        #still a text box inviting another todo add (she adds ' make a fly' )
        self.fail('finish the test')

        #page updates again and shows both items

        #E sees that the site has made a unique url for her list and some explanatory text
        #to that effect

        #she vists the url and the list is still there

if __name__ == '__main__':
    unittest.main(warnings='ignore')
