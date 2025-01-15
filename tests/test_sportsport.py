import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from pages.home_page import HomePage

@pytest.fixture
def driver():
    # Setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()


def test_homepage_title(driver):
    home_page = HomePage(driver)
    home_page.open()
    assert "SportSport.ba - Duplo više informacija! Duplo više sporta!" in driver.title, "Page title does not match."


def test_search_functionality(driver):
    home_page = HomePage(driver)
    home_page.open()

    home_page.search_for("Real")
    WebDriverWait(driver, 5)

    assert home_page.is_item_list_displayed(), "No products found for 'Real'."


def test_empty_search(driver):
    home_page = HomePage(driver)
    home_page.open()

    home_page.search_for("")
    WebDriverWait(driver, 5)

    assert not home_page.is_item_list_displayed(), "Products displayed for an empty search."


def test_search_functionality_results(driver):
    home_page = HomePage(driver)
    home_page.open()

    home_page.search_for("Football")

    WebDriverWait(driver, 5)
    results = driver.find_elements(By.TAG_NAME, "article")
    assert len(results) > 0, "No search results found for 'Football'."


def test_article_home_page_links(driver):
    home_page = HomePage(driver)
    home_page.open()

    articles = driver.find_elements(By.CSS_SELECTOR, "article")
    assert len(articles) > 0, "No articles found."

    for i in range(min(3, len(articles))):
        articles = driver.find_elements(By.CSS_SELECTOR, "article")
        
        article = articles[i]
        article.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.main"))
        )
        
        driver.back()

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article"))
        )


def test_fudbal_section_first_article(driver):
    home_page = HomePage(driver)
    home_page.open()

    fudbal_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-tb-region="Fudbal"]'))
    )
    
    articles = fudbal_section.find_elements(By.CSS_SELECTOR, "article")
    assert len(articles) > 0, "No articles found in the Fudbal section."

    articles[0].click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.main"))
    )
    

def test_article_title(driver):
    home_page = HomePage(driver)
    home_page.open()

    articles = driver.find_elements(By.CSS_SELECTOR, "article")
    assert len(articles) > 0, "No articles found in the Fudbal section."

    articles[0].click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.main"))
    )
    
    article_title = driver.find_element(By.CSS_SELECTOR, "h1").text
    assert article_title, "Article title is missing."


def test_navigation_to_contact_page(driver):
    home_page = HomePage(driver)
    home_page.open()

    contact_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "KONTAKT"))
    )
    contact_link.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.main"))
    )

    assert "Kontakt - SportSport.ba" in driver.title, "Failed to navigate to the Contact page."


def test_menu_open_and_close(driver):
    home_page = HomePage(driver)
    home_page.open()

    hamburger_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "hamburger-btn-open"))
    )
    hamburger_button.click()

    menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".dropMenu"))
    )
    assert menu.is_displayed(), "Menu did not open."

    close_button = driver.find_element(By.CSS_SELECTOR, "#hamburger-btn-closed")
    close_button.click()

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element(menu)
    )
    assert not menu.is_displayed(), "Menu did not close."


def test_menu_open_close_and_click_first_item(driver):
    home_page = HomePage(driver)
    home_page.open()

    hamburger_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "hamburger-btn-open"))
    )
    hamburger_button.click()

    menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "nav.dropMenu"))
    )
    assert menu.is_displayed(), "Menu did not open."

    first_menu_item = menu.find_element(By.LINK_TEXT, "RUKOMET")
    first_menu_item.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.main"))
    )

    driver.back()

    hamburger_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "hamburger-btn-open"))
    )
    hamburger_button.click()

    menu = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "nav.dropMenu"))
    )
    assert menu.is_displayed(), "Menu did not open."

    first_menu_item = menu.find_element(By.LINK_TEXT, "MAGAZIN")
    first_menu_item.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.main"))
    )

    articles = driver.find_elements(By.CSS_SELECTOR, "article")
    assert len(articles) > 0, "No articles found in the magazin section."

    articles[0].click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.main"))
    )
    
    article_title = driver.find_element(By.CSS_SELECTOR, "h1").text
    assert article_title, "Article title is missing."

