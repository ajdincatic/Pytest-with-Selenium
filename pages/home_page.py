from selenium.webdriver.common.by import By

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.search_input = (By.ID, "search-input")
        self.search_button = (By.CSS_SELECTOR, "header #search button")
        self.articles_list = (By.CSS_SELECTOR, ".main article")

    def open(self, url="https://sportsport.ba/"):
        self.driver.get(url)

    def search_for(self, product_name):
        self.driver.find_element(*self.search_input).send_keys(product_name)
        self.driver.find_element(*self.search_button).click()

    def is_item_list_displayed(self):
        return len(self.driver.find_elements(*self.articles_list)) > 0
