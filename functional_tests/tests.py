from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

    @staticmethod
    def getBrowser():
        browser = webdriver.Firefox()
        # browser = webdriver.PhantomJS()
        return browser

    def setUp(self):
        self.browser = NewVisitorTest.getBrowser()
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
        self.browser.get(self.live_server_url)

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
        edith_list_url = self.browser.current_url;
        self.assertRegex(edith_list_url,'/lists/.+');
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        #still a text box inviting another todo add (she adds ' build a hat' )
        todo_item_2 = 'use feathers to build hat'
        # NAB -- apparently have to reget the input box
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('use feathers to build hat')
        inputbox.send_keys(Keys.ENTER)
        self.browser.implicitly_wait(1)
        #page updates again and shows both items
        self.check_for_row_in_list_table('2: use feathers to build hat')
        #E sees that the site has made a unique url for her list and some explanatory text
        #  to that effect
        #she vists the url and the list is still there

        # a new user, Francis, comes to the site
        ## Use a new browser session to try so that no cookies or private data of edith's are left
        self.browser.quit()
        self.browser = NewVisitorTest.getBrowser()
        self.browser.get(self.live_server_url)

        # francis adds a todo
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Eat radishes')
        inputbox.send_keys(Keys.ENTER)
        # francis gets his very own url
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url,'/lists/.+')
        self.assertNotEqual(francis_list_url,edith_list_url)
        # no trace of edith's list
        page_text = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('Buy peacock feathers',page_text)
        self.assertIn('Eat radishes',page_text)

        self.fail('finish the test')
