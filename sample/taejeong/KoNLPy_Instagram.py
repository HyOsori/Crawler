def Crawling():

    # input
    tag = input("Enter a tag : ")

    # import
    from selenium import webdriver
    from bs4 import BeautifulSoup
    import time

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
        if len(lines) > 3: # or time.clock() - t > 10:
            break

    # Get Articles
    links = []
    for line in lines:
        articles = line.find_elements_by_tag_name('a')
        for article in articles:
            links.append(article.get_attribute("href"))

    # Collect
    posts  = [] # [ TEXTS, ... ]
    for link in links:
        driver.get(link)
        
        # Texts
        texts  = [] # [ [ NAME , CONTENT ], ... ]
        wordings = driver.find_elements_by_xpath("//*[@class='Xl2Pu']/li")
        for wording in wordings:
            if not wording.get_attribute("class") == "LGYDV":
                docs = wording.get_attribute("innerHTML")
                soup = BeautifulSoup(docs, "html.parser")
                name = soup.select('a')[0].text.encode("euc-kr", errors="ignore").decode("euc-kr")
                content = soup.select("span")[0].text.encode("euc-kr", errors="ignore").decode("euc-kr")
                texts.append([name, content])

        # Save
        posts.append(texts)

    # Close
    driver.close()
    driver.quit()

    # Return
    return posts

def run():

    # Crawling
    posts = Crawling()

    # Import
    from konlpy.tag import Kkma
    kkma = Kkma()
    
    # Data
    words = {}
    for post in posts:
        for wording in post:
            for word in kkma.nouns(wording[1].encode("euc-kr", errors="ignore").decode("euc-kr").replace("\n","")):
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1

    # Sort
    words = list(words.items())
    need = True
    while need:
        need = False
        for idx in range(1, len(words)):
            if words[idx][1] > words[idx - 1][1]:
                need = True
                temp = words[idx]
                words[idx] = words[idx-1]
                words[idx-1] = temp

    # Print
    for word in words:
        print(str(word))

run()