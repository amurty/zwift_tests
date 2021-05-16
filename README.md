# Selenium tests for testing www.zwift.com

The tests are written using python unittest frameowrk and includes 2 test cases, along with setup and tear down methods.

Test 1: 
test_validate_main_page_content(): Loads the url zwift.com and validates the content.

Test 2:
test_events_filter(): Loads the url zwift.com and navigate to "Events" page. Filter the events based on selected values and validate that the events are updated after the filter.

Dependencies

Python version: Python 3. Install python on the test machine if not installed
Python libraries: Install any of the libraries in the python environment if not already installed on the test environment
Chrome driver executable: Test assumes that the driver is in the same directory as the python script 
Browser: chrome 
Platform: Windows 10


Installing

Download the chromedriver and place the executable in the same directory as the python script

Run the tests

Execute all the tests on command line using the command: "py zwift.py"
