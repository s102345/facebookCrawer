from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expectedConditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
from modules.Driver_update import checkLastestVersion
from modules.Login import initialize

def commentCrawer(driver):
    #postUrl = input('請輸入欲查詢的文章網址：')
    postUrl='https://www.facebook.com/twcoolpc/posts/5183933061648663'
    driver.get(postUrl)
    commentButton={'回覆','查看另','檢視另','顯示先前的留言'}
    unfoldComment = driver.find_element_by_partial_link_text('顯示先前')
    unfoldComment.click()

if __name__=='__main__':
    #print('檢查更新中...')
    #checkLastestVersion()
    print('正在登入Facebook...')
    driver = initialize()
    commentCrawer(driver)
    