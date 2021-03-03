import requests #爬蟲
import zipfile #解壓縮用
import os #刪除zip檔
import json #driver版本存取
from time import sleep #緩衝
from win32com.client import Dispatch #讀取本地Chrome版本

def getLocalVersion():
    #目的：讀取本地Chrome版本號 
    #輸入：無
    #輸出：本地版本號 
    CHROME_PATH = r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe' #瀏覽器預設位置
    versionParser = Dispatch('Scripting.FileSystemObject') #存取電腦檔案 
    localVersion = versionParser.GetFileVersion(CHROME_PATH) #得到版本號 
    return localVersion.split('.')[0] #版本為：xx.yy.zz.aa 擷取xx可以得到最新版本號 
    
def getLastestVersion(localVersion):
    #目的：得到最新Chrome版本號 
    #輸入：本地版本號 
    #輸出：最新版本號 
    DRIVER_VERSION_API=f'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{localVersion}' #得到driver位置
    lastestVersion= requests.get(DRIVER_VERSION_API).text 
    return lastestVersion

def checkLastestVersion():
    #目的：檢查目前版本是否為最新版，若不是則安裝最新版 
    #輸入：無
    #輸出：無
    localVersion=getLocalVersion()
    lastestVersion=getLastestVersion(localVersion)
    with open(r'./data/driver_data.json','r') as Data:
        driverData=json.load(Data)
        driverVersion=driverData['version']
    if driverVersion == lastestVersion:
        print('您的driver已經是最新版本！')
    else:
        downloadZip(lastestVersion)
        extractZip()
        with open(r'./data/driver_data.json','w') as Data:
            driverData['version']=lastestVersion
            json.dump(driverData,Data,indent=4)
        print(f'您的driver已更新到{lastestVersion}版！')

def downloadZip(lastestVersion):
    #目的：安裝最新版 
    #輸入：最新版本號 
    #輸出：無
    DRIVER_URL=f'https://chromedriver.storage.googleapis.com/{lastestVersion}/chromedriver_win32.zip'
    downloadRequests = requests.get(DRIVER_URL)
    with open(r'./driver.zip', "wb") as code:
        code.write(downloadRequests.content)

def extractZip():
    #目的：解壓縮driver並刪除壓縮檔 
    #輸入：無
    #輸出：無
    with zipfile.ZipFile('driver.zip','r') as zip:
        zip.extractall(r'./driver')
    sleep(3)
    os.remove('driver.zip')

if __name__=='__main__' :
    checkLastestVersion()
    
# Reference
# https://yanwei-liu.medium.com/%E7%94%A8python%E4%B8%8B%E8%BC%89%E6%AA%94%E6%A1%88-451d1b6f5c10
# https://medium.com/drunk-wis/python-selenium-chrome-browser-%E8%88%87-driver-%E6%83%B1%E4%BA%BA%E7%9A%84%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86-cbaf1d1861ce
