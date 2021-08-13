import csv
from selenium import webdriver
from conduit_data import *
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options




def setup_env():
    driver_options = Options()
    driver_options.headless = True
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=driver_options)
    browser.get("http://localhost:1667")
    browser.maximize_window()
    return browser


# Cookie-k elfogadása:

def test_cookie():
    browser = setup_env()
    cookie_window = browser.find_element_by_xpath('//div[@class="cookie__bar__content"]')
    assert cookie_window.text == "We use cookies to ensure you get the best experience on our website. Learn More..."
    accept_cookie = browser.find_element_by_xpath('//*[@id="cookie-policy-panel"]/div/div[2]/button[2]')
    accept_cookie.click()
    time.sleep(1)
    # Ellenőrizzük, hogy eltűntek a gombok a kezdőlapról
    button_list = browser.find_elements_by_xpath('//button')
    assert len(button_list) == 0
    browser.quit()

# Regisztráció (valid adatokkal)


def test_registration():
    browser = setup_env()
    sign_up = webdriver_wait_xpath(browser, '//a[@href="#/register"]')
    sign_up.click()
    username = webdriver_wait_xpath(browser, '//*[@placeholder="Username"]')
    email = browser.find_element_by_xpath('//*[@placeholder="Email"]')
    password = browser.find_element_by_xpath('//*[@placeholder="Password"]')
    user_data = ["TesztUser111", "TesztUser111@gmail.com", "Teszt12123"]
    username.send_keys(user_data[0])
    email.send_keys(user_data[1])
    password.send_keys(user_data[2])
    browser.find_element_by_xpath('//button[1]').click()
    element = webdriver_wait_xpath(browser, '//button[@class="swal-button swal-button--confirm"]')
    element.click()
    name_tag = webdriver_wait_xpath(browser, '//*[@id="app"]/nav/div/ul/li[4]/a')
    # Ellenőrizzük, hogy a regisztráció végeztével megjelenik a felhasználónév, azaz a felhasználó belépett
    assert name_tag.text == user_data[0]
    conduit_logout(browser)



# Kijelentkezés


def test_logout():
    browser = setup_env()
    conduit_registration(browser)
    logout_button = webdriver_wait_xpath(browser, '//a[contains(text(),"Log out")]')
    logout_button.click()
    browser.refresh()
    text_no_article = webdriver_wait_xpath(browser, '//*[@class="article-preview"]')
    # Ellenőrizzük, hogy kilépés után a kezdőoldalon nem látszanak a bejegyzések
    # (a bejegyzéseket csak a bejelentkezett felhasználó láthatja)
    assert text_no_article.text == "No articles are here... yet."


# # # Bejelentkezés


def test_login():
    browser = setup_env()
    sign_in = webdriver_wait_xpath(browser, '//a[@href="#/login"]')
    sign_in.click()
    user_data = ["TesztUser99", "TesztUser99@gmail.com", "Teszt12123"]
    email_log = webdriver_wait_xpath(browser, '//*[@id="app"]/div/div/div/div/form/fieldset[1]/input')
    email_log.send_keys(user_data[1])
    pw_log = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset[2]/input')
    pw_log.send_keys(user_data[2])
    browser.find_element_by_xpath('//button[1]').click()
    name_tag = webdriver_wait_xpath(browser, '//*[@id="app"]/nav/div/ul/li[4]/a')
    assert name_tag.text == user_data[0]




# # Adatok listázása (az alkalmazásban található tagek listába gyűjtése, majd fájlba írása)


def test_data_list():
    browser = setup_env()
    tags = browser.find_elements_by_xpath('//a[@class="tag-pill tag-default"]')
    tag_list = []
    for i in tags:
        tag_list.append(i.text)
    with open("lista.txt", "w") as tag_lista:
        for j in tag_list:
            tag_lista.write(j + "\n")
    with open("lista.txt", "r") as lista:
        text_content=lista.read().splitlines()
    # Ellenőrizzük, hogy az oldalról kigyűjtött és a fájlba írt tagek megegyeznek
    assert tag_list == text_content



# # Több oldalas lista bejárása (lapozás működésének vizsgálata)


def test_pagination():
    browser = setup_env()
    conduit_registration(browser)
    second_page = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/nav/ul/li[2]/a')
    second_page.click()
    # Ellenőrizzük, hogy a 2. oldalra kattintás után az az oldal válik-e aktívvá
    active_page = webdriver_wait_xpath(browser, '//*[@class="page-item active"]')
    assert second_page.text == active_page.text

# # Új adat bevitel (új bejegyzés létrehozása csak címmel)


def test_new_data():
    browser = setup_env()
    conduit_registration(browser)
    settings = browser.find_element_by_xpath('//a[@href="#/editor"]')
    settings.click()
    article_title = webdriver_wait_xpath(browser, '//*[@placeholder="Article Title"]')
    article_title.send_keys("Tesztelni jó!")
    update_button = browser.find_element_by_xpath('//button[@class="btn btn-lg pull-xs-right btn-primary"]')
    update_button.click()
    article_title_text = webdriver_wait_xpath(browser, '//*[@id="app"]/div/div[1]/div/h1')
    assert article_title_text.text == "Tesztelni jó!"


# # Ismételt és sorozatos adatbevitel adatforrásból (új cikk létrehozása csv fájl segítségével)


def test_data_from_file():
    browser = setup_env()
    article_data = []
    with open('adatok_cikkhez.csv', 'r', encoding="utf-8") as data_file:
        table_reader = csv.reader(data_file, delimiter=";")
        next(table_reader)
        for row in table_reader:
            article_data.append(row)
    new_article = webdriver_wait_xpath(browser, '//*[@href="#/editor"]')
    new_article.click()
    article_title = webdriver_wait_xpath(browser, '//*[@placeholder="Article Title"]')
    article_about = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[2]/input')
    article_text = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[3]/textarea')
    article_title.send_keys(article_data[0])
    article_about.send_keys(article_data[1])
    article_text.send_keys(article_data[2])
    submit_button = webdriver_wait_xpath(browser, '//button[@type="submit"]')
    submit_button.click()
    article_title_page = webdriver_wait_xpath(browser, '//*[@id="app"]/div/div[1]/div/h1')
    # Ellenőrizzük, hogy a cikk valóban létrejött a megadott címmel
    assert article_title_page.text == "Uj bejegyzes"


# # Meglévő adat módosítás (felhasználó nevének módosítása)


def test_data_change():
    browser = setup_env()
    settings = webdriver_wait_xpath(browser, '//*[@href="#/settings"]')
    settings.click()
    name_field = webdriver_wait_xpath(browser, '//*[@placeholder="Your username"]')
    name_field.clear()
    name_field.send_keys("tesztella")
    browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]').click()
    ok_button = webdriver_wait_xpath(browser, '//*[@class="swal-button swal-button--confirm"]')
    ok_button.click()
    name_tag = webdriver_wait_xpath(browser, '//*[@id="app"]/nav/div/ul/li[4]/a')
    assert name_tag.text == "tesztella"


# # Adat vagy adatok törlése (létrehozott új bejegyzés törlése)


def test_del_data():
    browser = setup_env()
    new_article = webdriver_wait_xpath(browser, '//*[@href="#/editor"]')
    new_article.click()
    user_data = ["TesztUser20", "TesztUser56@gmail.com", "Teszt1217879"]
    article_title = webdriver_wait_xpath(browser, '//*[@placeholder="Article Title"]')
    article_about = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[2]/input')
    article_text = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[3]/textarea')
    article_title.send_keys(user_data[0])
    article_about.send_keys(user_data[1])
    article_text.send_keys(user_data[2])
    submit_button = webdriver_wait_xpath(browser, '//button[@type="submit"]')
    submit_button.click()
    delete_button = webdriver_wait_xpath(browser, '//button[@class="btn btn-outline-danger btn-sm"]')
    delete_button.click()
    name_tag = webdriver_wait_xpath(browser, '//*[@id="app"]/nav/div/ul/li[4]/a')
    name_tag.click()
    article_list = browser.find_elements_by_xpath('//*[@class="author router-link-exact-active router-link-active"]')
    assert len(article_list) == 0

# # Adatok lementése felületről (conduit címke fájlba mentése)


def test_data_save():
    browser = setup_env()
    conduit = webdriver_wait_xpath(browser, '//*[@id="app"]/nav/div/a')
    with open("conduit.txt", "w") as file:
        file.write(conduit.text)
    with open("conduit.txt", "r") as file2:
        result = file2.read()
    assert result == "conduit"
    conduit_logout(browser)

