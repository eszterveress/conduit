import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def webdriver_wait_xpath(browser, value):
    element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, value)))
    return element

def test_setup():
    browser.get("http://localhost:1667")
    browser.maximize_window()
    time.sleep(1)

def conduit_registration(browser):
    browser.find_element_by_xpath('//a[@href="#/register"]').click()
    webdriver_wait_xpath(browser,'//a[@href="#/register"]')
    username = browser.find_element_by_xpath('//*[@placeholder="Username"]')
    email = browser.find_element_by_xpath('//*[@placeholder="Email"]')
    password = browser.find_element_by_xpath('//*[@placeholder="Password"]')
    test_user_data =["TesztUser1","TesztUser1@gmail.com","Teszt12123"]
    username.send_keys(test_user_data[0])
    email.send_keys(test_user_data[1])
    password.send_keys(test_user_data[2])
    browser.find_element_by_xpath('//button[1]').click()
    webdriver_wait_xpath(browser,'//button[1]')
    browser.find_element_by_xpath('//*[@class="swal-button swal-button--confirm"]').click()
    webdriver_wait_xpath(browser, '//*[@class="swal-button swal-button--confirm"]')


def conduit_logout(browser):
    browser.find_element_by_xpath('//*[@class="nav-link" and contains(text(),"Log out")]').click()
    webdriver_wait_xpath(browser,'//*[@class="nav-link" and contains(text(),"Log out")]')


