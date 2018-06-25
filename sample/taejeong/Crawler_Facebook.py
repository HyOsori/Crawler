from selenium import webdriver
from bs4 import BeautifulSoup


def Crawling():

    # Driver
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    #options.add_argument('headless')
    driver = webdriver.Chrome("chromedriver", chrome_options = options)
    driver.get("https://www.facebook.com/hyubamboo/posts/")

    # Load
    articles = []
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        articles = driver.find_elements_by_xpath("//div[@class='_5pcr userContentWrapper']")
        if len(articles) > 10 :
            break

    # Collect
    posts = [] # [ [ POST, REPLIES ], ... ]
    for article in articles:

        # Get Data
        docs = article.get_attribute("innerHTML")
        soup = BeautifulSoup(docs, "html.parser")
        lines = soup.select('p')
        hoo = soup.select("p > a")[0]

        # post
        post = ""
        for line in lines:
            if not line.text.count(hoo.text) == 0:
                post += "▶" + line.text.replace(hoo.text, hoo.text + "\n")[1:]
                continue
            post += line.text[1:] + "\n"

        # reply
        replies = []
        elements = article.find_elements_by_xpath(".//span[@class=' UFICommentActorAndBody']")
        for element in elements:
            soup = BeautifulSoup(element.get_attribute("innerHTML"), "html.parser")
            name = soup.select("span.UFICommentActorName")
            if len(name) == 0:
                name = soup.select("a.UFICommentActorName")
            name = name[0].text
            text = soup.select("span.UFICommentBody")[0].text
            replies.append([name, text])

        # Save
        posts.append([post, replies])
        
    # Print
    for post in posts:
        print(post[0])
        for reply in post[1]:
            print(reply[0] + " : " + reply[1])
        print()

    # Close
    driver.close()
    driver.quit()
    
Crawling()
