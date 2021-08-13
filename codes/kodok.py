from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import names

PATH = "D:\\programok\\selenium\\chromedriver.exe"
browser = webdriver.Chrome(PATH)
browser.get("http://localhost:1667")
browser.maximize_window()

try:

    # Cookie-k elfogadása

    cookie_window = browser.find_element_by_xpath("//div[@class='cookie__bar__content']")
    # print(cookie_window.text)
    assert cookie_window.text == "We use cookies to ensure you get the best experience on our website. Learn More..."
    accept_cookie = browser.find_element_by_xpath("//*[@id='cookie-policy-panel']/div/div[2]/button[2]")
    accept_cookie.click()

    # Regisztráció

    browser.find_element_by_xpath("//a[@href='#/register']").click()
    time.sleep(2)
    username = browser.find_element_by_xpath("//*[@placeholder='Username']")
    email = browser.find_element_by_xpath("//*[@placeholder='Email']")
    password = browser.find_element_by_xpath("//*[@placeholder='Password']")
    rand_name = names.get_first_name()
    rand_email = rand_name + "@gmail.com"
    pw = "Teszt12123"
    # print(rand_name)
    # print(rand_email)
    user_data = []
    user_data.append(rand_name)
    user_data.append(rand_email)
    user_data.append(pw)
    # print(user_data)
    username.send_keys(user_data[0])
    email.send_keys(user_data[1])
    password.send_keys(user_data[2])
    browser.find_element_by_xpath("//button[1]").click()
    time.sleep(2)
    success_log = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".swal-text")))
    # print(success_log.text)
    assert success_log.text == "Your registration was successful!"
    browser.find_element_by_xpath("//*[@class='swal-button swal-button--confirm']").click()
    time.sleep(2)

    # Kijelentkezés

    browser.find_element_by_xpath('//*[@class="nav-link" and contains(text(),"Log out")]').click()
    time.sleep(1)
    browser.refresh()
    time.sleep(2)
    text_no_article = browser.find_element_by_xpath('//*[@class="article-preview"]')
    # print(text_no_article.text)
    assert text_no_article.text == "No articles are here... yet."

    # Bejelentkezés

    browser.find_element_by_xpath('//a[@href="#/login"]').click()
    email_log = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset[1]/input')
    email_log.send_keys(user_data[1])
    pw_log = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset[2]/input')
    pw_log.send_keys(user_data[2])
    browser.find_element_by_xpath("//button[1]").click()
    time.sleep(2)
    name_tag = browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a')
    # print(name_tag.text)
    assert name_tag.text == user_data[0]

    # Adatok listázása (az alkalmazásban található tagek listába gyűjtése, majd fájlba írása)

    tags = browser.find_elements_by_xpath('//a[@class="tag-pill tag-default"]')
    tag_list = []
    for i in tags:
        tag_list.append(i.text)
    # print(tag_list)
    with open("lista.txt", "w") as tag_lista:
        for j in tag_list:
            tag_lista.write(j + "\n")
    with open("lista.txt", "r") as lista:
        text_content=lista.read().splitlines()
    # print(tag_list)
    # print(text_content)
    assert tag_list == text_content

    # Több oldalas lista bejárása (lapozás működésének vizsgálata)

    first_page = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/nav/ul/li[1]/a')
    second_page = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/nav/ul/li[2]/a')
    second_page.click()
    time.sleep(2)
    active_page = browser.find_element_by_xpath('//*[@class="page-item active"]')
    # print(second_page.text)
    # print(active_page.text)
    assert second_page.text == active_page.text

    # Új adat bevitel

    browser.find_element_by_xpath('//a[@href="#/settings"]').click()
    time.sleep(3)
    bio_field = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[3]/textarea')
    bio_field.send_keys("Tesztelni jó!")
    browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/button').click()
    time.sleep(2)
    browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/button').click()
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a').click()
    time.sleep(2)
    user_text = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/div/div/p')
    # print(user_text.text)
    assert user_text.text == "Tesztelni jó!"

    # Ismételt és sorozatos adatbevitel adatforrásból (új cikk létrehozása csv fájl segítségével

    article_data = []
    with open('adatok_cikkhez.csv', 'r', encoding="utf-8") as data_file:
        table_reader = csv.reader(data_file, delimiter=";")
        next(table_reader)
        for row in table_reader:
            article_data.append(row)
    # print(article_data)
    browser.find_element_by_xpath('//*[@href="#/editor"]').click()
    time.sleep(3)
    article_title = browser.find_element_by_xpath('//*[@placeholder="Article Title"]')
    article_about = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[2]/input')
    article_text = browser.find_element_by_xpath('//*[@id="app"]/div/div/div/div/form/fieldset/fieldset[3]/textarea')
    article_title.send_keys(article_data[0])
    article_about.send_keys(article_data[1])
    article_text.send_keys(article_data[2])
    time.sleep(2)
    browser.find_element_by_xpath('//button[@type="submit"]').click()
    time.sleep(2)
    article_title_page = browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/h1')
    # print(article_title_page.text)
    assert article_title_page.text == "Uj bejegyzes"
    time.sleep(2)

    # Meglévő adat módosítás (felhasználó nevének módosítása)
    browser.find_element_by_xpath('//*[@href="#/settings"]').click()
    time.sleep(2)
    name_field = browser.find_element_by_xpath('//*[@placeholder="Your username"]')
    name_field.clear()
    name_field.send_keys("tesztella")
    browser.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]').click()
    time.sleep(2)
    browser.find_element_by_xpath("//*[@class='swal-button swal-button--confirm']").click()
    # print(name_tag.text)
    assert name_tag.text == "tesztella"

    # Adat vagy adatok törlése
    browser.find_element_by_xpath('//*[@href="#/editor"]').click()
    time.sleep(3)
    article_title.send_keys(user_data[0])
    article_about.send_keys(user_data[1])
    article_text.send_keys(user_data[0])
    time.sleep(2)
    browser.find_element_by_xpath('//button[@type="submit"]').click()
    time.sleep(2)
    browser.find_element_by_xpath('//button[@class="btn btn-outline-danger btn-sm"]').click()
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="app"]/nav/div/ul/li[4]/a').click()
    time.sleep(2)
    article_list = browser.find_elements_by_xpath('//*[@class="preview-link"]')
    # print(len(article_list))
    assert len(article_list) == 1

    #    Adatok lementése felületről
    conduit = browser.find_element_by_xpath('//*[@id="app"]/nav/div/a').text
    with open("conduit.txt", "w") as file:
        file.write(conduit)
    with open("conduit.txt", "r") as file2:
        result = file2.read()
    # print(result)
    assert result == "conduit"
    browser.find_element_by_xpath('//*[@class="nav-link" and contains(text(),"Log out")]').click()
    time.sleep(5)


finally:
    browser.close()
