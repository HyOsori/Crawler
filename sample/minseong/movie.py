from selenium import webdriver

# 위치
path = "./chromedriver.exe"
driver = webdriver.Chrome(path)

# 페이지 다운로드
driver.get('https://movie.naver.com/movie/running/current.nhn?view=list&tab=normal&order=point#')


for rank in range(1, 11):
    print("RANK "+str(rank)+" ============================================================================")
    commonPath = "//li["+str(rank)+"]/dl[@class='lst_dsc']"
    print("제목 : "+driver.find_element_by_xpath(commonPath+"/dt[@class='tit']/a").text)
    print("평점 : "+driver.find_element_by_xpath(commonPath+"/dd[@class='star']//span[@class='num']").text)
    info = driver.find_element_by_xpath(commonPath + "//dl[@class='info_txt1']/dd[1]").text
    
    if str(info).count('|') == 1:
        print("시간 : "+str(info).split('|')[0])
        print("개봉일 : " + str(info).split('|')[1])
    elif str(info).count('|') == 2:
        print("시간 : " + str(info).split('|')[1])
        print("개봉일 : " + str(info).split('|')[2])

    print("감독 : "+driver.find_element_by_xpath(commonPath+"//dl[@class='info_txt1']/dd[2]//a").text)

    actors = driver.find_elements_by_xpath(commonPath + "//dl[@class='info_txt1']/dd[3]//a")
    print("주연 : ", end="")
    for actor in actors:
        if actors.index(actor) == len(actors)-1:
            print(actor.text, end="")
            break
        print(actor.text, end=", ")
    print("\n===================================================================================")

driver.close()
driver.quit()
