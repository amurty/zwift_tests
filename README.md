# Selenium tests for testing www.zwift.com

The tests are written using python unittest framework and includes 2 test cases, along with setup and tear down methods.

Test 1: test_validate_main_page_content()
- Load the url zwift.com and validate the page loads
- Validate a content on the page

Test 2: test_events_filter() 
- Load the url zwift.com and navigate to "Events" page. 
- Filter the events based on selected values and validate that the events are updated after the filter.

Dependencies

- Python version: Python 3. Install python on the test machine if not installed
- Python libraries: Tests use various python libraries
- Chrome driver executable: Test assumes that the driver is in the same directory as the python script 
- Browser: chrome 
- Platform: Windows 10


Installing

- Download all the files in the repo to any directory and use the same direcotry path to execute tests
- If not using the chrome driver executable from the repo, download the chromedriver and place the executable in the same directory as the python script
- Install all the libraries added under the import section in the zwift.py on the test machine or virtual environment

Run the tests

- Execute all the tests on command line using the command: "py zwift.py"
