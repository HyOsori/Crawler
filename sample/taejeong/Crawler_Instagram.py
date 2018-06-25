from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Variable
tag = input("Enter a tag : ")

def Crawling():

    # Time Check
    t = time.clock()
    
    # Driver
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    driver.get('https://www.instagram.com/tags/' + tag)

    # Load
    lines = []
    while True:
        lines = driver.find_elements_by_xpath("//*[@class='Nnq7C weEfm']")
        if len(lines) > 3 or time.clock() - t > 3:
            break

    # Get Articles
    links = []
    for line in lines:
        articles = line.find_elements_by_tag_name('a')
        for article in articles:
            links.append(article.get_attribute("href"))

    # Collect
    posts  = [] # [ [ MEDIAE, TEXTS  ], ... ]
    for link in links:
        driver.get(link)
        
        # Media
        mediae = [] # [ SRC, ... ]
        btn = driver.find_elements_by_xpath("//article/div[1]/div/div/a")
        number = len(driver.find_elements_by_xpath("//*[@class='Yi5aA ']"))
        while True:
            media = ""
            content = driver.find_elements_by_tag_name("video")
            if not len(content) > 0:
                content = driver.find_elements_by_tag_name("img")
            media = content[0].get_attribute("src")
            mediae.append(media)
            number -= 1
            if number < 0:
                break
            btn[0].click()
        
        # Texts
        texts  = [] # [ [ NAME , CONTENT ], ... ]
        wordings = driver.find_elements_by_xpath("//*[@class='Xl2Pu']/li")
        for wording in wordings:
            if not wording.get_attribute("class") == "LGYDV":
                docs = wording.get_attribute("innerHTML")
                soup = BeautifulSoup(docs, "html.parser")
                name = soup.select('a')[0].text
                content = soup.select("span")[0].text
                texts.append([name, content])

        # Save
        posts.append([mediae, texts])
        
    # Print
    if len(posts) == 0:
        print("nothing has the tag.")
    print()
    for post in posts:
        for media in post[0]:
            print("MEDIA : " + media)
        for text  in post[1]:
            print(text[0].encode("euc-kr", errors='ignore').decode("euc-kr") + " : " +\
                  text[1].encode("euc-kr", errors='ignore').decode("euc-kr"))
        print()

    # Close
    driver.close()
    driver.quit()

Crawling()
