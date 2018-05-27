from selenium import webdriver
from bs4 import BeautifulSoup


# formatting output
def formatting(article):
    print(f"{str(article):>14} ",end='')

# option
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('chromedriver', chrome_options=options)

# get page
driver.get('https://movie.naver.com/movie/running/current.nhn?view=list&tab=normal&order=point#')

# variables
titles = []
scores = []
times  = []
dates  = []
directors = []
actors = []


for idx in range(1, 11):

    titles.append(driver.find_element_by_xpath(   "//ul[@class='lst_detail_t1']/li[" + str(idx) + "]/dl[@class='lst_dsc']/dt[@class='tit']/a"))      # title    

    scores.append(driver.find_element_by_xpath(   "//ul[@class='lst_detail_t1']/li[" + str(idx) + "]//span[@class='num']").text)                     # score

    # find dirctors
    directors.append([])
    for director in driver.find_elements_by_xpath("//ul[@class='lst_detail_t1']/li[" + str(idx) + "]//dd[2]/span[@class='link_txt']/a"):
        directors[idx-1].append(director.text)

    # find actors
    actors.append([])
    for actor in driver.find_elements_by_xpath("//ul[@class='lst_detail_t1']/li[" + str(idx) + "]//dd[3]/span[@class='link_txt']/a"):
        actors[idx-1].append(actor.text)

    # move movie page
    titles[idx-1].click()
    summary = driver.find_elements_by_xpath("//dl[@class='info_spec']/dd[1]/p/span")
    length  = len(summary)
    times.append(summary[length - 2].text)
    dates.append(summary[length - 1].text)

    # move back
    driver.back()

    # title
    titles[idx-1] = driver.find_element_by_xpath("//ul[@class='lst_detail_t1']/li[" + str(idx) + "]/dl[@class='lst_dsc']/dt[@class='tit']/a")

    formatting("title:")
    print(titles[idx-1].text)

    formatting("rating:")
    print(scores[idx-1])

    formatting("running time:")
    print(times[idx-1])

    formatting("opening date:")
    print(dates[idx-1][-14:-3])

    formatting("director(s):")
    output = ""
    for director in directors[idx-1]:
        output += director + ","
    print(output[:-1])

    formatting("actor(s):")
    output = ""
    for actor in actors[idx-1]:
        output += actor + ","
    print(output[:-1])
    print()

# close the browser
driver.close()
driver.quit()
