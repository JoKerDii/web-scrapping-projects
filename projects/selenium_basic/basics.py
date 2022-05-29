from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument("--headless")

options = webdriver.ChromeOptions()
s = Service('./chromedriver')
driver = webdriver.Chrome(service=s, options=options)
driver.get("https://duckduckgo.com")

# search_input = driver.find_element_by_id("search_form_input_homepage")
search_input = driver.find_element_by_xpath("(//input[contains(@class,'js-search-input')])[1]")
search_input.send_keys("my user agent")

search_btn = driver.find_element_by_id("search_button_homepage")
search_btn.click()
# driver.find_element_by_class_name()
# driver.find_elements_by_tag_name("h1")
# driver.find_elements_by_xpath()
# driver.find_elements_by_css_selector()

search_input.send_keys(Keys.ENTER)

print(driver.page_source)