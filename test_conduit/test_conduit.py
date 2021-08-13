import time
import csv
from csv import reader
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conduit_data import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options




def setup_env():
    driver_options = Options()
    driver_options.headless = True
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)
    browser.get("http://localhost:1667")
    browser.maximize_window()
    return browser


# Cookie-k elfogadása

def test_cookie():
    browser = setup_env()
    cookie_window = browser.find_element_by_xpath('//div[@class="cookie__bar__content"]')
    assert cookie_window.text == "We use cookies to ensure you get the best experience on our website. Learn More..."
    accept_cookie = browser.find_element_by_xpath('//*[@id="cookie-policy-panel"]/div/div[2]/button[2]')
    accept_cookie.click()
    # button_list = webdriver_wait_xpath(browser, '//button')
    time.sleep(1)
    button_list = browser.find_elements_by_xpath('//button')
    assert len(button_list) == 0
    browser.quit()

# Regisztráció (valid adatokkal)


# def test_registration():
#     browser = setup_env()
#     browser.find_element_by_xpath('//a[@href="#/register"]').click()
#     username = browser.find_element_by_xpath('//*[@placeholder="Username"]')
#     email = browser.find_element_by_xpath('//*[@placeholder="Email"]')
#     password = browser.find_element_by_xpath('//*[@placeholder="Password"]')
#     test_user_data = ["TesztUser14", "TesztUser19@gmail.com", "Teszt12123"]
#     username.send_keys(test_user_data[0])
#     email.send_keys(test_user_data[1])
#     password.send_keys(test_user_data[2])
#     browser.find_element_by_xpath('//button[1]').click()
#     element = webdriver_wait_xpath(browser, '//button[@class="swal-button swal-button--confirm"]')
#     element.click()
#     name_tag = webdriver_wait_xpath(browser, '//*[@id="app"]/nav/div/ul/li[4]/a')

    # name_tag = browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a')
    assert name_tag.text == "TesztUser14"
    browser.quit()

# Kijelentkezés

# def test_logout():
#     browser = setup_env()
#     conduit_registration()
#     browser.refresh()
#     webdriver_wait_xpath(browser, '//*[@class="article-preview"]')
#     text_no_article = browser.find_element_by_xpath('//*[@class="article-preview"]')
#     assert text_no_article.text == "No articles are here... yet."
# #
# # # Bejelentkezés
# #
# def test_login():
#     browser = setup_env()
#     conduit_registration()
#     conduit_logout()
#     browser.find_element_by_xpath('//a[@href="#/login"]').click()
#     email_log = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset[1]/input')
#     email_log.send_keys(user_data[1])
#     pw_log = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset[2]/input')
#     pw_log.send_keys(user_data[2])
#     browser.find_element_by_xpath('//button[1]').click()
#     webdriver_wait_xpath(browser,'//button[1]')
#     name_tag = browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a')
#     # print(name_tag.text)
#     assert name_tag.text == user_data[0]
#     conduit_logout(browser)
#
# # Adatok listázása (az alkalmazásban található tagek listába gyűjtése, majd fájlba írása)
#
# def test_data_list(browser):
#     # conduit_registration(browser)
#     tags = browser.find_elements_by_xpath('//a[@class="tag-pill tag-default"]')
#     tag_list = []
#     for i in tags:
#         tag_list.append(i.text)
#     with open("lista.txt", "w") as tag_lista:
#         for j in tag_list:
#             tag_lista.write(j + "\n")
#     with open("lista.txt", "r") as lista:
#         text_content=lista.read().splitlines()
#     assert tag_list == text_content
#     # conduit_logout(browser)
#
# # Több oldalas lista bejárása (lapozás működésének vizsgálata)
#
# def test_pagination(browser):
#     #     conduit_registration(browser)
#     first_page = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/nav/ul/li[1]/a')
#     second_page = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/nav/ul/li[2]/a')
#     second_page.click()
#     webdriver_wait_xpath(browser,'//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/nav/ul/li[2]/a')
#     active_page = browser.find_element_by_xpath('//*[@class="page-item active"]')
#     assert second_page.text == active_page.text
#     first_page.click()
#     webdriver_wait_xpath(browser,'//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/nav/ul/li[2]/a')
#     print(first_page.text)
#     assert first_page.text == active_page.text
#     # conduit_logout(browser)
#
# # Új adat bevitel (a felhasználó bemutatkozásának kitöltése)
#
# def test_new_data(browser):
#     #conduit_registration(browser)
#     browser.find_element_by_xpath('//a[@href="#/settings"]').click()
#     webdriver_wait_xpath(browser,'//a[@href="#/settings"]')
#     bio_field = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[3]/textarea')
#     bio_field.send_keys("Tesztelni jó!")
#     browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/button').click()
#     webdriver_wait_xpath(browser,'//*[@id="app"]/div/div/div/div/form/fieldset/button')
#     browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/button').click()
#     webdriver_wait_xpath(browser, '/html/body/div[2]/div/div[3]/div/button')
#     browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a').click()
#     webdriver_wait_xpath(browser, '//*[@id="app"]/nav/div/ul/li[4]/a')
#     user_text = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/div/p')
#     assert user_text.text == "Tesztelni jó!"
#     # conduit_logout(browser)
#
# # Ismételt és sorozatos adatbevitel adatforrásból (új cikk létrehozása csv fájl segítségével)
#
# def test_data_from_file(browser):
#     # conduit_registration(browser)
#     article_data = []
#     with open('adatok_cikkhez.csv', 'r', encoding="utf-8") as data_file:
#         table_reader = csv.reader(data_file, delimiter=";")
#         next(table_reader)
#         for row in table_reader:
#             article_data.append(row)
#     browser.find_element_by_xpath('//*[@href="#/editor"]').click()
#     webdriver_wait_xpath(browser,'//*[@href="#/editor"]')
#     article_title = browser.find_element_by_xpath('//*[@placeholder="Article Title"]')
#     article_about = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[2]/input')
#     article_text = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[3]/textarea')
#     article_title.send_keys(article_data[0])
#     article_about.send_keys(article_data[1])
#     article_text.send_keys(article_data[2])
#     browser.find_element_by_xpath('//button[@type="submit"]').click()
#     webdriver_wait_xpath(browser,'//button[@type="submit"]')
#     article_title_page = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/h1')
#     assert article_title_page.text == "Uj bejegyzes"
#     # conduit_logout(browser)
#
#
# # Meglévő adat módosítás (felhasználó nevének módosítása)
#
# def test_data_change(browser):
#     # conduit_registration(browser)
#     browser.find_element_by_xpath('//*[@href="#/settings"]').click()
#     webdriver_wait_xpath(browser,'//*[@href="#/settings"]')
#     name_field = browser.find_element_by_xpath('//*[@placeholder="Your username"]')
#     name_field.clear()
#     name_field.send_keys("tesztella")
#     browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]').click()
#     webdriver_wait_xpath(browser, '//button[@class="btn btn-lg btn-primary pull-xs-right"]')
#     browser.find_element_by_xpath('//*[@class="swal-button swal-button--confirm"]').click()
#     webdriver_wait_xpath(browser,'//*[@class="swal-button swal-button--confirm"]')
#     assert name_tag.text == "tesztella"
#     # conduit_logout(browser)
#
# # Adat vagy adatok törlése
#
# def test_del_data(browser):
#     # conduit_registration(browser)
#     browser.find_element_by_xpath('//*[@href="#/editor"]').click()
#     webdriver_wait_xpath(browser,'//*[@href="#/editor"]')
#     article_title.send_keys(user_data[0])
#     article_about.send_keys(user_data[1])
#     article_text.send_keys(user_data[0])
#     browser.find_element_by_xpath('//button[@type="submit"]').click()
#     webdriver_wait_xpath(browser,'//button[@type="submit"]')
#     browser.find_element_by_xpath('//button[@class="btn btn-outline-danger btn-sm"]').click()
#     webdriver_wait_xpath(browser,'//button[@class="btn btn-outline-danger btn-sm"]')
#     browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a').click()
#     webdriver_wait_xpath(browser, '//*[@id="app"]/nav/div/ul/li[4]/a')
#     article_list = browser.find_elements_by_xpath('//*[@class="preview-link"]')
#     assert len(article_list) == 1
#     # conduit_logout(browser)
#
# # Adatok lementése felületről (conduit címke fájlba mentése)
#
# def test_data_save(browser):
#     # conduit_registration(browser)
#     conduit = browser.find_element_by_xpath('//*[@id="app"]/nav/div/a').text
#     with open("conduit.txt", "w") as file:
#         file.write(conduit)
#     with open("conduit.txt", "r") as file2:
#         result = file2.read()
#     assert result == "conduit"
#     # conduit_logout(browser)
#
