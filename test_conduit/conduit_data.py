import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_env():
    driver_options = Options()
    driver_options.headless = True
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)
    browser.get("http://localhost:1667")
    browser.maximize_window()
    return browser


def webdriver_wait_xpath(browser, value):
    element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, value)))
    return element

def conduit_registration(browser):
    browser.find_element_by_xpath('//a[@href="#/register"]').click()
    webdriver_wait_xpath(browser, '//a[@href="#/register"]')
    username = browser.find_element_by_xpath('//*[@placeholder="Username"]')
    email = browser.find_element_by_xpath('//*[@placeholder="Email"]')
    password = browser.find_element_by_xpath('//*[@placeholder="Password"]')
    test_user_data =["TesztUser14", "TesztUser14@gmail.com","Teszt12123"]
    username.send_keys(test_user_data[0])
    email.send_keys(test_user_data[1])
    password.send_keys(test_user_data[2])
    browser.find_element_by_xpath('//button[1]').click()
    webdriver_wait_xpath(browser, '//*[@class="swal-button swal-button--confirm"]')
    browser.find_element_by_xpath('//*[@class="swal-button swal-button--confirm"]').click()



def conduit_logout():
    browser = setup_env()
    browser.find_element_by_xpath('//*[@class="nav-link" and contains(text(),"Log out")]').click()



