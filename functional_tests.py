from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #E goes to a todo app's homepage    
        self.browser.get('http://localhost:8000')

        #She notices the page title and header mention todo lists
        self.assertIn('To-Do',self.browser.title)
        self.fail('Finish the test')


        #She is invited to enter a todo item right away
        
        #E types 'buy peacock feathers' into a textbox
        
        #when she hits enter the page updates and now the page lists 'buy peacock feathers' in 
        #a todo list
        
        #still a text box inviting another todo add (she adds ' make a fly' )
        
        #page updates again and shows both items
        
        #E sees that the site has made a unique url for her list and some explanatory text
        #to that effect
        
        #she vists the url and the list is still there

if __name__ == '__main__':
    unittest.main(warnings='ignore')
