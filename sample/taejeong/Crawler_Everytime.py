from selenium import webdriver
from bs4 import BeautifulSoup
import requests

import xmltodict
import json
from io import StringIO

import pprint

# Constants
ES_ADDRESS = "http://localhost:9200"
HOW_MANY_PAGE = 30
HOW_MANY_BOARD = 0


def coding(text):
    return text.encode("UTF-8", errors="ignore").decode("UTF-8")


def get_text(obj):
    import bs4
    if type(obj) == bs4.element.Tag:
        return obj.getText()
    elif type(obj) == str:
        return obj
    return ""


def first_in_list(arr):
    if len(arr):
        return arr[0]
    return ""


def put_article_data(data):
    headers = {}
    headers["content-type"] = "application/json"
    headers["charset"] = "UTF-8"
    piece = data["link"].split("/")
    path = "/site/everytime/" + piece[-3] + "." + piece[-1]
    r = requests.put("http://localhost:9200" + path,
                     data=json.dumps(data), headers=headers)

    if r.status_code in range(200, 300):
        print(r)
    else:
        pp = pprint.PrettyPrinter()
        req_info = json.load(StringIO(r.text))["error"]["root_cause"][0]
        print(req_info["type"] + " : " + req_info["reason"] + "\n\n")
        pp.pprint(data)
        print(json.dumps(data))
        return True
    return False


def get_article_data(driver, src):

    article_data = {}

    # load article
    driver.get(src)
    while True:
        if len(driver.find_elements_by_css_selector("div.profile h3")):
            break

    # get page source
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # get title
    article_data["title"] = coding(get_text(first_in_list(soup.select("a.article > h2"))))

    # get username
    article_data["username"] = coding(get_text(first_in_list(soup.select("div.profile h3"))))

    # get timestamp
    article_data["timestamp"] = first_in_list(
        soup.select("div.profile time")).attrs["title"]

    # get body
    body = ""
    for line in soup.select("div.wrap.articles > article > a > p"):
        body += line.text + "\n"
    article_data["body"] = coding(body[:-1])

    images = []  # [ SRC, ... ]
    for image in soup.select("div.wrap.articles > article figure.attach > img"):
        images.append(image.attrs["src"])
    article_data["images"] = images

    # get comments
    article_data["comments"] = []
    for comment_element in soup.select(".comments > article"):

        # crawl
        child = "child" in comment_element.attrs["class"]
        writer = coding(first_in_list(
            comment_element.select("h3")).text)
        time = first_in_list(comment_element.select("time")).attrs["title"]
        body = ""
        for line in comment_element.select('p'):
            body += line.text + "\n"
        body = coding(body[:-1])

        # store
        article_data["comments"].append([child, writer, time, body])

    article_data["link"] = src

    return article_data


def collect_data(driver, src, board):
    current_page = 1
    while True:
        # load page
        driver.get(src + "/p/" + str(current_page))
        while True:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            if len(driver.find_elements_by_css_selector("div.wrap.articles article a.article")):
                break
            if get_text(first_in_list(soup.select(".dialog"))) == "더 이상 글이 없습니다.":
                print("No more pages")
                return

        # get article links in page
        article_links = []
        for article_element in driver.find_elements_by_css_selector(".wrap.articles article a.article"):
            article_links.append(article_element.get_attribute("href"))

        # main task
        for article_link in article_links:
            article_data = get_article_data(driver, article_link)
            article_data["board"] = board
            PUT_ERROR = put_article_data(article_data)

        # add page number
        current_page += 1

        if current_page > HOW_MANY_PAGE and HOW_MANY_PAGE or PUT_ERROR:
            break


def Crawling():

    # Driver
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    # options.add_argument('headless')
    driver = webdriver.Chrome("chromedriver", chrome_options=options)

    # Login
    userId = input("ID : ")
    password = input("PW : ")
    driver.get("https://everytime.kr/login")
    driver.find_element_by_xpath("//input[@type='text']").send_keys(userId)
    driver.find_element_by_xpath(
        "//input[@type='password']").send_keys(password)
    driver.find_element_by_xpath("//input[@type='submit']").click()

    # Collect Boards
    board_count = 1
    cookies = driver.get_cookies()
    s = requests.Session()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    r = s.get("https://everytime.kr/find/board/list/")
    xml_data = xmltodict.parse(r.text)
    boards = {}
    for board in xml_data['response']['quick']['board'] + xml_data['response']['noquick']['board']:
        boards[board["@name"]] = board["@id"]

    # Collect Articles
    for board_name in boards.keys():
        collect_data(driver, "https://everytime.kr/" +
                     boards[board_name], board_name)
        board_count += 1
        if board_count > HOW_MANY_BOARD and HOW_MANY_BOARD:
            break

    # Close
    driver.close()
    driver.quit()


Crawling()
