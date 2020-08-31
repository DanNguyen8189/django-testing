    from selenium import webdriver
    #from budget.models import Project
    from django.contrib.staticfiles.testing import StaticLiveServerTestCase
    from django.test import LiveServerTestCase
    from django.urls import reverse
    import time

    class TestProjectListPage(StaticLiveServerTestCase):
    #def test_foo(self):
    #  self.assertEquals(0, 1) # this should fail


    #runs before every single test function
    def setUp(self):
        #self.browser = webdriver.Chrome(executable_path='C:/Users/DanXa/Documents/Coding Projects/Executables/chromedriver.exe')
        #create new browser instance which we can use for all other tests
        try:
        self.browser = webdriver.Chrome(executable_path='C:/Users/DanXa/Documents/Coding Projects/Executables/chromedriver.exe')
        except:
        super().tearDown()

    #runs after every single test function
    def tearDown(self):
        #close browser after every single function
        self.browser.close()

    def test_no_projects_alert_is_displayed(self):
        #url for our test to navigate
        #self.live_server_url attribute comes from StaticLiveServerTestCase
        self.browser.get(self.live_server_url)
        
        #user visits page first time
        alert = self.browser.find_element_by_class_name('noproject-wrapper')
        self.assertEquals(
        alert.find_element_by_tag_name('h3').text,
        'Sorry, you don\'t have any projects, yet.'
        )