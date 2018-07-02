from selenium import webdriver
from bs4 import BeautifulSoup
import requests

def Crawling():

    # Driver
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    #options.add_argument('headless')
    driver = webdriver.Chrome("chromedriver", chrome_options = options)

    # Login
    userId = input("ID : ")
    password = input("PW : ")
    driver.get("https://everytime.kr/login")
    driver.find_element_by_xpath("//input[@type='text']").send_keys(userId)
    driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
    driver.find_element_by_xpath("//input[@type='submit']").click()
    
    # Collect Boards
    boards = [] # [ [ TITLE, LINK ], ... ]
    driver.get("https://everytime.kr")
    docs = driver.page_source
    soup = BeautifulSoup(docs, "html.parser")
    for board in soup.select("#submenu a"):
        if board.attrs.get("class") in [["more"], ["search"]]:
            continue
        boards.append([board.text, "https://everytime.kr" + board.attrs["href"]])

    # Collect Articles
    articles = [] # [ [ BOARD, TITLE, WRITER, TIME, BODY, IMGS, REPLIES ], ... ]
    for board in boards:
        
        driver.get(board[1])

        # Loading
        import time
        t = time.clock()
        while True:
            if len(driver.find_elements_by_css_selector("div.wrap.articles article a.article")) > 19 or\
               time.clock() - t > 1:
                break

        # Parsing
        docs = driver.page_source
        soup = BeautifulSoup(docs, "html.parser")
        for article in soup.select("div.wrap.articles article a.article"):
            driver.get("https://everytime.kr" + article.attrs["href"])

            while True:
                if len(driver.find_elements_by_css_selector("div.profile h3")) > 0:
                    break
            
            docs = driver.page_source
            soup = BeautifulSoup(docs, "html.parser")

            BOARD   = board[0].encode("euc-kr", errors='ignore').decode("euc-kr")
            
            TITLE   = ""
            for title in soup.select("a.article > h2"  ):
                TITLE = title.text.encode("euc-kr", errors='ignore').decode("euc-kr")

            WRITER  = soup.select("div.profile h3"  )[0].text.encode("euc-kr", errors='ignore').decode("euc-kr")

            TIME    = soup.select("div.profile time")[0].attrs["title"]
            
            BODY    = ""
            for line  in soup.select("div.wrap.articles > article > a > p"):
                BODY += line.text + "\n"
            BODY = BODY[:-1].encode("euc-kr", errors='ignore').decode("euc-kr")
                
            IMGS    = [] # [ SRC, ... ]
            for img   in soup.select("div.wrap.articles > article figure.attach > img"):
                IMGS.append(img.attrs["src"])
                
            REPLIES = [] # [ [ WRITER, TIME, BODY ], ... ]
            for reply in soup.select("div.comments > article"):
                child = ("child" in reply.attrs["class"])
                soup = BeautifulSoup(str(reply), "html.parser")
                writer = soup.select("h3")[0].text.encode("euc-kr", errors='ignore').decode("euc-kr")
                time   = soup.select("time")[0].attrs["title"]
                body   = ""
                for line in soup.select('p'):
                    body += line.text + "\n"
                body = body[:-1].encode("euc-kr", errors='ignore').decode("euc-kr")
                REPLIES.append([child, writer, time, body])

            articles.append([BOARD, TITLE, WRITER, TIME, BODY, IMGS, REPLIES])

    # Close
    driver.close()
    driver.quit()

    # Print
    for article in articles:
        print("[BOARD  ] "+article[0])
        print("[TITLE  ] "+article[1])
        print("[WRITER ] "+article[2])
        print("[TIME   ] "+article[3])
        print("[BODY   ] "+article[4])
        for img   in article[5]:
            print("[IMAGE  ] "+img)
        print("[REPLIES]")
        for reply in article[6]:
            if reply[0]:
                print("└", end = '')
            print("[" + reply[1] + "] " + reply[3])
        print()
    
Crawling()
