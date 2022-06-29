#Using python unittest frameowork. This can be done using pytest too.

import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
import sys
import datetime
import re


class ZwiftTests(unittest.TestCase):
    def setUp(self):    

        #Initialize the webdriver. Assume that the driver is in the same directory as the python script
        self.driver = webdriver.Chrome('./chromedriver')


    def tearDown(self):
        print("Test teardown steps")
        self.driver.close()


    def test_validate_main_page_content(self):
        print("Test steps below")

        title_input = 'The at Home Cycling & Running Virtual Training App - Zwift'

        self.driver.implicitly_wait(10)

        #Use driver.get() method in Selenium for opening the URL
        self.driver.get("https://www.zwift.com")
        self.driver.implicitly_wait(5)
        start_url = self.driver.current_url
        #driver.maximize_window() method is used for maximizing the browser window
        self.driver. maximize_window()
        #Reject cookies for this test purpose
        self.driver.find_element_by_xpath('//button[@id="truste-consent-required"]').click()

        #check/wait for the element to be visible to confirm page as loaded
        main_page = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='_2gGSD57urY4DjTUQdMs_wn']")))
        #print("The main page text:", main_page.get_attribute('textContent'))
        self.assertEqual(main_page.get_attribute('textContent'),'Seriously fun indoor training')

        #The driver.title() method is used for retrieving the title of the web page under test. 
        #Assert is raised if the expected title does not match the title of the web page displayed in the browser window
        self.assertEqual(self.driver.title,title_input)

        #Check for the element "Try free for 7 days" on main page
        main_page_free_trial = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//a[@class="VOvJR9SLGKCL0Zu0nWsv5 _2XbVlxIRp_9PeK8wIB4uA8 _2hqlEaYeILaEn267p00soR"]')))
        #print("Timeout happened, element Try free for 7 days did not load")
        self.assertEqual(main_page_free_trial.text, "TRY FREE FOR 7 DAYS")

        #Check for the "Get started" link
        get_started_ele = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//span[@class="_1pK23joOsN6Ime4V0nDK6a" and text()="Get Started"]')))
        self.assertEqual(get_started_ele.text, "GET STARTED")

        sign_in_ele = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//span[@class="_2TTnY4YQX0BYPA64IEp4tW" and text()="Sign In"]')))
        self.assertEqual(sign_in_ele.text, "Sign In")

        #Validating the content "Try free for 7 days" that loads the page with "Create an Account" 
        main_page_free_trial.click()
        search_string = self.driver.find_element_by_xpath('//span[@class="_2SFhg8KjB9xA-TBS6KNtil" and text()="Create an Account"]')
        #print("The create account element text is:", search_string.text)
        create_account_form = self.driver.find_element_by_xpath('//form')
        #print("The form element text is:", create_account_form.text)
        #Assert if the page doesn't show create an account elemment. 
        self.assertEqual(search_string.get_attribute('textContent'), "Create an Account")
        current_url = self.driver.current_url
        #Assert if the main page url is same as the current url
        self.assertNotEqual(start_url, current_url)

        #Below is additional test with with some basic form fill without any validations and no assertions
        #fill/submit sign up form with some temp values. Post request could be used to validate the data entered 
        self.driver.find_element_by_xpath('//input[@id="firstName-input"]').send_keys("Testfirst")
        self.driver.find_element_by_xpath('//input[@id="lastName-input"]').send_keys("Testlast")
        self.driver.find_element_by_xpath('//input[@id="email-input"]').send_keys("ashwinigouder@gmail.com")
        self.driver.find_element_by_xpath('//input[@id="password-input"]').send_keys("testing123!")
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="ageCheck-input"]'))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="terms-input"]'))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@id="newsletter-input"]'))).click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="VOvJR9SLGKCL0Zu0nWsv5 _2XbVlxIRp_9PeK8wIB4uA8"]'))).click()



    def test_events_filter(self):

        #Parametrized tests can be used to pass 2 sets of values to same test.For this test, a set of values for filter input are commented out
        #Below are set of filter values for testing no events result or "No results" display
        #updated_event_sport = "RUNNING"
        #updated_event_time = "evening"
        #updated_event_intensity = "1"

        #Below are set of filter values for testing multiple events result 
        updated_event_sport = "CYCLING"
        updated_event_time = "morning"
        updated_event_intensity = "1"

        #Assume the default number of events for morning time are 200
        expected_default_events_count = 200

        #Since there is no info on the input data or events, only checking the Am/PM strings to verify the filter output
        time_string = ""
        if updated_event_time == "morning":
            time_string = "AM"
        else:
            time_string = "PM"


        """
        #Below block of code is commented as there is no information on the event cut off times. The code would work if the cut off times for 
        #morning events is 11:40 am
        #Get the date time format for current day and next day to check the data on events header
        now = datetime.datetime.now()
        tom = datetime.datetime.today() + datetime.timedelta(days=1)
        events_day = ""
        print("Formatted datetime as per matching the header", now.strftime('%A, %B %dth'))
        print("Formatted datetime as per matching the header", tom.strftime('%A, %B %dth'))
        #Without additional data, assuming that the cut off times for the morning eventson current day is 11:40. 
        #If the events cut off times to show all the next morning events changes then the below check would change.
        if int(now.strftime('%H')) < 12 and int(now.strftime('%M')) < 40:
            events_day = now.strftime('%A, %B %dth')
        else:
            events_day = tom.strftime('%A, %B %dth')
        """

        #Use driver.get() method in Selenium for opening the URL
        self.driver.get("https://www.zwift.com")

        #driver.maximize_window() method is used for maximizing the browser window
        self.driver. maximize_window()

        self.driver.implicitly_wait(10)

         #Reject cookies for this test purpose
        self.driver.find_element_by_xpath('//button[@id="truste-consent-required"]').click()

        #Find the navigation button to navigate to "Events" page
        nav_button = self.driver.find_element_by_xpath('//button[@type="button" and @class="_1y_LNCV6bN8pLbpzSLHKCd" and @aria-label="Open side navigation"]').click()

        #Find the "Events" element and click
        events_link = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//span[@class="_2TTnY4YQX0BYPA64IEp4tW" and text()="Events"]'))).click()
        #events_link.click()

        #Check for visibility of the Events element to validate page load
        event_ele = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//h1[text()="EVENTS"]')))
        self.assertEqual(event_ele.text, "EVENTS", "Events page is loaded and shows the element")

        #Find all the default events on the events page
        default_events = self.driver.find_elements_by_xpath('//div[@class="tab-listing"]')
        print("The total number of events with default filters are: ", len(default_events))
        #Assuming we know the total number of events, assert if the events count not matching the expected count
        self.assertEqual(len(default_events), expected_default_events_count, "All events are not displayed")

        #Below steps show applying filters to sports, start time and intensity fields
        #Find and click the filter event button
        filter_button = self.driver.find_element_by_xpath('//button[@class="filter-toggle" and text()="Filter events"]').click()

        #Find and click the sports button. create xpath if you need to pass variable string to xpath
        xpath_sports = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//button[@class="buttons" and @value= "{}"]'.format(updated_event_sport))))
        xpath_sports.click()

        #Find and click the Internsity button for value "A"
        xpath_intensity = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//button[@class="buttons" and @value= "{}"]'.format(updated_event_intensity))))
        xpath_intensity.click()

        #Find and click the "start time" button for value "Morning"
        xpath_time = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//button[@class="buttons" and @value= "{}"]'.format(updated_event_time))))
        xpath_time.click()

        #Use the below commands to wait for element to be clickable and as in case another element obscures the "Apply Filters" button use execute_script() method as below
        self.driver.execute_script("arguments[0].click();", WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="apply-button"]'))))
        
        event_details = self.driver.find_element_by_xpath('//column[@cols="100" and @style="margin-top: 30px;" and text()]')

        #Find all the events that match the filter
        events = self.driver.find_elements_by_xpath('//div[contains(@class,"tab-listing")]')

        #events = self.driver.find_elements_by_xpath('//div[@class="tab-listing"]')
        print("After applying filters, the total number of records are: ", len(events))

        """
        #Below assert is to check the events header returns correct day and month string in format- "Day month date".
        #commenting the below assert as data on events cut off times not provided. The check will work if the last cut off for morning events is 11:40 am
        event_header_filter = self.driver.find_element_by_xpath('//div[@class="tab-header"]')
        #print("After applying filter, the event header day/time: ", event_header_filter.text)
        self.assertEqual(event_header_filter.text, events_day.upper(), "The events from the filter shows incorrect header")
        """

        #Below code verifies the event filter output for sport, intensity and time and asserts if the output doesn't match the filter 
        #Assume that filter should return "No results" if no events matching the filter
        #Assume that there is an issue with filter if the filter does not return any record or string and assert
        if len(events) == 1 and "No results" in event_details.text :      # filter returns no events
            print("Events matching the filter are:", event_details.text)
            self.assertIn("No results", event_details.text, "There are no events for the selected filters")
        elif len(events) == 0 and len(default_events) > 0:          # filter failed and does not return anything
            self.assertFalse(True, "There is some issue with the events filter ")
        else:                                                        # filter returns multiple events
            #Loop through the events and verify if the updated events show up as per the filter
            for temp in events:                 
                #print("\nThe event details are:", temp.text)
                sports = temp.find_element_by_class_name("map-sport-type")
                print("\nSports after filter:", sports.text)
                #Assert if the elected sport filter is not matching the filtered events output
                self.assertEqual( sports.text, updated_event_sport, "The events from the filter shows incorrect sports")

                intensity = temp.find_element_by_class_name("group-label")
                print("Intensity after filter:", intensity.get_attribute('data-label'))
                #Assert if the selected intensity is not matching the filtered events output
                self.assertEqual( intensity.get_attribute('data-label'), updated_event_intensity, "The intensity from the filter shows incorrect value")
                
                start_time = temp.find_element_by_class_name("listing-header")
                #Use the regex to get the event time
                time_after_filter = re.search(r'^(\d{1,2}:\d{1,2}?AM|PM)\s.*',start_time.text)
                print("Start time after filter:", time_after_filter.group(1))
                #Use a regex to search for the "AM|PM" string in the event start times to verify the filter returned correct values/times
                am_pm_string = re.search(r'([A-Z]+)',time_after_filter.group(1))
                print("The time string on the filtered events is:", am_pm_string.group(1))
                #Assert if the selected time is not matching the filtered events output
                self.assertEqual(am_pm_string.group(1), time_string, "The events from the filter shows incorrect event times")



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ZwiftTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

